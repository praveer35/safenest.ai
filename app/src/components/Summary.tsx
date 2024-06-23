import React from 'react';
import './Dashboard.css'; // Reusing the existing Dashboard CSS

import { useNavigate } from 'react-router-dom';

const Summary: React.FC = () => {
  const navigate = useNavigate();

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
      </div>
    </div>
  );
};

export default Summary;
