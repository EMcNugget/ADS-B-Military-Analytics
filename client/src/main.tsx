import ReactDOM from "react-dom/client";
import { Routes, Route, BrowserRouter, Navigate } from "react-router-dom";
import Api from "./components/pages/ApiPage";
import About from "./components/pages/AboutPage";
import Map from "./components/pages/MapPage";
import Privacy from "./components/pages/PrivacyPolicy";
import Home from "./components/pages/HomePage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/map" element={<Map />} />
        <Route path="/about" element={<About />} />
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
