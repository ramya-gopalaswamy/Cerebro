"use client";
import React, { useState, useRef } from "react";

type Agent = "ANXIETY" | "ANGER" | "SADNESS" | "JOY" | "LOGIC";
interface ChatMessage {
  role: "user" | "agent";
  text: string;
  agent?: Agent;
}

const AGENT_META: Record<Agent, { color: string; img: string }> = {
  ANXIETY: { color: "purple", img: "/assets/images/fear.png" },
  ANGER: { color: "red", img: "/assets/images/anger.png" },
  SADNESS: { color: "blue", img: "/assets/images/sadness.png" },
  JOY: { color: "yellow", img: "/assets/images/joyicon.png" },
  LOGIC: { color: "cyan", img: "/assets/images/logicicon.png" },
};
const CHARACTER_VOICES: Record<Agent, { voice_id: string; stability: number; similarity_boost: number }> = {
  JOY: { voice_id: "EXAVITQu4vr4xnSDxMaL", stability: 0.2, similarity_boost: 0.7 },
  ANGER: { voice_id: "TxGEqnHWrfWFTfGW9XjX", stability: 0.8, similarity_boost: 0.5 },
  ANXIETY: { voice_id: "MF3mGyEYCl7XYWbV9V6O", stability: 0.3, similarity_boost: 0.6 },
  LOGIC: { voice_id: "pNInz6obpgDQGcFmaJgB", stability: 0.9, similarity_boost: 0.9 },
  SADNESS: { voice_id: "21m00Tcm4TlvDq8ikWAM", stability: 0.4, similarity_boost: 0.7 },
};
function getVoiceMeta(agent: Agent) {
  return CHARACTER_VOICES[agent] || CHARACTER_VOICES.LOGIC;
}

const ELEVENLABS_API_KEY = process.env.NEXT_PUBLIC_ELEVENLABS_API_KEY || "sk_864f9771a4a2c35f376f355c099bd3cdfaaf177eb686b1d7";

const Chatbot = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const sendMessage = async () => {
    if (!input.trim()) return;
    setMessages((msgs) => [...msgs, { role: "user", text: input }]);
    setLoading(true);
    setInput("");
    // Call backend Gemini endpoint
    const res = await fetch("/api/chatbot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input })
    });
    const data = await res.json();
    // Multi-agent replies
    if (data.replies && Array.isArray(data.replies)) {
      for (const reply of data.replies) {
        setMessages((msgs) => [...msgs, { role: "agent", agent: reply.agent, text: reply.text }]);
        // Play audio for each agent
        if (reply.agent && reply.text) {
          const { voice_id, stability, similarity_boost } = getVoiceMeta(reply.agent as Agent);
          fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voice_id}`,
            {
              method: "POST",
              headers: {
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
              },
              body: JSON.stringify({
                text: reply.text,
                voice_settings: { stability, similarity_boost }
              })
            }
          )
            .then(res => res.blob())
            .then(blob => {
              if (audioRef.current) audioRef.current.pause();
              const audio = new Audio(URL.createObjectURL(blob));
              audioRef.current = audio;
              audio.play();
            });
        }
      }
    }
    setLoading(false);
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
      {!open && (
        <button
          className="rounded-full shadow-lg bg-white border-2 border-purple-400 p-3 hover:bg-purple-100 transition"
          style={{ width: 60, height: 60 }}
          aria-label="Open chatbot"
          onClick={() => setOpen(true)}
        >
          <img src="/assets/images/joyicon.png" alt="Chatbot" className="w-10 h-10" />
        </button>
      )}
      {open && (
        <div className="flex flex-col items-end">
          <div className="fixed inset-0 bg-black/30 z-40" onClick={() => setOpen(false)} />
          <div className="relative z-50">
            <div className="w-80 bg-white/90 rounded-2xl shadow-2xl border-2 border-purple-300 p-4 mb-2 flex flex-col max-h-[60vh] overflow-y-auto">
              {messages.map((msg, i) =>
                msg.role === "user" ? (
                  <div key={i} className="flex justify-end mb-2">
                    <div className="bg-purple-100 text-purple-900 px-4 py-2 rounded-2xl max-w-[70%] shadow">{msg.text}</div>
                  </div>
                ) : (
                  <div key={i} className="flex items-start gap-2 mb-2">
                    <img src={msg.agent ? AGENT_META[msg.agent].img : ""} alt={msg.agent} className="w-10 h-10 rounded-full border-2" style={{ borderColor: msg.agent ? AGENT_META[msg.agent].color : undefined }} />
                    <div className="bg-white px-4 py-2 rounded-2xl shadow border-2" style={{ borderColor: msg.agent ? AGENT_META[msg.agent].color : undefined, color: msg.agent ? AGENT_META[msg.agent].color : undefined }}>
                      <div className="font-bold text-xs mb-1 uppercase">{msg.agent}</div>
                      {msg.text}
                    </div>
                  </div>
                )
              )}
              {loading && <div className="text-gray-400 text-sm">Thinking...</div>}
            </div>
            <div className="flex gap-2 w-80">
              <input
                className="flex-1 px-4 py-2 rounded-l-2xl border-2 border-purple-300 focus:outline-none"
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === "Enter" && sendMessage()}
                placeholder="Ask the agents..."
                disabled={loading}
              />
              <button
                className="px-4 py-2 bg-purple-600 text-white rounded-r-2xl font-bold shadow hover:bg-purple-700 transition"
                onClick={sendMessage}
                disabled={loading}
              >
                Send
              </button>
              <button
                className="ml-2 px-2 py-2 rounded-full bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold border border-gray-400"
                aria-label="Close chatbot"
                onClick={() => setOpen(false)}
              >
                ×
              </button>
              <button
                className="ml-2 px-2 py-2 rounded-full bg-purple-200 hover:bg-purple-300 text-purple-700 font-bold border border-purple-400"
                aria-label="Clear chat"
                onClick={() => setMessages([])}
              >
                🗑
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
