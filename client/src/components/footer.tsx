import { FaGithub } from "react-icons/fa";
import "../scss/footer.scss";

function Footer() {
  return (
    <div className="body">
      <footer className="footer">
        <a
          href="https://github.com/EMcNugget/ADS-B-Military-Analytics"
          target="_blank"
          rel="noopener noreferrer"
        >
          <FaGithub className="icon" />
          GitHub
        </a>
        <p className="copy">&copy;2023 ADSB-Military-Analytics.</p>
        <a className="copy" href="/privacy">
          Privacy Policy
        </a>
      </footer>
    </div>
  );
}

export default Footer;
