/**
 * API client for backend communication
 */
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8003';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types
export interface DailyTarget {
  apps: number;
  leetcode: number;
}

export interface Task {
  id: string;
  type: 'job' | 'leetcode';
  title: string;
  url?: string;
  description?: string;
  created_at: string;
  completed: boolean;
  completed_at?: string;
}

export interface OrbInventory {
  gold: number;
  blue: number;
  red: number;
}

export interface UserState {
  user_id: string;
  daily_target: DailyTarget;
  created_at: string;
  updated_at: string;
  today_tasks: Task[];
  orb_inventory: OrbInventory;
  task_history_count: number;
}

export interface VerificationResult {
  verification: {
    apps_sent: number;
    apps_target: number;
    leetcode_done: boolean;
    leetcode_target: number;
    completion_rate: number;
  };
  orbs_awarded: OrbInventory;
  orb_inventory: OrbInventory;
  messages: {
    joy?: string;
    sadness?: string;
    logic?: string;
    orb_messages?: Record<string, string>;
  };
  analysis: {
    apps_completion: number;
    leetcode_completion: number;
    overall_completion: number;
    insights: string[];
    recommendations: string[];
  };
}

// API functions
export const api = {
  // Health check
  health: async () => {
    const response = await apiClient.get('/api/health');
    return response.data;
  },

  // Setup
  setup: async (dailyTarget: DailyTarget, userId: string = 'demo_user') => {
    try {
      const response = await apiClient.post(
        `/api/setup/?user_id=${encodeURIComponent(userId)}`,
        { daily_target: dailyTarget },
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      return response.data;
    } catch (error: any) {
      console.error('Setup API error:', error);
      if (error.response) {
        throw new Error(error.response.data?.detail || error.response.data?.message || 'Setup failed');
      }
      throw error;
    }
  },

  // Tasks
  getTodayTasks: async (userId: string = 'demo_user') => {
    const response = await apiClient.get('/api/tasks/today', {
      params: { user_id: userId },
    });
    return response.data;
  },

  generateTasks: async (keywords: string = 'frontend developer', userId: string = 'demo_user') => {
    const response = await apiClient.post('/api/tasks/generate', null, {
      params: { keywords, user_id: userId },
    });
    return response.data;
  },

  resetTasks: async (userId: string = 'demo_user') => {
    const response = await apiClient.post('/api/tasks/reset', null, {
      params: { user_id: userId },
    });
    return response.data;
  },

  // Verification
  checkProgress: async (userId: string = 'demo_user', timeframeHours: number = 24) => {
    const response = await apiClient.get('/api/verification/check-progress', {
      params: { user_id: userId, timeframe_hours: timeframeHours },
    });
    return response.data as VerificationResult;
  },

  // Insights
  getWeeklyInsights: async (userId: string = 'demo_user') => {
    const response = await apiClient.get('/api/insights/weekly', {
      params: { user_id: userId },
    });
    return response.data;
  },

  // War Room
  makeDecision: async (question: string, context?: string, userId: string = 'demo_user') => {
    const response = await apiClient.post('/api/war-room/decide', {
      question,
      context,
    }, {
      params: { user_id: userId },
    });
    return response.data;
  },

  // User registration
  register: async (email: string, password: string) => {
    const response = await apiClient.post('/api/auth/register', { email, password });
    return response.data;
  },

  // User login
  login: async (email: string, password: string) => {
    const response = await apiClient.post('/api/auth/login', { email, password });
    return response.data;
  },

  // User profile fetch with JWT
  getProfile: async (token: string) => {
    const response = await apiClient.get('/api/auth/profile', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  },

  // Fetch motivational image from Freepik
  getMotivationalImage: async (query: string = 'motivation') => {
    const response = await apiClient.get('/api/motivation-image', {
      params: { query },
    });
    return response.data as { image_url: string | null; title: string };
  },
};

export default api;
