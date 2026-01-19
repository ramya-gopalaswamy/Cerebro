/**
 * Dashboard component - Main user interface
 */
'use client';

import React, { useState, useEffect } from 'react';
import { api, Task, DailyTarget, OrbInventory } from '@/services/api';
import OrbJar from './OrbJar';
import TaskList from './TaskList';
import SetupForm from './SetupForm';
import VerificationButton from './VerificationButton';
import { RefreshCw, CheckCircle, Calendar } from 'lucide-react';
import { VerificationResult } from '@/services/api';

interface DashboardProps {
  userId?: string;
}

const Dashboard: React.FC<DashboardProps> = ({ userId = 'demo_user' }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [dailyTarget, setDailyTarget] = useState<DailyTarget>({ apps: 3, leetcode: 1 });
  const [orbInventory, setOrbInventory] = useState<OrbInventory>({ gold: 0, blue: 0, red: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [generating, setGenerating] = useState(false);
  const [needsSetup, setNeedsSetup] = useState(false);

  useEffect(() => {
    loadDashboardData();
  }, [userId]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getTodayTasks(userId);
      setTasks(data.tasks || []);
      setDailyTarget(data.daily_target || { apps: 3, leetcode: 1 });
      setOrbInventory(data.orb_inventory || { gold: 0, blue: 0, red: 0 });
      setNeedsSetup(false);
    } catch (err: any) {
      // Check if it's a 404 (user not found) - needs setup
      if (err.response?.status === 404 || err.response?.data?.detail?.includes('not found')) {
        setNeedsSetup(true);
        setError(null);
      } else {
        setError('Failed to load dashboard data. Please try again.');
        console.error('Dashboard load error:', err);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSetupComplete = () => {
    setNeedsSetup(false);
    loadDashboardData();
  };

  const handleGenerateTasks = async () => {
    try {
      setGenerating(true);
      setError(null);
      const data = await api.generateTasks('frontend developer', userId);
      setTasks(data.tasks || []);
      await loadDashboardData(); // Reload to get updated inventory
    } catch (err) {
      setError('Failed to generate tasks');
      console.error('Generate tasks error:', err);
    } finally {
      setGenerating(false);
    }
  };

  const handleResetTasks = async () => {
    try {
      setGenerating(true);
      setError(null);
      const data = await api.resetTasks(userId);
      setTasks(data.today_tasks || []);
      await loadDashboardData();
    } catch (err) {
      setError('Failed to reset tasks');
      console.error('Reset tasks error:', err);
    } finally {
      setGenerating(false);
    }
  };

  const handleVerificationComplete = async (result: VerificationResult) => {
    // Reload dashboard to show updated orb inventory
    await loadDashboardData();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-4 text-blue-500" />
          <p className="text-gray-600 dark:text-gray-400">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  // Show setup form if user hasn't been set up
  if (needsSetup) {
    return <SetupForm userId={userId} onSetupComplete={handleSetupComplete} />;
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-transparent py-8 px-4">
      <div className="w-full max-w-3xl rounded-2xl p-8 bg-white/10 backdrop-blur-md border-2 border-blue-200/40 shadow-2xl relative">
        <h1 className="text-4xl font-extrabold text-center text-white drop-shadow mb-8 tracking-wide">
          SET DAILY CORE MEMORIES
        </h1>
        <div className="flex flex-col gap-12">
          {/* Jobland Adventures */}
          <div className="flex flex-col items-center">
            <span className="text-xl font-bold text-blue-200 mb-2 tracking-wide">JOBLAND ADVENTURES</span>
            <div className="flex items-center gap-4">
              <div className="w-10 h-32 bg-blue-400 rounded-full flex items-end justify-center relative mr-4">
                <div className="w-8 h-16 bg-blue-200 rounded-b-full absolute bottom-0 left-1/2 -translate-x-1/2 border-4 border-blue-500"></div>
              </div>
              <div className="flex items-center gap-2">
                {[1,2,3,4,5].map((n) => (
                  <div key={n} className={`w-16 h-16 rounded-lg border-4 ${n <= dailyTarget.apps ? 'border-blue-400 bg-blue-200/80' : 'border-blue-200 bg-blue-100/30'} flex items-center justify-center text-2xl font-bold text-blue-700 relative`}>
                    <span className="drop-shadow">{n <= dailyTarget.apps ? n : ''}</span>
                    {n === dailyTarget.apps && (
                      <span className="absolute -top-6 right-0 text-3xl">😃</span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
          {/* Leetcode Challenges */}
          <div className="flex flex-col items-center">
            <span className="text-xl font-bold text-green-200 mb-2 tracking-wide">LEETCODE CHALLENGES</span>
            <div className="flex items-center gap-4">
              <div className="w-10 h-32 bg-green-400 rounded-full flex items-end justify-center relative mr-4">
                <div className="w-8 h-8 bg-green-200 rounded-b-full absolute bottom-0 left-1/2 -translate-x-1/2 border-4 border-green-500"></div>
              </div>
              <div className="flex items-center gap-2">
                {[1,2,3,4,5].map((n) => (
                  <div key={n} className={`w-16 h-16 rounded-lg border-4 ${n <= dailyTarget.leetcode ? 'border-green-400 bg-green-200/80' : 'border-green-200 bg-green-100/30'} flex items-center justify-center text-2xl font-bold text-green-700 relative`}>
                    <span className="drop-shadow">{n <= dailyTarget.leetcode ? n : ''}</span>
                    {n === dailyTarget.leetcode && (
                      <span className="absolute -top-6 right-0 text-3xl">😒</span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
          {/* Daily Targets Speech Bubble */}
          <div className="flex justify-center mt-4">
            <div className="bg-white/80 rounded-2xl px-8 py-4 shadow-lg border-2 border-blue-200 text-xl font-bold text-gray-800 relative">
              <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-3xl">💬</span>
              YOUR DAILY TARGETS: <span className="text-blue-700">{dailyTarget.apps} JOB APPLICATIONS</span> + <span className="text-green-700">{dailyTarget.leetcode} LEETCODE PROBLEM</span>
            </div>
          </div>
          {/* Activate Goals Button */}
          <div className="flex justify-center mt-8">
            <button
              className="bg-blue-500 hover:bg-blue-600 text-white text-2xl font-bold py-4 px-12 rounded-full shadow-lg flex items-center gap-4 border-4 border-blue-200/60 transition-all duration-200"
              onClick={handleGenerateTasks}
              disabled={generating}
            >
              <span role="img" aria-label="brain">🧠</span> ACTIVATE GOALS
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
