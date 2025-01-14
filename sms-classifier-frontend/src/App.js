import React, { useState } from 'react';
import './App.css';

function App() {
  const [sms, setSms] = useState('');
  const [prediction, setPrediction] = useState(null);

  // Handle form input change
  const handleInputChange = (e) => {
    setSms(e.target.value);
  };

  // Call the backend API to get the prediction
  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch('http://127.0.0.1:8000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: sms }),
    });

    const result = await response.json();
    setPrediction(result.prediction);
  };

  return (
    <div className="App">
      <h1>SMS Spam Classifier</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          rows="4"
          cols="50"
          value={sms}
          onChange={handleInputChange}
          placeholder="Enter your SMS message here"
        ></textarea>
        <br />
        <button type="submit">Classify</button>
      </form>

      {prediction && (
        <h2>{prediction === 'spam' ? 'It is a spam message!' : 'It is not a spam message!'}</h2>
      )}
    </div>
  );
}

export default App;
