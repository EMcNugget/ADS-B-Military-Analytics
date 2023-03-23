import { useState } from "react";
import { Link } from "react-router-dom";
import Footer from "../libs/footer";
import "../../scss/home.scss";

function Home() {
  const [show, setShow] = useState(false);

  return (
    <div>
      <div className="home">
        <div className="home_container">
          <div className="home_title">
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
                Get Started
              </button>
            </Link>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default Home;
