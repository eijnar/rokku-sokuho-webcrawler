import React from 'react';
import { BandProvider } from './contexts/BandContext';
import BandList from './components/BandList/BandList';

const App = () => {
  return (
    <BandProvider>
      <div className="App">
        <h1>Band Directory</h1>
        <BandList />
      </div>
    </BandProvider>
  );
}

export default App;