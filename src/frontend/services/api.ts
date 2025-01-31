import axios from 'axios';

interface TrackingData {
  id?: number;
  date: Date;
  consumption_amount: number;
  money_saved: number;
  associated_habits: Record<string, number>;
  mood_score?: number;
  triggers_encountered?: Record<string, string>;
  coping_strategies_used?: Record<string, boolean>;
}

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

interface Api {
  recordRelapse: (goalId: number, date: Date, notes: string) => Promise<void>;
  getGoalStats: (goalId: number) => Promise<any>;
  getDashboardData: (userId: number) => Promise<any>;
  updateTracking: (trackingData: TrackingData) => Promise<any>;
  getRecoveryPlan: () => Promise<any>;
}

export const api: Api = {
  async recordRelapse(goalId: number, date: Date, notes: string): Promise<void> {
    try {
      const response = await axios.post(`${API_URL}/relapses/`, {
        goal_id: goalId,
        last_relapse_date: date,
        notes
      });
      return response.data;
    } catch (error) {
      console.error('Error recording relapse:', error);
      throw error;
    }
  },

  async getGoalStats(goalId: number) {
    try {
      const response = await axios.get(`${API_URL}/goals/${goalId}/stats`);
      return response.data;
    } catch (error) {
      console.error('Error fetching goal stats:', error);
      throw error;
    }
  },

  async getDashboardData(userId: number) {
    return axios.get(`${API_URL}/dashboard/${userId}`);
  },
  
  async updateTracking(trackingData: TrackingData) {
    return axios.post(`${API_URL}/tracking`, trackingData);
  },
  
  async getRecoveryPlan() {
    return axios.get(`${API_URL}/recovery-plan`);
  }
}; 