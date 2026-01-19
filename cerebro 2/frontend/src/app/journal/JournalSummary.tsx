"use client";
import React, { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import api from "../../services/api";
import "../../styles/journal-polish.css";

// Type definitions
interface Stats {
  total_apps: number;
  target_apps: number;
  total_leetcode: number;
  target_leetcode: number;
  easy: number;
  medium: number;
  hard: number;
  skipped_days: string[];
  easy_solved: number;
  easy_suggested: number;
  medium_solved: number;
  medium_suggested: number;
  hard_solved: number;
  hard_suggested: number;
}

interface DialogueLine {
  agent: keyof typeof AGENT_META;
  stage: string;
  speech: string;
  key: number;
}

// Map agent names to colors and images (update paths as needed)
const AGENT_META = {
  ANXIETY: { color: "purple", img: "/assets/images/fear.png" },
  ANGER: { color: "red", img: "/assets/images/anger.png" },
  SADNESS: { color: "blue", img: "/assets/images/sadness.png" },
  JOY: { color: "yellow", img: "/assets/images/joyicon.png" },
  LOGIC: { color: "cyan", img: "/assets/images/logicicon.png" },
};

function parseDialogue(summary: string | undefined | null): DialogueLine[] {
  if (!summary || typeof summary !== "string") return [];
  // Split summary into lines, group by agent
  const lines = summary.split(/\n|\r/).filter(Boolean);
  return lines.map((line, idx) => {
    // Match AGENT: (stage) speech OR AGENT: speech
    const match = line.match(/^(ANXIETY|ANGER|SADNESS|JOY|LOGIC):?\s*(?:\((.*?)\))?\s*(.*)$/i);
    if (match) {
      return {
        agent: match[1].toUpperCase() as keyof typeof AGENT_META,
        stage: match[2] || "",
        speech: match[3],
        key: idx,
      };
    }
    return { agent: "LOGIC", stage: "", speech: line, key: idx };
  });
}

const CHARACTER_VOICES = {
  JOY: { voice_id: "EXAVITQu4vr4xnSDxMaL", stability: 0.2, similarity_boost: 0.7 }, // Nicole
  ANGER: { voice_id: "TxGEqnHWrfWFTfGW9XjX", stability: 0.8, similarity_boost: 0.5 }, // Bill
  ANXIETY: { voice_id: "MF3mGyEYCl7XYWbV9V6O", stability: 0.3, similarity_boost: 0.6 }, // Ethan
  LOGIC: { voice_id: "pNInz6obpgDQGcFmaJgB", stability: 0.9, similarity_boost: 0.9 }, // Brian
  SADNESS: { voice_id: "21m00Tcm4TlvDq8ikWAM", stability: 0.4, similarity_boost: 0.7 }, // Rachel
};

const ELEVENLABS_API_KEY = process.env.NEXT_PUBLIC_ELEVENLABS_API_KEY || "sk_864f9771a4a2c35f376f355c099bd3cdfaaf177eb686b1d7";

function getVoiceMeta(agent: keyof typeof CHARACTER_VOICES) {
  return CHARACTER_VOICES[agent] || CHARACTER_VOICES.LOGIC;
}

const JournalSummary: React.FC = () => {
  const [summary, setSummary] = useState("");
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [currentIndex, setCurrentIndex] = useState(0);
  const [motivation, setMotivation] = useState<{ image_url: string | null; title: string } | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const router = useRouter();

  useEffect(() => {
    fetch("/api/journal/summary")
      .then((res) => res.json())
      .then((data) => {
        setSummary(data.summary);
        setStats(data.stats);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load journal summary.");
        setLoading(false);
      });
    // Fetch motivational image
    api.getMotivationalImage().then(setMotivation).catch(() => setMotivation(null));
  }, []);

  // Remove auto-play from useEffect. Add a play button for user-triggered audio.
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [isAudioLoading, setIsAudioLoading] = useState(false);

  const fetchAudio = async (agent: keyof typeof CHARACTER_VOICES, speech: string) => {
    setIsAudioLoading(true);
    const { voice_id, stability, similarity_boost } = getVoiceMeta(agent);
    try {
      const res = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voice_id}`, {
        method: "POST",
        headers: {
          "xi-api-key": ELEVENLABS_API_KEY,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          text: speech,
          voice_settings: { stability, similarity_boost }
        })
      });
      if (!res.ok) throw new Error("Failed to fetch audio");
      const blob = await res.blob();
      setAudioUrl(URL.createObjectURL(blob));
    } catch (e) {
      setAudioUrl(null);
    } finally {
      setIsAudioLoading(false);
    }
  };

  const dialogue = parseDialogue(summary);
  const current = dialogue[currentIndex];
  const total = dialogue.length;

  useEffect(() => {
    setAudioUrl(null); // Clear audio when navigating
  }, [currentIndex, summary]);

  // Auto-play audio and auto-advance on end
  useEffect(() => {
    if (!current) return;
    let cancelled = false;
    const play = async () => {
      try {
        await fetchAudio(current.agent, current.speech);
      } catch (e) {
        setAudioUrl(null);
      }
    };
    play();
    return () => { cancelled = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentIndex, summary]);

  // Auto-advance when audio ends
  useEffect(() => {
    if (!audioRef.current) return;
    const handleEnded = () => {
      setAudioUrl(null);
      if (currentIndex < dialogue.length - 1) {
        setCurrentIndex(currentIndex + 1);
      }
    };
    const audio = audioRef.current;
    audio.addEventListener('ended', handleEnded);
    audio.addEventListener('error', handleEnded); // advance on error too
    return () => {
      audio.removeEventListener('ended', handleEnded);
      audio.removeEventListener('error', handleEnded);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [audioUrl, currentIndex, dialogue.length]);

  const handleNav = (idx: number) => {
    setCurrentIndex(idx);
  };

  if (loading) return <div className="p-8 text-lg">Loading journal summary...</div>;
  if (error) return <div className="p-8 text-red-600">{error}</div>;

  return (
    <div
      className="min-h-screen bg-cover bg-center flex flex-col items-center"
      style={{ backgroundImage: "url('/assets/images/background.jpg')" }}
    >
      <div className="w-full max-w-5xl mx-auto py-10 px-4">
        <button
          className="mb-6 px-6 py-2 bg-purple-600 text-white rounded-full font-bold shadow hover:bg-purple-700 transition"
          onClick={() => router.push("/")}
        >
          ← Back to Homepage
        </button>
        <h1 className="text-4xl font-extrabold mb-2 text-center text-white drop-shadow">Weekly Performance Journal</h1>
        <div className="text-center text-gray-500 mb-6">Neural Boardroom Session // Week Review</div>
        {stats && (
          <div className="mb-8 bg-white/80 rounded-2xl p-6 shadow flex flex-wrap gap-6 justify-center border border-purple-200">
            <div className="flex flex-col items-center min-w-[180px]">
              <div className="text-gray-500">Applications</div>
              <div className="text-2xl font-bold">{stats.total_apps} <span className="text-lg font-normal">/ {stats.target_apps}</span></div>
              <div className={`mt-1 text-xs font-semibold ${stats.total_apps >= stats.target_apps ? 'text-green-600' : 'text-red-500'}`}>{stats.total_apps >= stats.target_apps ? 'SUCCESS' : 'FAIL'}</div>
            </div>
            <div className="flex flex-col items-center min-w-[180px]">
              <div className="text-gray-500">Coding Problems</div>
              <div className="text-2xl font-bold">{stats.total_leetcode} <span className="text-lg font-normal">/ {stats.target_leetcode}</span></div>
              <div className={`mt-1 text-xs font-semibold ${stats.total_leetcode >= stats.target_leetcode ? 'text-green-600' : 'text-red-500'}`}>{stats.total_leetcode >= stats.target_leetcode ? 'SUCCESS' : 'FAIL'}</div>
            </div>
            <div className="flex flex-col items-center min-w-[180px]">
              <div className="text-gray-500">Difficulty</div>
              <div className="text-base font-bold"><span className="text-green-600">{stats.easy_solved}</span><span className="text-gray-600"> / {stats.easy_suggested}</span> Easy</div>
              <div className="text-base font-bold"><span className="text-orange-500">{stats.medium_solved}</span><span className="text-gray-600"> / {stats.medium_suggested}</span> Medium</div>
              <div className="text-base font-bold"><span className="text-red-500">{stats.hard_solved}</span><span className="text-gray-600"> / {stats.hard_suggested}</span> Hard</div>
            </div>
            <div className="flex flex-col items-center min-w-[180px]">
              <div className="text-gray-500">Consistency</div>
              <div className="text-base font-bold">{stats.skipped_days.length ? `Skipped ${stats.skipped_days.length} days` : 'No days skipped'}</div>
              <div className="text-xs text-gray-500">{stats.skipped_days.length ? stats.skipped_days.join(", ") : ''}</div>
            </div>
          </div>
        )}
        {(!summary || dialogue.length === 0) && (
          <div className="text-gray-500 text-center py-8">No journal summary available.</div>
        )}
        {current && (
          <div className="flex flex-col items-center mb-8">
            <div className="flex items-center gap-4">
              <img
                src={AGENT_META[current.agent]?.img || "/assets/images/joyicon.png"}
                alt={current.agent}
                className={`w-20 h-20 rounded-full border-4 shadow-lg avatar-glow`}
                style={{
                  borderColor: AGENT_META[current.agent]?.color || "#00bcd4",
                  boxShadow: `0 0 0 6px ${
                    AGENT_META[current.agent]?.color === 'yellow' ? '#fffbe6' :
                    AGENT_META[current.agent]?.color === 'red' ? '#ffeaea' :
                    AGENT_META[current.agent]?.color === 'blue' ? '#eaf4ff' :
                    AGENT_META[current.agent]?.color === 'purple' ? '#f3eaff' : '#eafffa'}`
                }}
              />
              <div className={`rounded-2xl px-6 py-4 shadow-lg text-lg max-w-2xl whitespace-pre-line font-medium border-2 speech-bubble fade-in`}
                style={{
                  background: `${AGENT_META[current.agent]?.color === 'yellow' ? '#fffbe6' : AGENT_META[current.agent]?.color === 'red' ? '#ffeaea' : AGENT_META[current.agent]?.color === 'blue' ? '#eaf4ff' : AGENT_META[current.agent]?.color === 'purple' ? '#f3eaff' : '#eafffa'}`,
                  borderColor: AGENT_META[current.agent]?.color || '#00bcd4',
                  color: AGENT_META[current.agent]?.color === 'yellow' ? '#b59f00' : AGENT_META[current.agent]?.color === 'red' ? '#b00020' : AGENT_META[current.agent]?.color === 'blue' ? '#1e3a8a' : AGENT_META[current.agent]?.color === 'purple' ? '#6d28d9' : '#0891b2',
                  position: 'relative'
                }}
              >
                <span className="speech-bubble-tail" style={{background: AGENT_META[current.agent]?.color === 'yellow' ? '#fffbe6' : AGENT_META[current.agent]?.color === 'red' ? '#ffeaea' : AGENT_META[current.agent]?.color === 'blue' ? '#eaf4ff' : AGENT_META[current.agent]?.color === 'purple' ? '#f3eaff' : '#eafffa', left: '-18px', top: '32px'}}></span>
                <div className="agent-name font-bold mb-1 uppercase tracking-wide">{current.agent}</div>
                {current.speech}
              </div>
            </div>
            <div className="flex justify-center items-center gap-4 mt-6">
              <button
                className="rounded-full border-2 border-purple-300 bg-white/80 w-10 h-10 flex items-center justify-center text-2xl font-bold text-purple-600 shadow hover:bg-purple-100 disabled:opacity-40"
                onClick={() => handleNav(Math.max(currentIndex - 1, 0))}
                disabled={currentIndex === 0}
                aria-label="Previous"
              >
                &#8592;
              </button>
              <span className="text-purple-700 font-semibold text-lg">{currentIndex + 1} / {total}</span>
              <button
                className="rounded-full border-2 border-purple-300 bg-white/80 w-10 h-10 flex items-center justify-center text-2xl font-bold text-purple-600 shadow hover:bg-purple-100 disabled:opacity-40"
                onClick={() => handleNav(Math.min(currentIndex + 1, total - 1))}
                disabled={currentIndex === total - 1}
                aria-label="Next"
              >
                &#8594;
              </button>
            </div>
            {/* Removed Play Voice button for auto-advance */}
            {isAudioLoading && (
              <div className="mt-4 text-blue-600 font-semibold">Loading voice...</div>
            )}
            {audioUrl && (
              <audio ref={audioRef} src={audioUrl} autoPlay />
            )}
          </div>
        )}
        {currentIndex === dialogue.length - 1 && (
          <>
            <div className="directive-card">
              <div className="directive-title">DIRECTIVE FOR NEXT WEEK:</div>
              <div className="text-gray-700 mb-2" style={{fontWeight: 500}}>We need to stabilize. We cannot rely on "bursts" of energy.</div>
              <div className="directive-action">Action A:</div>
              <div className="mb-1">We will initiate a "Power Hour" at 9:00 AM strictly for applications to fix the outreach gap.</div>
              <div className="directive-action">Action B:</div>
              <div className="mb-1">We will attempt one "Hard" problem on Tuesday to satisfy the difficulty requirement.</div>
              <div className="directive-overall">Overall:</div>
              <div>Good work on the coding front. The logic core is strengthening. Let's fix the consistency and keep moving. Dismissed.</div>
            </div>
            {motivation && motivation.image_url && (
              <div className="mt-8 flex flex-col items-center motivation-card bg-white/80 rounded-2xl p-6 shadow border border-yellow-200 max-w-xl mx-auto">
                <img src={motivation.image_url} alt={motivation.title} className="rounded-xl shadow mb-4 w-full object-cover" style={{maxHeight: 300}} />
                <div className="text-lg font-semibold text-yellow-700 text-center">{motivation.title}</div>
                <div className="text-sm text-gray-500 text-center mt-1">Motivational image powered by Freepik</div>
              </div>
            )}
          </>
        )}
        <div className="flex justify-center">
          <img
            src="/assets/images/inside-out-disney-11.jpg"
            alt="Inside Out Boardroom"
            className="rounded-2xl shadow-xl w-full max-w-5xl object-cover"
            style={{ marginBottom: 32 }}
          />
        </div>
      </div>
    </div>
  );
};

export default JournalSummary;
