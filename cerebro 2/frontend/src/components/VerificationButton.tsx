/**
 * Verification Button component - Check progress and award orbs
 */
'use client';

import React, { useState } from 'react';
import { api, VerificationResult } from '@/services/api';
import { CheckCircle, Loader, Sparkles } from 'lucide-react';

interface VerificationButtonProps {
  userId?: string;
  onVerificationComplete?: (result: VerificationResult) => void;
}

const VerificationButton: React.FC<VerificationButtonProps> = ({ 
  userId = 'demo_user',
  onVerificationComplete 
}) => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<VerificationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleVerify = async () => {
    try {
      setLoading(true);
      setError(null);
      const verificationResult = await api.checkProgress(userId, 24);
      setResult(verificationResult);
      if (onVerificationComplete) {
        onVerificationComplete(verificationResult);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to check progress');
      console.error('Verification error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <button
        onClick={handleVerify}
        disabled={loading}
        className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-semibold py-3 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
      >
        {loading ? (
          <>
            <Loader className="w-5 h-5 animate-spin" />
            Checking Progress...
          </>
        ) : (
          <>
            <CheckCircle className="w-5 h-5" />
            Check Progress (Morning Routine)
          </>
        )}
      </button>

      {error && (
        <div className="bg-red-100 dark:bg-red-900 border border-red-400 dark:border-red-700 text-red-700 dark:text-red-200 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {result && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 space-y-4">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-yellow-500" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Verification Results
            </h3>
          </div>

          {/* Progress Stats */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3">
              <div className="text-sm text-gray-600 dark:text-gray-400">Applications</div>
              <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                {result.verification.apps_sent}/{result.verification.apps_target}
              </div>
            </div>
            <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-3">
              <div className="text-sm text-gray-600 dark:text-gray-400">LeetCode</div>
              <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                {result.verification.leetcode_done ? '✓' : '✗'}
              </div>
            </div>
          </div>

          {/* Orbs Awarded */}
          <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
            <div className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              Orbs Awarded:
            </div>
            <div className="flex gap-4">
              {result.orbs_awarded.gold > 0 && (
                <div className="flex items-center gap-2">
                  <span className="text-yellow-600 dark:text-yellow-400 font-bold">
                    {result.orbs_awarded.gold}
                  </span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">Gold</span>
                </div>
              )}
              {result.orbs_awarded.blue > 0 && (
                <div className="flex items-center gap-2">
                  <span className="text-blue-600 dark:text-blue-400 font-bold">
                    {result.orbs_awarded.blue}
                  </span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">Blue</span>
                </div>
              )}
              {result.orbs_awarded.red > 0 && (
                <div className="flex items-center gap-2">
                  <span className="text-red-600 dark:text-red-400 font-bold">
                    {result.orbs_awarded.red}
                  </span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">Red</span>
                </div>
              )}
              {result.orbs_awarded.gold === 0 && result.orbs_awarded.blue === 0 && result.orbs_awarded.red === 0 && (
                <span className="text-sm text-gray-500">No orbs awarded</span>
              )}
            </div>
          </div>

          {/* Agent Messages */}
          {result.messages && (
            <div className="border-t border-gray-200 dark:border-gray-700 pt-4 space-y-2">
              {result.messages.joy && (
                <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-3">
                  <div className="text-sm font-semibold text-yellow-800 dark:text-yellow-200 mb-1">
                    Joy:
                  </div>
                  <div className="text-sm text-yellow-700 dark:text-yellow-300">
                    {result.messages.joy}
                  </div>
                </div>
              )}
              {result.messages.sadness && (
                <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3">
                  <div className="text-sm font-semibold text-blue-800 dark:text-blue-200 mb-1">
                    Sadness:
                  </div>
                  <div className="text-sm text-blue-700 dark:text-blue-300">
                    {result.messages.sadness}
                  </div>
                </div>
              )}
              {result.messages.logic && (
                <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
                  <div className="text-sm font-semibold text-gray-800 dark:text-gray-200 mb-1">
                    Logic:
                  </div>
                  <div className="text-sm text-gray-700 dark:text-gray-300">
                    {result.messages.logic}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Completion Rate */}
          <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
            <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">
              Overall Completion Rate
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-4">
              <div
                className="bg-green-600 h-4 rounded-full transition-all duration-500"
                style={{ width: `${result.verification.completion_rate * 100}%` }}
              />
            </div>
            <div className="text-right text-sm font-semibold text-gray-700 dark:text-gray-300 mt-1">
              {Math.round(result.verification.completion_rate * 100)}%
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default VerificationButton;
