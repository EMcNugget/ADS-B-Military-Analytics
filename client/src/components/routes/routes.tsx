import { Routes, Route, BrowserRouter, Navigate } from "react-router-dom";
import Api from "../pages/ApiPage";
import About from "../pages/AboutPage";
import Map from "../pages/MapPage";
import Privacy from "../pages/PrivacyPolicy";
import Home from "../pages/HomePage";

export default function App() {
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
