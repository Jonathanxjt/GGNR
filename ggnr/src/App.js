
import React from 'react';
import {MyNavbar} from './components/MyNavbar/MyNavbar';
import RouteConfig from './Route';


function App() {
  return (
    <div className="App">
      <Nav/>
      <RouteConfig />
    </div>
  );
}
// How to run components in React
function Nav() {
  return (
    <div>
      <MyNavbar/>
    </div>
  );
}

export default App;
