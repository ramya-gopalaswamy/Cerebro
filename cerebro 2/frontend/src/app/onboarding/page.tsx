"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

const IMG_JOY = "/assets/images/joy.png";
const IMG_ANGER = "/assets/images/anger.png";
const IMG_SADNESS = "/assets/images/sadness.png";
const IMG_DISGUST = "/assets/images/disgust.png";
const IMG_FEAR = "/assets/images/fear.png";

const GOAL_TYPES = [
  { icon: '💼', label: 'Career' },
  { icon: '🧠', label: 'Mindset' },
  { icon: '✈️', label: 'Travel' },
  { icon: '🏠', label: 'Personal Project' },
  { icon: '🌱', label: 'New Habit' },
  { icon: '💪', label: 'Fitness' },
];

export default function Onboarding() {
  const [goal, setGoal] = useState('');
  const [selectedType, setSelectedType] = useState('Career');
  const router = useRouter();

  // Helper to check if input is job/career related
  function isCareerGoal(goal: string) {
    const keywords = ['job', 'career', 'work', 'employment', 'interview', 'offer', 'resume', 'cv', 'company', 'position', 'role', 'hire'];
    return keywords.some(word => goal.toLowerCase().includes(word));
  }

  return (
    <div className="onboarding-background min-h-screen flex flex-col items-center justify-center">
      <div className="w-full max-w-3xl mx-auto flex flex-col items-center bg-transparent p-0 md:p-4 relative" style={{ minHeight: '80vh', justifyContent: 'center' }}>
        {/* Title - moved to top of page */}
        <h1 className="text-3xl md:text-5xl font-extrabold text-white text-center drop-shadow-lg mb-1 mt-0 tracking-wide" style={{ position: 'absolute', top: 0, left: 0, width: '100%' }}>
          SET COURSE: <br className="md:hidden" />OPERATIONS HEADQUARTERS
        </h1>
        <div style={{ height: '4rem' }} />
        {/* Characters - evenly spaced and centered below textbox, increase size of all except Joy */}
        <div className="flex flex-row items-end justify-center w-full gap-8" style={{ marginBottom: '2vh' }}>
          <img src={IMG_SADNESS} width={110} alt="Sadness" className="character-float" />
          <img src={IMG_FEAR} width={100} alt="Fear" className="character-float" />
          <img src={IMG_JOY} width={85} alt="Joy" className="character-float" />
          <img src={IMG_DISGUST} width={100} alt="Disgust" className="character-float" />
          <img src={IMG_ANGER} width={110} alt="Anger" className="character-float" />
        </div>
        {/* Input Box without Enter button */}
        <div className="flex flex-row items-center justify-center w-full" style={{ marginTop: '2vh', marginBottom: '2vh' }}>
          <input
            type="text"
            value={goal}
            onChange={e => setGoal(e.target.value)}
            placeholder="My next big goal is... (e.g., Land my dream job!)"
            className="w-full max-w-2xl px-8 py-4 rounded-full border-2 border-white bg-white bg-opacity-90 text-lg md:text-xl text-gray-800 shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>
        {/* Goal Type Buttons */}
        <div className="flex flex-row flex-wrap justify-center gap-2 md:gap-4 mb-6">
          {GOAL_TYPES.map(type => (
            <button
              key={type.label}
              className={`flex flex-col items-center px-4 py-2 rounded-xl border-2 font-semibold text-white text-sm md:text-base shadow-md transition-all duration-200 ${selectedType === type.label ? 'bg-blue-600 border-blue-400 scale-105' : 'bg-black bg-opacity-30 border-transparent hover:bg-blue-400 hover:bg-opacity-80'}`}
              onClick={() => {
                setSelectedType(type.label);
                // If Career icon is clicked and goal is job/career related or not empty, redirect
                if ((type.label === 'Career') && (isCareerGoal(goal) || goal.trim() !== '')) {
                  router.push('/joblandlandingpage');
                }
              }}
            >
              <span className="text-2xl mb-1">{type.icon}</span>
              {type.label}
            </button>
          ))}
        </div>
        {/* Activate Button */}
        <button
          className="w-full max-w-md py-4 rounded-full bg-cyan-400 text-black text-2xl font-extrabold shadow-2xl hover:bg-cyan-500 transition-all tracking-wide glow-btn mb-2"
          onClick={() => {
            if (isCareerGoal(goal) || selectedType === 'Career') {
              router.push('/joblandlandingpage');
            } else {
              alert(`Goal: ${goal}\nType: ${selectedType}`);
            }
          }}
        >
          <span className="flex items-center justify-center gap-2">
            <span role="img" aria-label="brain">🧠</span> ACTIVATE GOALS
          </span>
        </button>
      </div>
      <style jsx>{`
        .onboarding-background {
          background-image: url('/background.jpg');
          background-size: cover;
          background-position: center;
          min-height: 100vh;
        }
        .character-float {
          filter: drop-shadow(0 4px 12px #2226);
        }
        .glow-btn {
          box-shadow: 0 0 24px 4px #00e6ff99, 0 2px 8px #0004;
        }
      `}</style>
    </div>
  );
}
