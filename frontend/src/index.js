// File: src/index.js

import React from 'react';
import ReactDOM from 'react-dom/client'; // Updated import
import App from './App';
import CssBaseline from '@mui/material/CssBaseline';

const container = document.getElementById('root');
const root = ReactDOM.createRoot(container); // Create root

root.render(
  <React.StrictMode>
    <CssBaseline />
    <App />
  </React.StrictMode>
);
