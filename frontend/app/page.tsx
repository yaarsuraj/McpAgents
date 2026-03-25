'use client';
import { useState, useEffect } from 'react';

export default function Home() {
    const [gameState, setGameState] = useState<any>(null);

    const fetchState = async () => {
        try {
            const res = await fetch("http://localhost:8000/state");
            const data = await res.json();
            setGameState(data);
        } catch (e) {
            console.error(e);
        }
    };

    const nextTick = async () => {
        try {
            const res = await fetch("http://localhost:8000/tick", { method: 'POST' });
            const data = await res.json();
            setGameState(data);
        } catch (e) {
            console.error(e);
        }
    };

    useEffect(() => {
        fetchState();
    }, []);

    if (!gameState) return <div className="p-8 text-neutral-400">Looking for backend API on port 8000... <button onClick={fetchState} className="underline text-blue-400 ml-4">Retry</button></div>;

    return (
        <div className="min-h-screen bg-neutral-900 text-neutral-100 p-8 font-sans">
            <div className="max-w-6xl mx-auto border border-neutral-800 rounded-xl overflow-hidden shadow-2xl bg-neutral-800/50 backdrop-blur">

                <div className="p-6 border-b border-neutral-700 flex justify-between items-center bg-neutral-800">
                    <div>
                        <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">Intelligent Traffic Orchestrator</h1>
                        <p className="text-sm text-neutral-400 mt-1 flex items-center gap-2">
                            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                            Live Multi-Agent Simulation
                        </p>
                    </div>
                    <button onClick={nextTick} className="flex items-center gap-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold py-2 px-6 rounded-lg transition-all shadow-lg active:scale-95">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
                        Next Cycle Tick
                    </button>
                </div>

                <div className="p-6 grid grid-cols-1 md:grid-cols-12 gap-6">

                    {/* Metrics - 4 cols */}
                    <div className="md:col-span-4 flex flex-col gap-4">
                        <div className="bg-neutral-800 border border-neutral-700/50 p-5 rounded-xl shadow-inner relative overflow-hidden">
                            <div className="absolute top-0 left-0 w-2 h-full bg-emerald-500"></div>
                            <h2 className="text-lg font-bold mb-4 text-neutral-300 tracking-wide uppercase text-xs flex items-center gap-2 font-mono">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2v20"></path><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
                                Global Performance
                            </h2>
                            <div className="space-y-4 font-mono text-sm">
                                <div className="flex justify-between items-end border-b border-neutral-700/50 pb-2">
                                    <span className="text-neutral-400">Avg Travel Time</span>
                                    <span className="text-xl text-emerald-300 font-bold">{gameState.metrics?.avg_travel_time_sec?.toFixed(1)}s</span>
                                </div>
                                <div className="flex justify-between items-end border-b border-neutral-700/50 pb-2">
                                    <span className="text-neutral-400">Network Throughput</span>
                                    <span className="text-xl text-blue-300 font-bold">{gameState.metrics?.network_throughput_veh_per_min?.toFixed(1)} <span className="text-xs">v/min</span></span>
                                </div>
                                <div className="flex justify-between items-end border-b border-neutral-700/50 pb-2">
                                    <span className="text-neutral-400">Congestion Events</span>
                                    <span className="text-xl text-orange-400 font-bold">{gameState.metrics?.congestion_events}</span>
                                </div>
                                <div className="flex justify-between items-end pb-2">
                                    <span className="text-neutral-400">Signal Efficiency</span>
                                    <span className="text-xl text-indigo-300 font-bold">{(gameState.metrics?.signal_efficiency_score * 100)?.toFixed(1)}%</span>
                                </div>
                            </div>
                        </div>

                        <div className="bg-neutral-800 border border-neutral-700/50 p-5 rounded-xl text-xs font-mono text-neutral-400 overflow-x-auto shadow-inner h-full">
                            <div className="font-bold mb-2 text-indigo-400">RL Policy Weights:</div>
                            <pre>{JSON.stringify(gameState.rl_policy, null, 2)}</pre>
                        </div>
                    </div>

                    {/* Zones & Signals - 8 cols */}
                    <div className="md:col-span-8 flex flex-col gap-6">

                        <div className="bg-neutral-800 border border-neutral-700/50 p-5 rounded-xl shadow-inner relative overflow-hidden">
                            <div className="absolute top-0 left-0 w-2 h-full bg-orange-500"></div>
                            <h2 className="text-lg font-bold mb-4 text-neutral-300 tracking-wide uppercase text-xs flex items-center gap-2 font-mono">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                                City Zones
                            </h2>

                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                {Object.entries(gameState.zones).map(([zoneId, zData]: any) => (
                                    <div key={zoneId} className={`p-4 rounded-lg border flex flex-col relative overflow-hidden ${zData.congestion_level === 'high' || zData.congestion_level === 'critical' ? 'border-red-500/50 bg-red-950/20' : 'border-neutral-700 bg-neutral-900/40'}`}>
                                        <h3 className="font-bold text-lg mb-1 flex items-center justify-between">
                                            {zoneId}
                                            <span className={`text-[10px] uppercase px-2 py-0.5 rounded-full ${zData.congestion_level === 'high' || zData.congestion_level === 'critical' ? 'bg-red-500/20 text-red-400 border border-red-500/50' : 'bg-green-500/20 text-green-400 border border-green-500/50'}`}>
                                                {zData.congestion_level}
                                            </span>
                                        </h3>
                                        <div className="w-full bg-neutral-800 h-2 rounded-full overflow-hidden mt-3 mb-1 border border-neutral-700">
                                            <div className={`h-full ${zData.vehicle_density > 0.7 ? 'bg-red-500' : 'bg-emerald-500'}`} style={{ width: `${zData.vehicle_density * 100}%` }}></div>
                                        </div>
                                        <div className="flex justify-between text-xs text-neutral-400 font-mono mb-3">
                                            <span>Density: {(zData.vehicle_density * 100).toFixed(0)}%</span>
                                            <span>Speed: {zData.average_speed_kmh}km/h</span>
                                        </div>

                                        <div className="mt-auto border-t border-neutral-700/50 pt-2 text-xs font-mono">
                                            <span className="text-neutral-500">Queues: </span>
                                            <span className="text-neutral-300">{Object.entries(zData.queue_lengths).map(([inter, q]) => `${inter}(${q})`).join(', ')}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="bg-neutral-800 border border-neutral-700/50 p-5 rounded-xl shadow-inner relative overflow-hidden">
                            <div className="absolute top-0 left-0 w-2 h-full bg-yellow-400"></div>
                            <h2 className="text-lg font-bold mb-4 text-neutral-300 tracking-wide uppercase text-xs flex items-center gap-2 font-mono">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="9" y="9" width="6" height="14" rx="2"></rect><circle cx="12" cy="14" r="1.5"></circle><rect x="4" y="4" width="16" height="5" rx="2"></rect><path d="M12 2v2"></path></svg>
                                Dynamic Signal Control
                            </h2>

                            <div className="flex flex-wrap gap-4">
                                {Object.entries(gameState.signals).map(([sigId, sData]: any) => (
                                    <div key={sigId} className="flex flex-col items-center p-4 border border-neutral-700 bg-neutral-900/40 rounded-xl relative hover:border-neutral-500 transition-colors">
                                        <span className="font-mono text-xs text-neutral-400 mb-3 uppercase tracking-wider">{sigId}</span>
                                        <div className={`w-10 h-10 rounded-full flex items-center justify-center border-4 border-neutral-800 ${sData.current_phase === 'green' ? 'bg-emerald-500 shadow-[0_0_20px_rgba(16,185,129,0.5)]' : 'bg-neutral-700 shadow-inner'}`}>
                                            {sData.current_phase === 'green' && <div className="w-2 h-2 rounded-full bg-white opacity-80"></div>}
                                        </div>
                                        <div className={`w-10 h-10 rounded-full mt-2 flex items-center justify-center border-4 border-neutral-800 ${sData.current_phase === 'red' ? 'bg-red-500 shadow-[0_0_20px_rgba(239,68,68,0.5)]' : 'bg-neutral-700 shadow-inner'}`}>
                                            {sData.current_phase === 'red' && <div className="w-2 h-2 rounded-full bg-white opacity-80"></div>}
                                        </div>

                                        <div className="mt-3 bg-neutral-800 px-3 py-1 text-xs font-mono font-bold rounded text-neutral-300 border border-neutral-700/50">
                                            {sData.phase_duration_sec}s
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    );
}
