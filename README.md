# EchoOS — AI Assistant OS

**EchoOS** is a lightweight, secure operating system blueprint designed to run your personal AI assistant. It features a private local LLM runtime, RAG memory, face verification, and an app controller.

## Features
- **Private AI**: Local LLM runtime (llama.cpp/Transformers).
- **Security**: Camera-based face verification.
- **Automation**: App controller to launch and manage applications.
- **Aurora UI**: Cinematic, animated HUD for interaction.
- **News Engine**: Real-time, trustworthy news context.

## Directory Structure
- `ai_core/`: LLM wrappers and model management.
- `agents/`: Safe tool runners and planners.
- `camera/`: Face capture and verification logic.
- `app_controller/`: OS automation and app registry.
- `web_ui/`: React-based frontend (Aurora).
- `services/`: Systemd unit files.
- `scripts/`: Installers and build tools.

## Getting Started
See `scripts/install_echoos.sh` to set up the environment.
