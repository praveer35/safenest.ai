import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import Dashboard from './components/Dashboard';
import Charter from './components/Charter';
import Summary from './components/Summary';
import SignUpPage from './components/SignUpPage';
import VideoUpload from './components/VideoUpload';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/signup" element={<SignUpPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/charter" element = {<Charter />} />
        <Route path="/summary" element = {<Summary />} />
        <Route path="/videoupload" element={<VideoUpload />} />
      </Routes>
    </Router>
  );
}

export default App;