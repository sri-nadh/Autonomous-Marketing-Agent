import React, { useState } from 'react';
import MarketingForm from './components/MarketingForm';
import ResultsDisplay from './components/ResultsDisplay';
import History from './components/History';
import { Brain, TrendingUp, Target, Zap } from 'lucide-react';
import './App.css';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const handleAnalysisComplete = (result) => {
    setResults(result);
    setHistory(prev => [result, ...prev.slice(0, 9)]); // Keep last 10
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <Brain className="logo-icon" />
            <h1>Marketing Agent</h1>
          </div>
          <p className="tagline">AI-powered marketing analysis with specialized agents</p>
        </div>
      </header>

      <main className="main-content">
        <div className="content-grid">
          <div className="primary-section">
            <div className="card">
              <div className="card-header">
                <Zap className="card-icon" />
                <h2>Marketing Analysis</h2>
              </div>
              <MarketingForm 
                onAnalysisComplete={handleAnalysisComplete}
                setLoading={setLoading}
                loading={loading}
              />
            </div>

            {results && (
              <div className="card">
                <div className="card-header">
                  <TrendingUp className="card-icon" />
                  <h2>Analysis Results</h2>
                </div>
                <ResultsDisplay results={results} />
              </div>
            )}
          </div>

          <div className="sidebar">
            <div className="card">
              <div className="card-header">
                <Target className="card-icon" />
                <h2>Available Agents</h2>
              </div>
              <div className="agents-list">
                <div className="agent-item">
                  <div className="agent-dot market-research"></div>
                  <div>
                    <h4>Market Research</h4>
                    <p>Industry analysis & competitor insights</p>
                  </div>
                </div>
                <div className="agent-item">
                  <div className="agent-dot marketing-strategy"></div>
                  <div>
                    <h4>Marketing Strategy</h4>
                    <p>Go-to-market & positioning strategies</p>
                  </div>
                </div>
                <div className="agent-item">
                  <div className="agent-dot content-delivery"></div>
                  <div>
                    <h4>Content Delivery</h4>
                    <p>Social media & viral content ideas</p>
                  </div>
                </div>
              </div>
            </div>

            {history.length > 0 && (
              <div className="card">
                <History history={history} onSelectResult={setResults} />
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App; 