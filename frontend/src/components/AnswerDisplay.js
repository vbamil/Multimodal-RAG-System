// src/components/AnswerDisplay.js
import React from 'react';

const AnswerDisplay = ({ answer, sources }) => {
  if (!answer) return null;

  return (
    <div style={styles.container}>
      <h2>Answer:</h2>
      <p>{answer}</p>
      <h3>Sources:</h3>
      <ul>
        {sources.texts && sources.texts.map((text, index) => (
          <li key={index} style={styles.textSource}>{text}</li>
        ))}
        {sources.images && sources.images.map((img, index) => (
          <li key={index} style={styles.imageSource}>
            <img src={`data:image/jpeg;base64,${img}`} alt={`Source ${index}`} style={styles.image} />
          </li>
        ))}
      </ul>
    </div>
  );
};

const styles = {
  container: {
    margin: '20px auto',
    width: '80%',
    padding: '20px',
    border: '1px solid #ddd',
    borderRadius: '8px',
    backgroundColor: '#f9f9f9',
  },
  textSource: {
    marginBottom: '10px',
  },
  imageSource: {
    marginBottom: '10px',
  },
  image: {
    maxWidth: '100%',
    height: 'auto',
  },
};

export default AnswerDisplay;
