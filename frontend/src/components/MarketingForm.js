import React, { useState } from 'react';
import { Send } from 'lucide-react';
import axios from 'axios';

const AGENT_OPTIONS = [
  { value: 'market_research', label: 'Market Research', color: '#3b82f6' },
  { value: 'marketing_strategy', label: 'Marketing Strategy', color: '#10b981' },
  { value: 'content_delivery', label: 'Content Delivery', color: '#f59e0b' }
];

function MarketingForm({ onAnalysisComplete, setLoading, loading }) {
  const [query, setQuery] = useState('');
  const [selectedAgents, setSelectedAgents] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    setLoading(true);
    
    try {
      const payload = {
        query: query.trim(),
        ...(selectedAgents.length > 0 && { specific_agents: selectedAgents })
      };

      const response = await axios.post('/analyze', payload);
      onAnalysisComplete(response.data);
      
      setQuery('');
      setSelectedAgents([]);
      
    } catch (error) {
      console.error('Error analyzing request:', error);
      alert('Failed to analyze request. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleAgentChange = (agentValue, checked) => {
    if (checked) {
      setSelectedAgents(prev => [...prev, agentValue]);
    } else {
      setSelectedAgents(prev => prev.filter(agent => agent !== agentValue));
    }
  };

  return (
    <form onSubmit={handleSubmit} className="marketing-form">
      <div className="form-group">
        <label htmlFor="query" className="form-label">
          Marketing Query
        </label>
        <textarea
          id="query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Describe your marketing needs... (e.g., 'I'm launching a new fitness app and need market research and content ideas')"
          className="form-textarea"
          required
          minLength={10}
          maxLength={1000}
        />
        <div className="char-count">
          {query.length}/1000 characters
        </div>
      </div>

      <div className="form-group">
        <label className="form-label">
          Specific Agents (optional - leave empty for auto-routing)
        </label>
        <div className="agent-checkboxes">
          {AGENT_OPTIONS.map(agent => (
            <label key={agent.value} className="checkbox-item">
              <input
                type="checkbox"
                checked={selectedAgents.includes(agent.value)}
                onChange={(e) => handleAgentChange(agent.value, e.target.checked)}
                style={{ accentColor: agent.color }}
              />
              <span>{agent.label}</span>
            </label>
          ))}
        </div>
        {selectedAgents.length === 0 && (
          <div className="auto-route-note">
            ✨ Auto-routing enabled - AI will select the best agents for your query
          </div>
        )}
      </div>

      <button
        type="submit"
        disabled={!query.trim() || loading}
        className="submit-button"
      >
        {loading ? (
          <>
            <div className="loading-spinner"></div>
            Processing...
          </>
        ) : (
          <>
            <Send size={16} />
            Analyze Marketing Request
          </>
        )}
      </button>
    </form>
  );
}

export default MarketingForm; 