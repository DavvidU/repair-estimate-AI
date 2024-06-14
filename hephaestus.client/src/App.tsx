import "./App.css";
import Navigation from "./Navigation/Navigation";
import React, { useEffect } from 'react'; 

function App() {
    useEffect(() => {
        document.title = "Hephaestus";
    }, []);
  return (
    <div className="App">
      <Navigation />
    </div>
  );
}

export default App;
