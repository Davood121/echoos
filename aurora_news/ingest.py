# aurora_news/ingest.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import feedparser
# Note: sentence_transformers and chromadb would be installed in the env
# We import them inside functions or try/except to allow the script to load even if deps are missing during dev
try:
    from sentence_transformers import SentenceTransformer
    import chromadb
except ImportError:
    SentenceTransformer = None
    chromadb = None

app = FastAPI()

# Global instances (lazy loaded)
embed_model = None
db_client = None
collection = None

def get_model():
    global embed_model
    if embed_model is None and SentenceTransformer:
        embed_model = SentenceTransformer('all-mpnet-base-v2')
    return embed_model

def get_collection():
    global db_client, collection
    if chromadb and collection is None:
        db_client = chromadb.Client()
        collection = db_client.get_or_create_collection('news')
    return collection

class Source(BaseModel):
    url: str
    type: str = 'rss'

@app.post('/fetch')
async def fetch(source: Source):
    if not SentenceTransformer or not chromadb:
        raise HTTPException(status_code=503, detail="ML dependencies not installed")

    d = feedparser.parse(source.url)
    results = []
    col = get_collection()
    model = get_model()

    if not col or not model:
        raise HTTPException(status_code=500, detail="Database or Model init failed")

    for e in d.entries:
        title = e.get('title', 'No Title')
        summary = e.get('summary', '')
        link = e.get('link', '')
        
        text = f"{title}\n{summary}"
        
        # Generate embedding
        emb = model.encode([text]).tolist()[0]
        
        # Add to DB (using link as ID to avoid dupes)
        col.add(
            documents=[text],
            metadatas=[{'url': link, 'source': source.url}],
            embeddings=[emb],
            ids=[link]
        )
        results.append({'title': title, 'link': link})
        
    return {'count': len(results), 'items': results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
