import "../../scss/header.scss";

const Header = () => {
  return (
    <header className="header">
      <h1 className="header_title">ADS-B Military Analytics</h1>
      <nav className="header_nav">
        <ul>
          <li>
            <a href="/">Home</a>
          </li>
          <li>
            <a href="/map">Map</a>
          </li>
          <li>
            <a href="/history">History</a>
          </li>
          <li>
            <a href="/about">About</a>
          </li>
          <li>
            <a
              href="mailto: support@adsbmilanalytics.com"
              target="_blank"
              rel="noreferrer"
            >
              Contact
            </a>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
