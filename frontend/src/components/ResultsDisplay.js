import React from 'react';
import { Clock, CheckCircle } from 'lucide-react';

function ResultsDisplay({ results }) {
  if (!results) return null;

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  const formatDuration = (seconds) => {
    return `${seconds.toFixed(1)}s`;
  };

  return (
    <div className="results-container">
      <div className="results-meta">
        <div>
          <div className="agents-used">
            {results.selected_agents.map(agent => (
              <span key={agent} className="agent-badge">
                {agent.replace('_', ' ')}
              </span>
            ))}
          </div>
        </div>
        <div className="meta-info">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
            <Clock size={12} />
            <span>{formatDuration(results.processing_time_seconds)}</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <CheckCircle size={12} />
            <span>{formatTimestamp(results.timestamp)}</span>
          </div>
        </div>
      </div>
      
      <div className="results-content">
        {results.formatted_output || 'No formatted output available'}
      </div>
      
      <div className="request-id">
        <small style={{ opacity: 0.6 }}>
          Request ID: {results.request_id}
        </small>
      </div>
    </div>
  );
}

export default ResultsDisplay; 