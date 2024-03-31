
import React from 'react';
import RouteConfig from './Route';
import ToastManager from './components/ToastManager';
import './App.css';

function App() {

  return (
    <div className="App">
      <ToastManager />
      <RouteConfig />
      
    </div>
  );
}

export default App;
