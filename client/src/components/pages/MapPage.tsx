import "../../scss/map.scss";
import Footer from "../libs/footer";
import Header from "../libs/header";

function Map() {
  return (
    <div>
      <div>
        <Header />
      </div>
      <div className="main">
        <h1>Coming Soon</h1>
      </div>
      <div className="foot">  
        <Footer />
      </div>
    </div>
  );
}

export default Map;
