import { FaGithub } from "react-icons/fa";
import "../css/footer.css";

function Footer() {
  return (
    <div className="body">
      <footer className="footer">
        <a
          href="https://github.com/EMcNugget/ADSB-Military-Analytics"
          target="_blank"
          rel="noopener noreferrer"
        >
          <FaGithub className="icon" />
          GitHub
        </a>
        <p className="copy">&copy;2023 ADSB-Military-Analytics.</p>
        <a className="copy" href="/privacy">Privacy Policy</a>
      </footer>
    </div>
  );
}

export default Footer;
