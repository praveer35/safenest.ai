import React, { useState } from 'react';
import './Dashboard.css';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Charter from './Charter';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string>('');
  const [isUploadSuccessful, setIsUploadSuccessful] = useState<boolean>(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!selectedFile) {
      setUploadStatus('Please select a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('video', selectedFile);

    try {
      const response = await axios.post('http://localhost:1601/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      if (response.status === 200) {
        setUploadStatus('File uploaded successfully.');
        setIsUploadSuccessful(true);
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      setUploadStatus('Error uploading file.');
      setIsUploadSuccessful(false);
    }
  };

  const handleLogout = () => {
    // Perform any logout logic here, then navigate to login page
    navigate('/');
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
        <div className="video-upload">
          <h2>Upload a Video</h2>
          <form onSubmit={handleSubmit} className="upload-form">
            <input type="file" accept="video/*" onChange={handleFileChange} />
            <button type="submit">Upload</button>
          </form>
          {uploadStatus && <p>{uploadStatus}</p>}
          {isUploadSuccessful && <Charter />} {/* Conditionally render Charter */}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
