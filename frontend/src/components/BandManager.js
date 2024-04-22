import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Band from './Band';
import './styles/BandManager.css';

const BandManager = () => {
  const [bands, setBands] = useState([]);
  const [newBandName, setNewBandName] = useState('');

  useEffect(() => {
    fetchBands();
  }, []);

  const fetchBands = async () => {
    const response = await axios.get('http://localhost:8000/bands/');
    setBands(response.data);
  };

  const handleAddBand = async () => {
    if (newBandName) {
      const response = await axios.post('http://localhost:8000/bands/', { band_name: newBandName });
      setBands([...bands, response.data]);
      setNewBandName('');  // Reset the input field
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', padding: '20px' }}>
        <input
          type="text"
          placeholder="Add new band"
          value={newBandName}
          onChange={(e) => setNewBandName(e.target.value)}
        />
        <button onClick={handleAddBand}>Save Band</button>
      </div>
      {bands.map(band => (
        <Band key={band.band_id} band={band} fetchBands={fetchBands} />
      ))}
    </div>
  );
};

export default BandManager;
