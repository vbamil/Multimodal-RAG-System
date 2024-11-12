// src/components/QueryInput.js
import React, { useState } from 'react';

const QueryInput = ({ onSubmit }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() === '') return;
    onSubmit(query);
    setQuery('');
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter your query..."
        required
        style={styles.input}
      />
      <button type="submit" style={styles.button}>Ask</button>
    </form>
  );
};

const styles = {
  form: {
    display: 'flex',
    justifyContent: 'center',
    margin: '20px 0',
  },
  input: {
    width: '60%',
    padding: '10px',
    fontSize: '16px',
    border: '1px solid #ccc',
    borderRadius: '4px 0 0 4px',
    outline: 'none',
  },
  button: {
    padding: '10px 20px',
    fontSize: '16px',
    border: 'none',
    backgroundColor: '#4CAF50',
    color: 'white',
    cursor: 'pointer',
    borderRadius: '0 4px 4px 0',
  },
};

export default QueryInput;
