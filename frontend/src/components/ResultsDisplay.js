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

  const formatContent = (text) => {
    if (!text) return null;
    
    const lines = text.split('\n');
    const elements = [];
    let currentKey = 0;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line) continue;

      // Main heading (# )
      if (line.startsWith('# ')) {
        elements.push(
          <h1 key={currentKey++} className="result-h1">
            {line.substring(2)}
          </h1>
        );
      }
      // Sub heading (## )
      else if (line.startsWith('## ')) {
        elements.push(
          <h2 key={currentKey++} className="result-h2">
            {line.substring(3)}
          </h2>
        );
      }
      // Sub-sub heading (### )
      else if (line.startsWith('### ')) {
        elements.push(
          <h3 key={currentKey++} className="result-h3">
            {line.substring(4)}
          </h3>
        );
      }
      // Sub-sub-sub heading (#### )
      else if (line.startsWith('#### ')) {
        elements.push(
          <h4 key={currentKey++} className="result-h4">
            {line.substring(5)}
          </h4>
        );
      }
      // Bullet point (- )
      else if (line.startsWith('- ')) {
        const content = line.substring(2);
        const formattedContent = formatBoldText(content);
        elements.push(
          <div key={currentKey++} className="result-bullet">
            <span className="bullet-point">•</span>
            <span className="bullet-content">{formattedContent}</span>
          </div>
        );
      }
      // Regular paragraph
      else {
        const formattedContent = formatBoldText(line);
        elements.push(
          <p key={currentKey++} className="result-paragraph">
            {formattedContent}
          </p>
        );
      }
    }

    return elements;
  };

  const formatBoldText = (text) => {
    const parts = text.split(/(\*\*.*?\*\*)/);
    return parts.map((part, index) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return (
          <strong key={index} className="result-bold">
            {part.slice(2, -2)}
          </strong>
        );
      }
      return part;
    });
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
        {formatContent(results.formatted_output) || 'No formatted output available'}
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