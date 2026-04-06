import React from 'react';

function App() {
  const params = new URLSearchParams(window.location.search);
  const username = params.get('username');

  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to the Insecure React App</h1>
        
        {/* VULNERABILITY: Reflected XSS */}
        {username && (
          <p>Hello, <span dangerouslySetInnerHTML={{ __html: username }}></span>!</p>
        )}

        <p>Try adding "?username=YourName" to the URL!</p>
      </header>
    </div>
  );
}

export default App;