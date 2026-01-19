"use client";

import React, { useState, useRef } from 'react';
import { ProgressTrack } from '@/components/ProgressTrack';
import { useRouter } from 'next/navigation';

const JobOnboardingPage = () => {
  // State for sliders
  const [jobCompleted, setJobCompleted] = useState(3);
  const [leetcodeCompleted, setLeetcodeCompleted] = useState(1);
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleResumeUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setResumeFile(e.target.files[0]);
    }
  };

  const handleActivateGoals = () => {
    if (!resumeFile) {
      alert('Please upload resume to continue.');
      return;
    }
    // TODO: Save resume to backend here
    router.push('/');
  };

  return (
    <div className="relative min-h-screen w-full flex items-center justify-center corememories-bg">
      <div className="border-4 border-[#b18fff] rounded-[40px] p-2 w-full max-w-4xl flex flex-col items-center" style={{ boxShadow: '0 0 0 4px #b18fff, 0 8px 40px 0 rgba(80,0,180,0.25)', background: 'rgba(255,255,255,0.28)', backdropFilter: 'blur(18px)', WebkitBackdropFilter: 'blur(18px)' }}>
        <div className="w-full h-full rounded-[36px] bg-transparent flex flex-col items-center px-2 py-8 md:px-12 md:py-12">
          <h1 className="text-5xl md:text-6xl font-extrabold text-white tracking-wider mb-12 text-center drop-shadow-lg" style={{ letterSpacing: '0.06em' }}>SET DAILY CORE MEMORIES</h1>
          <div className="w-full flex flex-col gap-16 mb-12 relative">
            {/* Chatbox speech bubble */}
            <div className="absolute right-0 top-0 z-20" style={{marginRight: '1.5rem', marginTop: '-2.5rem'}}>
              <div className="relative bg-white rounded-2xl px-4 py-2 shadow-lg border-2 border-blue-200 text-xs md:text-sm font-semibold text-purple-900 text-center leading-tight min-w-[170px] max-w-[220px]" style={{boxShadow: '0 4px 16px rgba(0,0,0,0.12)'}}>
                YOUR DAILY TARGETS:<br />
                <span className="text-base font-bold">{jobCompleted} JOB APPLICATION{jobCompleted !== 1 ? 'S' : ''} +<br />{leetcodeCompleted} LEETCODE PROBLEM{leetcodeCompleted !== 1 ? 'S' : ''}</span>
                {/* Speech bubble tail */}
                <div className="absolute bottom-0 right-8 translate-y-full">
                  <div className="relative">
                    <div className="w-4 h-4 bg-white rounded-full -mt-2"></div>
                    <div className="w-3 h-3 bg-white rounded-full -mt-1 ml-2"></div>
                  </div>
                </div>
              </div>
            </div>
            <div className="mb-2 flex items-center gap-3">
              <img src="/assets/images/bluelever.png" alt="blue lever" className="w-12 h-10 md:w-16 md:h-12" />
              <div className="flex-1">
                <ProgressTrack
                  title="JOBLAND ADVENTURES"
                  icon="briefcase"
                  color="blue"
                  completed={jobCompleted}
                  total={5}
                  avatarImage="/assets/images/joyicon.png"
                  showTarget={false}
                />
                <input
                  type="range"
                  min={0}
                  max={5}
                  value={jobCompleted}
                  onChange={e => setJobCompleted(Number(e.target.value))}
                  className="w-full accent-blue-500 mt-4"
                />
              </div>
            </div>
            <div className="flex items-center gap-3">
              <img src="/assets/images/greenlever.png" alt="green lever" className="w-12 h-10 md:w-16 md:h-12" />
              <div className="flex-1">
                <ProgressTrack
                  title="LEETCODE CHALLENGES"
                  icon="code"
                  color="green"
                  completed={leetcodeCompleted}
                  total={5}
                  avatarImage="/assets/images/disgusticon.png"
                />
                <input
                  type="range"
                  min={0}
                  max={5}
                  value={leetcodeCompleted}
                  onChange={e => setLeetcodeCompleted(Number(e.target.value))}
                  className="w-full accent-green-500 mt-4"
                />
              </div>
            </div>
          </div>
          <div className="flex gap-4 items-center mt-4">
            <button
              className="px-16 py-5 bg-gradient-to-b from-[#4fc3f7] to-[#1976d2] hover:from-[#1976d2] hover:to-[#4fc3f7] text-white text-3xl font-extrabold rounded-full shadow-2xl border-4 border-blue-200 transition-all focus:outline-none focus:ring-4 focus:ring-blue-300 flex items-center gap-4 tracking-wide"
              style={{ textShadow: '0 2px 8px #1976d2, 0 1px 0 #fff' }}
              onClick={handleActivateGoals}
            >
              <span role="img" aria-label="brain" className="text-4xl">🧠</span> ACTIVATE GOALS
            </button>
            <button
              className="px-6 py-4 bg-gradient-to-b from-[#ffd600] to-[#ff9800] hover:from-[#ff9800] hover:to-[#ffd600] text-white text-xl font-bold rounded-full shadow-xl border-2 border-yellow-300 transition-all focus:outline-none focus:ring-4 focus:ring-yellow-300 flex items-center gap-2"
              onClick={() => fileInputRef.current?.click()}
              type="button"
            >
              <span role="img" aria-label="upload" className="text-2xl">📄</span> Upload Resume
            </button>
            <input
              ref={fileInputRef}
              type="file"
              accept="application/pdf"
              style={{ display: 'none' }}
              onChange={handleResumeUpload}
            />
            {resumeFile && <span className="ml-2 text-green-700 font-semibold">{resumeFile.name}</span>}
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobOnboardingPage;
