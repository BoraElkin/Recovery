import React, { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { format } from 'date-fns';
import { api } from '../services/api';
import { RelapseTracker } from './RelapseTracker';
import { useGoalStats } from '../hooks/useGoalStats';
import '../styles/Dashboard.css';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface DashboardData {
  savings: number;
  streak: number;
  goalsProgress: Record<string, number>;
  consumptionTrends: Record<string, number>;
  lastRelapseDate?: Date;
  initialQuitDate: Date;
  longestStreak: number;
  goalId: number;
}

const Dashboard: React.FC = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const { stats: goalStats, loading: statsLoading } = useGoalStats();

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const response = await api.getDashboardData(0); // TODO: Replace with actual user ID
        setData(response.data);
      } catch (err) {
        setError('Failed to load dashboard data');
        console.error('Error fetching dashboard data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading || statsLoading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  if (!data) return <div className="no-data">No data available</div>;

  const chartData = {
    labels: Object.keys(data.consumptionTrends).map(date => 
      format(new Date(date), 'MMM d')
    ),
    datasets: [
      {
        label: 'Consumption Trends',
        data: Object.values(data.consumptionTrends),
        borderColor: '#4CAF50',
        backgroundColor: 'rgba(76, 175, 80, 0.1)',
        tension: 0.1,
        fill: true,
      }
    ]
  };

  const handleRelapse = async (date: Date, notes: string) => {
    try {
      await api.recordRelapse(data.goalId, date, notes);
      // Refresh dashboard data after recording relapse
      const response = await api.getDashboardData(0); // TODO: Replace with actual user ID
      setData(response.data);
    } catch (err) {
      console.error('Error recording relapse:', err);
      setError('Failed to record relapse');
    }
  };

  return (
    <div className="dashboard">
      <h2>Recovery Dashboard</h2>
      
      <div className="stats-container">
        <div className="stat-card">
          <h3>Money Saved</h3>
          <p>${data.savings.toFixed(2)}</p>
        </div>
        
        <div className="stat-card">
          <h3>Current Streak</h3>
          <p>{data.streak} days</p>
        </div>
        
        <div className="stat-card">
          <h3>Goals Progress</h3>
          <div className="progress-container">
            <div className="progress">
              <div 
                className="progress-bar"
                style={{ width: `${goalStats.progress}%` }}
              />
            </div>
            <span className="progress-text">{goalStats.progress}%</span>
          </div>
        </div>
      </div>

      <div className="charts-container">
        <div className="chart-card">
          <h3>Progress Over Time</h3>
          <Line 
            data={chartData}
            options={{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  position: 'top' as const,
                },
                title: {
                  display: true,
                  text: 'Consumption Trends'
                }
              },
              scales: {
                y: {
                  beginAtZero: true,
                  ticks: {
                    callback: (value) => `${value}%`
                  }
                }
              }
            }}
          />
        </div>
      </div>

      <RelapseTracker
        initialQuitDate={data.initialQuitDate}
        lastRelapseDate={data.lastRelapseDate}
        totalSoberDays={data.streak}
        longestStreak={data.longestStreak}
        goalId={data.goalId}
        onRelapse={handleRelapse}
      />
    </div>
  );
};

export default Dashboard; 