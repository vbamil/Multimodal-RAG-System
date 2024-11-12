// File: src/components/UploadForm.js

import React, { useState } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import { Typography, Button, LinearProgress, Box } from '@mui/material';
import './UploadForm.css';

const UploadForm = ({ onUploadSuccess, onUploadError }) => {
    const [file, setFile] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [uploadProgress, setUploadProgress] = useState(0);

    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files.length > 0) {
            setFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) {
            onUploadError("Please select a file to upload.");
            return;
        }

        const allowedTypes = [
            'application/pdf',
            'text/plain',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        ];
        if (!allowedTypes.includes(file.type)) {
            onUploadError("Unsupported file type. Please upload a .txt, .pdf, or .docx file.");
            return;
        }

        setIsLoading(true);
        onUploadError(null);
        setUploadProgress(0);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post(`${API_BASE_URL}/api/upload`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                onUploadProgress: (progressEvent) => {
                    const percentCompleted = Math.round(
                        (progressEvent.loaded * 100) / progressEvent.total
                    );
                    setUploadProgress(percentCompleted);
                },
            });

            setUploadProgress(100);
            onUploadSuccess(response.data);
        } catch (error) {
            console.error("Upload Error:", error);
            if (error.response) {
                // Server responded with a status other than 2xx
                onUploadError(
                    `Error ${error.response.status}: ${
                        error.response.data.detail || 'An error occurred.'
                    }`
                );
            } else if (error.request) {
                // Request was made but no response received
                onUploadError('No response from server. Please try again later.');
            } else {
                // Something else caused the error
                onUploadError('An unexpected error occurred.');
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Box sx={{ mt: 4, mb: 4, textAlign: 'center' }} className="upload-form">
            <Typography variant="h6" gutterBottom>
                📁 Upload Your Document
            </Typography>
            <Button variant="contained" component="label" sx={{ mb: 2 }}>
                Choose File
                <input type="file" hidden onChange={handleFileChange} accept=".txt,.pdf,.docx" />
            </Button>
            {file && (
                <Typography variant="body1" gutterBottom>
                    Selected File: {file.name}
                </Typography>
            )}
            {/* Conditionally render the Upload button only if a file is selected */}
            {file && (
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleUpload}
                    disabled={isLoading}
                >
                    {isLoading ? 'Uploading...' : 'Upload'}
                </Button>
            )}
            {isLoading && (
                <Box sx={{ width: '100%', mt: 2 }}>
                    <LinearProgress variant="determinate" value={uploadProgress} />
                    <Typography variant="body2" color="textSecondary">
                        Uploading: {uploadProgress}%
                    </Typography>
                </Box>
            )}
        </Box>
    );
};

UploadForm.propTypes = {
    onUploadSuccess: PropTypes.func.isRequired,
    onUploadError: PropTypes.func.isRequired,
};

export default UploadForm;
