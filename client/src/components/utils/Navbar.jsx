import { Link, NavLink } from "react-router-dom";


function Navbar() {
  return (
    <header className="navbar">
      <nav className="navbar-inner">
        <div className="nav-left">
          <span className="app-name">EconSignals</span>
        </div>

        <div className="nav-right">
          <NavLink to="/" end className="nav-link">
            Dashboard
          </NavLink>
          <NavLink to="/insights" className="nav-link">
            Insights
          </NavLink>
          <NavLink to="/forecast" className="nav-link nav-link--primary">
            Forecast
          </NavLink>
        </div>
      </nav>
    </header>
  );
}

export default Navbar;
