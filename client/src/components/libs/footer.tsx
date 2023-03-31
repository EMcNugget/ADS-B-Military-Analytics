import { Box, Link, Typography } from "@mui/material";
import { FaMailBulk, FaGithub } from "react-icons/fa";
import "../../scss/footer.scss";

export default function Footer() {
  const content = {
    copy: "© 2023 ADS-B Military Analytics. All rights reserved.",
    git: "Github",
    contact: "Contact",
  };

  return (
    <footer className="footer">
      <Box
        display="flex"
        flexWrap="wrap"
        alignItems="center"
        className="root"
        bgcolor={"#282c34"}
        color={"white"}
      >
        <Box component="nav" sx={{ display: "flex", gap: "1.1rem" }}>
          <Link
            underline="hover"
            color={"inherit"}
            href="https://github.com/ADS-B-Military-Analytics/ADS-B-Military-Analytics"
            variant="body2"
            rel="noreferrer"
            target="_blank"
            className="link"
          >
            <FaGithub />
            &nbsp;
            {content["git"]}
          </Link>
          <Link
            underline="hover"
            color={"inherit"}
            href="mailto: support@adsbmilanalytics.com"
            variant="body2"
            rel="noopener noreferrer"
            target="_blank"
            className="link"
          >
            <FaMailBulk />
            &nbsp;
            {content["contact"]}
          </Link>
        </Box>

        <Typography component="p" variant="caption" gutterBottom={false}>
          {content["copy"]}
        </Typography>
      </Box>
    </footer>
  );
}
