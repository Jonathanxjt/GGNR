
import React from 'react';
import {MyNavbar} from './components/MyNavbar/MyNavbar';

function App() {
  return (
    <div className="App">
      <Nav/>
    </div>
  );
}
// How to run components in React
function Nav() {
  return (
    <div>
      <MyNavbar/>
      <h1>Test</h1>
      <p>test123</p>
    </div>
  );
}

export default App;
