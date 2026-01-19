/**
 * Setup Form component - Initial user configuration
 */
'use client';

import React, { useState } from 'react';
import { api, DailyTarget } from '@/services/api';
import { Target, Briefcase, Code, Loader } from 'lucide-react';

interface SetupFormProps {
  userId?: string;
  onSetupComplete: () => void;
}

const SetupForm: React.FC<SetupFormProps> = ({ userId = 'demo_user', onSetupComplete }) => {
  const [apps, setApps] = useState(3);
  const [leetcode, setLeetcode] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const dailyTarget: DailyTarget = {
        apps: parseInt(apps.toString()),
        leetcode: parseInt(leetcode.toString()),
      };

      const result = await api.setup(dailyTarget, userId);
      console.log('Setup successful:', result);
      onSetupComplete();
    } catch (err: any) {
      const errorMessage = err.message || err.response?.data?.detail || 'Failed to complete setup. Please try again.';
      setError(errorMessage);
      console.error('Setup error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center py-12 px-4">
      <div className="max-w-md w-full bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 dark:bg-blue-900 rounded-full mb-4">
            <Target className="w-8 h-8 text-blue-600 dark:text-blue-400" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Welcome to Cerebro
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Set your daily targets to get started
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Job Applications Target */}
          <div>
            <label className="flex items-center gap-2 text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              <Briefcase className="w-4 h-4 text-blue-500" />
              Job Applications per Day
            </label>
            <div className="flex items-center gap-4">
              <input
                type="range"
                min="0"
                max="10"
                value={apps}
                onChange={(e) => setApps(parseInt(e.target.value))}
                className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
              />
              <div className="w-16 text-center">
                <span className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                  {apps}
                </span>
              </div>
            </div>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              How many job applications do you want to send daily?
            </p>
          </div>

          {/* LeetCode Problems Target */}
          <div>
            <label className="flex items-center gap-2 text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              <Code className="w-4 h-4 text-green-500" />
              LeetCode Problems per Day
            </label>
            <div className="flex items-center gap-4">
              <input
                type="range"
                min="0"
                max="5"
                value={leetcode}
                onChange={(e) => setLeetcode(parseInt(e.target.value))}
                className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
              />
              <div className="w-16 text-center">
                <span className="text-2xl font-bold text-green-600 dark:text-green-400">
                  {leetcode}
                </span>
              </div>
            </div>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              How many coding problems do you want to solve daily?
            </p>
          </div>

          {/* Summary */}
          <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4">
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
              Your daily targets:
            </p>
            <div className="flex items-center justify-between">
              <span className="text-gray-700 dark:text-gray-300">
                {apps} job application{apps !== 1 ? 's' : ''}
              </span>
              <span className="text-gray-400">+</span>
              <span className="text-gray-700 dark:text-gray-300">
                {leetcode} LeetCode problem{leetcode !== 1 ? 's' : ''}
              </span>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-100 dark:bg-red-900 border border-red-400 dark:border-red-700 text-red-700 dark:text-red-200 px-4 py-3 rounded">
              {error}
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading || (apps === 0 && leetcode === 0)}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-semibold py-3 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader className="w-5 h-5 animate-spin" />
                Setting up...
              </>
            ) : (
              <>
                <Target className="w-5 h-5" />
                Start Tracking
              </>
            )}
          </button>

          {apps === 0 && leetcode === 0 && (
            <p className="text-xs text-center text-gray-500 dark:text-gray-400">
              Please set at least one target to continue
            </p>
          )}
        </form>
      </div>
    </div>
  );
};

export default SetupForm;
