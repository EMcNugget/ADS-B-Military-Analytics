import ReactDOMServer from 'react-dom/server';
import { StaticRouter } from "react-router-dom/server";
import { Routes, Route } from 'react-router-dom';
import Api from './components/api_fetch';
import Footer from './components/footer';
import './css/landing.css';
import './css/footer.css';

function Home() {
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
          <a href="/history">
            <button className="button">Click to get started</button>
          </a>
        </div>
      </div>
      <Footer />
    </div>
  );
}

function App() {
  return (
    <StaticRouter location={''}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/history" element={<Api />} />
      </Routes>
    </StaticRouter>
  );
}

export default function render(req: any, res: any) {
  const html = ReactDOMServer.renderToString(<App />);
  res.send(html);
}
