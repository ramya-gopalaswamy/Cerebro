"use client";

import React, { useState, useEffect } from 'react';
import { ProgressTrack } from '@/components/ProgressTrack';
import { useRouter } from 'next/navigation';
import { useUser } from '@auth0/nextjs-auth0/client';
import { InformationCircleIcon, BookOpenIcon } from '@heroicons/react/24/outline';

const JobOnboardingPage = () => {
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [loadingData, setLoadingData] = useState(true);
  const [fetchError, setFetchError] = useState<string | null>(null);
  const [showInstructions, setShowInstructions] = useState(false);
  const router = useRouter();
  const { user, error, isLoading } = useUser();

  useEffect(() => {
    if (!user) return;
    setLoadingData(true);
    setFetchError(null);
    fetch(process.env.NEXT_PUBLIC_DASHBOARD_ROUTE || "/api/dashboard")
      .then(async (res) => {
        if (!res.ok) throw new Error("Failed to fetch dashboard data");
        const data = await res.json();
        setDashboardData(data);
        setLoadingData(false);
      })
      .catch((err) => {
        setFetchError(err.message);
        setLoadingData(false);
      });
  }, [user]);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>{error.message}</div>;
  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <a href="/api/auth/login" className="px-8 py-4 bg-blue-600 text-white rounded-lg text-2xl font-bold shadow-lg">Log In</a>
      </div>
    );
  }
  if (loadingData) return <div className="min-h-screen flex items-center justify-center">Loading dashboard...</div>;
  if (fetchError) return <div className="min-h-screen flex items-center justify-center text-red-600">{fetchError}</div>;

  // Fallbacks for demo if backend is not yet implemented
  const jars = dashboardData?.jars || [
    { color: 'yellow', progress: 0.7 },
    { color: 'blue', progress: 0.5 },
    { color: 'purple', progress: 0.3 },
    { color: 'red', progress: 0.1 },
  ];
  const leetcodeChallenge = dashboardData?.logicAgent?.challenge || 'Invert Binary Tree';
  const jobSources = dashboardData?.jobScout?.jobs || [];

  return (
    <>
      <div className="absolute top-4 right-4 z-50">
        <button
          aria-label="Show instructions"
          onClick={() => setShowInstructions(true)}
          className="bg-white/80 rounded-full p-2 shadow-lg hover:bg-blue-200 focus:outline-none"
        >
          <InformationCircleIcon className="h-8 w-8 text-blue-600" />
        </button>
      </div>
      <div className="absolute top-20 right-4 z-50">
        <button
          aria-label="Weekly Journal"
          onClick={() => router.push('/journal')}
          className="bg-white/80 rounded-full p-2 shadow-lg hover:bg-purple-200 focus:outline-none"
        >
          <BookOpenIcon className="h-8 w-8 text-purple-600" />
        </button>
      </div>
      {showInstructions && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-lg w-full relative">
            <button
              aria-label="Close instructions"
              onClick={() => setShowInstructions(false)}
              className="absolute top-4 right-4 text-gray-500 hover:text-gray-800"
            >
              ×
            </button>
            <h2 className="text-2xl font-extrabold mb-2 text-blue-700">OPERATIONAL PROTOCOL v1.0</h2>
            <h3 className="text-lg font-bold mb-4 text-gray-700">How to pilot the Cerebro System</h3>
            <div className="space-y-4 text-gray-800 text-base">
              <div>
                <span className="font-bold text-blue-600">Core Rule 1: The Silent Protocol</span>
                <ul className="list-disc ml-6">
                  <li>There are no checkboxes here. You cannot manually complete tasks.</li>
                  <li>Your job is to execute the orders externally (LinkedIn, LeetCode, Gmail).</li>
                </ul>
              </div>
              <div>
                <span className="font-bold text-blue-600">Core Rule 2: The Reality Check</span>
                <ul className="list-disc ml-6">
                  <li>Do not report back. The Agents are watching.</li>
                  <li>At 08:00 tomorrow, the Logic Agent will scan your LeetCode profile and the Gmail Agent will scan your 'Sent' folder.</li>
                </ul>
              </div>
              <div>
                <span className="font-bold text-blue-600">Core Rule 3: Memory Formation</span>
                <ul className="list-disc ml-6">
                  <li>If the Agents find proof of work, a GOLD ORB (Joy) is generated.</li>
                  <li>If no proof is found, a BLUE ORB (Sadness) is generated.</li>
                  <li>Your goal: Fill the core memory banks with Gold.</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}
      <div
        className="min-h-screen w-full flex flex-col items-center justify-start relative"
        style={{
          backgroundImage: "url('/assets/images/background2.png')",
          backgroundSize: "cover",
          backgroundPosition: "center",
          backgroundRepeat: "no-repeat"
        }}
      >
        {/* Sadness Ball on the left, move slightly right */}
        <img
          src="/assets/images/sadnessball.png"
          alt="Sadness Ball"
          className="hidden md:block absolute left-[17%] top-[38%] -translate-y-1/2 w-48 h-48"
          style={{ zIndex: 2 }}
        />
        {/* Joy on the right, move slightly left and reduce width */}
        <img
          src="/assets/images/joy.png"
          alt="Joy"
          className="hidden md:block absolute right-[17%] top-[38%] -translate-y-1/2 w-40 h-48"
          style={{ zIndex: 2 }}
        />
        <div className="pt-12 pb-2 flex flex-col items-center w-full">
          <h1 className="text-6xl md:text-7xl font-extrabold text-white tracking-wider mb-2 text-center drop-shadow-lg" style={{ letterSpacing: "0.06em" }}>
            <span className="text-yellow-300">HEAD</span><span className="text-white">QUARTERS</span>
          </h1>
          <div className="mt-2 mb-6">
            <span className="bg-green-400 text-white font-bold rounded-full px-6 py-2 text-lg shadow-lg">ALL SYSTEMS GO!</span>
          </div>
          <div className="flex gap-10 mb-6 items-end justify-center">
            {/* Jars Row - now dynamic */}
            {jars.map((jar: any, idx: number) => (
              <div className="flex flex-col items-center" key={jar.color}>
                <img src={`/assets/images/${jar.color}jar.png`} alt={`${jar.color} Jar`} className="w-28 md:w-32" />
                <div className="w-24 h-3 bg-gray-200 rounded-full mt-2">
                  <div
                    className={`h-3 rounded-full ${jar.color === 'yellow' ? 'bg-yellow-300' : jar.color === 'blue' ? 'bg-blue-400' : jar.color === 'purple' ? 'bg-purple-400' : 'bg-red-400'}`}
                    style={{ width: `${Math.round(jar.progress * 100)}%` }}
                  ></div>
                </div>
                <span className="text-white font-bold mt-1 text-sm">{Math.round(jar.progress * 100)}%</span>
              </div>
            ))}
          </div>
          <button className="bg-gradient-to-r from-blue-400 to-purple-400 text-white font-bold text-xl px-10 py-3 rounded-full shadow-lg mb-8 flex items-center gap-2 border-2 border-white" style={{ letterSpacing: "0.04em" }}>
            <span>⚡</span> COMMAND CENTER <span>⚡</span>
          </button>
          <div className="flex gap-8 mb-8">
            {/* Logic Agent Card */}
            <div className="bg-blue-500 bg-opacity-80 rounded-2xl p-6 shadow-2xl w-96 flex flex-col gap-4 border-2 border-blue-300" style={{ boxShadow: "0 0 32px 8px #4fc3f7" }}>
              <div className="flex items-center gap-2 mb-2">
                <span className="text-white text-xl font-bold">LOGIC AGENT</span>
                <span className="text-yellow-300 text-lg">• •</span>
              </div>
              <div className="bg-blue-300 bg-opacity-60 rounded-lg px-4 py-3 text-white font-semibold text-lg">
                LeetCode Challenge: <a href={dashboardData.logicAgent?.url} target="_blank" rel="noopener noreferrer" className="underline">{dashboardData.logicAgent?.challenge}</a>
              </div>
              <button className="bg-green-400 text-white font-bold rounded-lg px-4 py-3 text-lg shadow-md">&gt;_ OPEN TERMINAL</button>
            </div>
            {/* Job Scout Card */}
            <div className="bg-yellow-400 bg-opacity-90 rounded-2xl p-6 shadow-2xl w-96 flex flex-col gap-4 border-2 border-yellow-300 relative" style={{ boxShadow: "0 0 32px 8px #ffd600" }}>
              <div className="flex items-center gap-2 mb-2">
                <span className="text-white text-xl font-bold">JOB SCOUT</span>
                <span className="text-yellow-100 text-lg">🔍</span>
              </div>
              {jobSources.map((src: any) => (
                <button
                  key={src.name}
                  className={`bg-${src.color}-400 text-white font-bold rounded-lg px-4 py-3 text-lg shadow-md mb-2`}
                >
                  {src.name}
                </button>
              ))}
              <div className="bg-green-300 bg-opacity-60 rounded-lg px-4 py-3 text-white font-semibold text-lg mt-6">
                Job Scout:
                <ul className="mt-2 space-y-2">
                  {jobSources.length === 0 ? (
                    <li>No jobs found.</li>
                  ) : (
                    jobSources.map((job: any, idx: number) => (
                      <li key={job.id || idx}>
                        <a href={job.url} target="_blank" rel="noopener noreferrer" className="underline">
                          {job.title}
                        </a>
                        {job.company && <span className="ml-2 text-sm text-gray-200">({job.company})</span>}
                      </li>
                    ))
                  )}
                </ul>
              </div>
              <span className="absolute -top-6 -right-6 bg-yellow-200 rounded-full w-14 h-14 flex items-center justify-center border-4 border-white shadow-lg"><span className="text-3xl">🔍</span></span>
            </div>
          </div>
          <div className="flex gap-4 mt-2 mb-8">
            <div className="w-8 h-8 rounded-full bg-purple-400"></div>
            <div className="w-8 h-8 rounded-full bg-purple-400"></div>
            <div className="w-8 h-8 rounded-full bg-purple-400"></div>
          </div>
        </div>
      </div>
    </>
  );
};

export default JobOnboardingPage;
