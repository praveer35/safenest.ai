import React from 'react';
import './Dashboard.css';
import { useNavigate } from 'react-router-dom';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Perform any logout logic here, then navigate to login page
    navigate('/login');
  };

  return (
    <div className="dashboard-page">
      <nav className="navbar">
        <div className="navbar-left">
          <span className="project-name">SafeNet.AI</span>
        </div>
        <div className="navbar-center">
          <span className="dashboard-title">Dashboard</span>
        </div>
        <div className="navbar-right">
          <button className="navbar-button" onClick={() => navigate('/summary')}>
            Summary
          </button>
          <button className="navbar-button" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </nav>
      <div className="dashboard-content">
        {/* Space for future content */}
      </div>
    </div>
  );
};

export default Dashboard;
