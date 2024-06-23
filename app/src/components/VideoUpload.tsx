import React, { useState } from 'react';
import axios from 'axios';
import './VideoUpload.css';
import Charter from './Charter';

const VideoUpload: React.FC = () => {
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

  return (
    <div className="video-upload">
      <h2>Upload a Video</h2>
      <form onSubmit={handleSubmit} className="upload-form">
        <label className="file-label">
          <span className="custom-file-input">Choose a file</span>
          <input type="file" accept="video/*" onChange={handleFileChange} />
        </label>
        <button type="submit">Upload</button>
      </form>
      {uploadStatus && <p>{uploadStatus}</p>}
      {isUploadSuccessful && <Charter />} {/* Conditionally render Charter */}
    </div>
  );
};

export default VideoUpload;
