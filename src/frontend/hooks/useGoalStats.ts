import { useState, useEffect } from 'react';
import { api } from '../services/api';

interface GoalStats {
  progress: number;
}

export const useGoalStats = () => {
  const [stats, setStats] = useState<GoalStats>({ progress: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch goal stats logic here
  }, []);

  return { stats, loading };
};