import React, { useState } from 'react'
import BootAnim from './components/BootAnim'

function App() {
    const [booted, setBooted] = useState(false)

    return (
        <div className="min-h-screen bg-gray-900 text-white overflow-hidden font-sans">
            {!booted && (
                <BootAnim onComplete={() => setBooted(true)} />
            )}

            {booted && (
                <div className="flex flex-col h-screen">
                    {/* Header / HUD Top */}
                    <header className="p-4 border-b border-gray-800 flex justify-between items-center bg-gray-900/80 backdrop-blur">
                        <h1 className="text-xl font-bold tracking-widest text-indigo-400">AURORA OS</h1>
                        <div className="flex gap-4 text-sm text-gray-400">
                            <span>CPU: 12%</span>
                            <span>MEM: 4.2GB</span>
                            <span>NET: ONLINE</span>
                        </div>
                    </header>

                    {/* Main Content Area */}
                    <main className="flex-1 flex items-center justify-center relative">
                        {/* Central Assistant Bubble */}
                        <div className="w-64 h-64 rounded-full bg-gradient-to-t from-indigo-900 to-black border border-indigo-500/30 flex items-center justify-center shadow-[0_0_50px_rgba(79,70,229,0.3)] animate-pulse">
                            <div className="text-center">
                                <p className="text-indigo-300 text-lg">Listening...</p>
                            </div>
                        </div>

                        {/* News / Context Cards (Mock) */}
                        <div className="absolute bottom-10 left-10 w-80 bg-gray-800/50 p-4 rounded-xl border border-gray-700 backdrop-blur">
                            <h3 className="text-xs font-bold text-gray-400 uppercase mb-2">Live Context</h3>
                            <p className="text-sm">System is running normally. No active alerts.</p>
                        </div>
                    </main>
                </div>
            )}
        </div>
    )
}

export default App
