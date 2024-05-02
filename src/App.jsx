import { useState } from "react";
import "./App.css";

function App() {
  return (
    <div id="main">
      <div id="title">
        <p>Canticum</p>
      </div>
      <div id="input-box">
        <input id="song-input" type="text" placeholder="search for a song" />
        <div id="go-button">
          <button>go!</button>
        </div>
      </div>
    </div>
  );
}

export default App;
