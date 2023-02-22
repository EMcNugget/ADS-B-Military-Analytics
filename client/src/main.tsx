import { Routes, Route, Link, BrowserRouter } from 'react-router-dom';
import { useState } from 'react';
import Api from './components/api_fetch';
import Footer from './components/footer';
import './css/landing.css';
import './css/footer.css';
import ReactDOM from 'react-dom';
import React from 'react';

function Home() {
  const [show, setShow] = useState(false);

  return (
    <div className="landing">
      <div className="landing__container">
        <div className="landing_title">
          <h1>
            ADS-B Military Analytics
          </h1>
          <h6>
            No data before February 20th, 2023
          </h6>
        </div>
        <div className="button-container">
          <Link to="/history">
            <button className="button" onClick={() => setShow(!show)}>Click to get started</button>
          </Link>
        </div>
      </div>
      <Footer />
    </div>
  );
}


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/history" element={<Api />} />
      </Routes>
    </BrowserRouter>
  );
}

ReactDOM.render(<App />, document.getElementById('root'));