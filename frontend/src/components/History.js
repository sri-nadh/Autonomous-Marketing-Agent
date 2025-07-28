import React from 'react';
import { History as HistoryIcon, Clock } from 'lucide-react';

function History({ history, onSelectResult }) {
  if (history.length === 0) return null;

  const formatTimeAgo = (timestamp) => {
    const now = new Date();
    const past = new Date(timestamp);
    const diffInMinutes = Math.floor((now - past) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
    return `${Math.floor(diffInMinutes / 1440)}d ago`;
  };

  const truncateText = (text, maxLength = 80) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  return (
    <>
      <div className="card-header">
        <HistoryIcon className="card-icon" />
        <h2>Recent Requests</h2>
      </div>
      <div className="history-list">
        {history.map((item, index) => (
          <div
            key={item.request_id || index}
            className="history-item"
            onClick={() => onSelectResult(item)}
            title="Click to view results"
          >
            <div className="history-query">
              {truncateText(item.query)}
            </div>
            <div className="history-meta">
              <div className="agents-used">
                {item.selected_agents.slice(0, 2).map(agent => (
                  <span key={agent} className="agent-badge" style={{ fontSize: '0.6rem' }}>
                    {agent.replace('_', ' ')}
                  </span>
                ))}
                {item.selected_agents.length > 2 && (
                  <span className="agent-badge" style={{ fontSize: '0.6rem' }}>
                    +{item.selected_agents.length - 2}
                  </span>
                )}
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                <Clock size={10} />
                <span>{formatTimeAgo(item.timestamp)}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}

export default History; 