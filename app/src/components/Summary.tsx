import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Dashboard.css'; // Reusing the existing Dashboard CSS
import { useNavigate } from 'react-router-dom';

const Summary: React.FC = () => {
  const [script, setScript] = useState<string>('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchScript = async () => {
      try {
        const response = await axios.get('http://localhost:1601/summary');
        setScript(response.data.script);
      } catch (error) {
        console.error('Error fetching script:', error);
      }
    };

    fetchScript();
  }, []);

  const handleLogout = () => {
    navigate('/');
  };

  return (
    <div className="dashboard-page">
      <nav className="navbar">
        <div className="navbar-left">
          <span className="project-name">SafeNet.AI</span>
        </div>
        <div className="navbar-center">
          <span className="dashboard-title"><strong>Summary</strong></span>
        </div>
        <div className="navbar-right">
          <button className="navbar-button" onClick={() => navigate('/dashboard')}>
            Dashboard
          </button>
          <button className="navbar-button" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </nav>
      <div className="dashboard-content">
        <pre>{script}</pre>
      </div>
    </div>
  );
};

export default Summary;