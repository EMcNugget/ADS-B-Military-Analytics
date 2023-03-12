import ReactDOM from "react-dom/client";
import { Routes, Route, Link, BrowserRouter, Navigate } from "react-router-dom";
import { useState } from "react";
import Api from "./components/api_fetch";
import Footer from "./components/footer";
import Privacy from "./components/privacy";
import "./css/landing.css";
import "./css/footer.css";

function Home() {
  const [show, setShow] = useState(false);

  return (
    <div>
      <div className="landing">
        <div className="landing__container">
          <div className="landing_title">
            <h1>ADS-B Military Analytics</h1>
            <h6>
              ADS-B Military Analytics is a tool to view historical data for
              military aircraft from our extensive database collected 24/7 made
              possible by ADS-B Exchange.
            </h6>
            <h2>No data before March 9th, 2023</h2>
          </div>
          <div className="button-container">
            <Link to="/history">
              <button className="button" onClick={() => setShow(!show)}>
                Click to get started
              </button>
            </Link>
          </div>
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
        <Route path="/privacy" element={<Privacy />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  );
}

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <App />
);
