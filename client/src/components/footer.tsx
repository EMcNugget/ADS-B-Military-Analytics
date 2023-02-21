import { FaGithub } from 'react-icons/fa';
import '../css/footer.css';

export const Footer = () => {
  return (
    <div className="footer">
      <a href="https://github.com/EMcNugget/adsb_mil_data" target="_blank" rel="noopener noreferrer">
        <FaGithub className="icon" />
        GitHub
      </a>
      <p className="copy">&copy;2023 ADSB-Military-Analytics.</p>
    </div>
  );
};
