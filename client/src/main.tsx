import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import { Link, BrowserRouter, Route, Routes } from 'react-router-dom';
import Api from './components/api_fetch';
import Footer from './components/footer';
import './css/landing.css';
import './css/footer.css';

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

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
