import React, { useState } from 'react';
import { format, differenceInDays } from 'date-fns';
import { api } from '../services/api';

interface RelapseTrackerProps {
  initialQuitDate: Date;
  lastRelapseDate?: Date;
  totalSoberDays: number;
  longestStreak: number;
  goalId: number;
  onRelapse: (date: Date, notes: string) => void;
}

export const RelapseTracker = ({
  initialQuitDate,
  lastRelapseDate,
  totalSoberDays,
  longestStreak,
  goalId,
  onRelapse,
}: RelapseTrackerProps) => {
  const [showRelapseForm, setShowRelapseForm] = useState(false);
  const [notes, setNotes] = useState('');
  const [relapseDate, setRelapseDate] = useState(new Date());
  const [error, setError] = useState('');

  const currentStreak = lastRelapseDate 
    ? differenceInDays(new Date(), lastRelapseDate)
    : differenceInDays(new Date(), initialQuitDate);

  const handleRelapseSubmit = async () => {
    try {
      await api.recordRelapse(Number(goalId), relapseDate, notes);
      onRelapse(relapseDate, notes);
      setShowRelapseForm(false);
      setNotes('');
    } catch (error) {
      setError('Failed to record relapse. Please try again.');
    }
  };

  return (
    <div className="recovery-tracker">
      <div className="stats-container">
        <div className="stat-card">
          <h3>Journey Started</h3>
          <p>{format(initialQuitDate, 'MMM dd, yyyy')}</p>
        </div>
        <div className="stat-card">
          <h3>Current Streak</h3>
          <p>{currentStreak} days</p>
        </div>
        <div className="stat-card">
          <h3>Total Sober Days</h3>
          <p>{totalSoberDays} days</p>
        </div>
        <div className="stat-card">
          <h3>Longest Streak</h3>
          <p>{longestStreak} days</p>
        </div>
      </div>

      {!showRelapseForm ? (
        <button 
          className="relapse-button"
          onClick={() => setShowRelapseForm(true)}
        >
          Record a Relapse
        </button>
      ) : (
        <div className="relapse-form">
          <h4>Record Relapse</h4>
          <input
            type="date"
            value={format(relapseDate, 'yyyy-MM-dd')}
            onChange={(e) => setRelapseDate(new Date(e.target.value))}
          />
          <textarea
            placeholder="What triggered this relapse? (optional)"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />
          <div className="button-group">
            <button onClick={handleRelapseSubmit}>Submit</button>
            <button onClick={() => setShowRelapseForm(false)}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
}; 