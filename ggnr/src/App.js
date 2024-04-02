
import React from 'react';
import RouteConfig from './Route';
import ToastManager from './components/ToastManager';
import './App.css';
import MyFooter from './components/MyFooter/MyFooter';

function App() {

  return (
    <div className="App">
      <ToastManager />
      <RouteConfig />
      <MyFooter />
    </div>
  );
}

export default App;
