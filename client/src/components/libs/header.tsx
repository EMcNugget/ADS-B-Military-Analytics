import { IconButton, Typography, Toolbar, Menu, MenuItem } from "@mui/material";
import { Link } from "react-router-dom";
import MenuIcon from "@mui/icons-material/Menu";
import "../../scss/header.scss";
import React from "react";

export default function Header() {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <Toolbar className="header">
      <IconButton
        size="large"
        edge="start"
        color="inherit"
        aria-label="menu"
        sx={{ mr: 2 }}
        onClick={handleClick}
      >
        <MenuIcon />
      </IconButton>
      <Menu anchorEl={anchorEl} open={open} onClose={handleClose}>
        <MenuItem component={Link} to="/" onClick={handleClose}>
          Home
        </MenuItem>
        <MenuItem component={Link} to="/map" onClick={handleClose}>
          Map
        </MenuItem>
        <MenuItem component={Link} to="/history" onClick={handleClose}>
          Historical Data
        </MenuItem>
        <MenuItem component={Link} to="/about" onClick={handleClose}>
          About
        </MenuItem>
      </Menu>
      <Typography
        variant="h6"
        color="inherit"
        component="div"
        sx={{ flexGrow: 1 }}
        fontWeight="bold"
      >
        ADS-B Military Analytics
      </Typography>
    </Toolbar>
  );
}
