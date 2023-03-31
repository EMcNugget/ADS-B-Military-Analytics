import { Link, Button } from "@mui/material";
import Footer from "../libs/footer";
import Header from "../libs/header";
import "../../scss/home.scss";

const HomeButton = () => {
  return (
    <Link href="/history" underline="none">
      <Button variant="contained" color="primary" size="large">
        Get Started
      </Button>
    </Link>
  );
};
function Home() {
  return (
    <div className="home">
      <Header />
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
          <HomeButton />
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default Home;
