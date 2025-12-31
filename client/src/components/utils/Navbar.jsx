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
          <NavLink to="/pageB" className="nav-link">
            Page B
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

// import { Link } from "react-router-dom"
// function Navbar(){
//     return(
//         <header>
//             <nav>
//                 <span className="nav-left">
//                     <p>App Name</p>
//                 </span>
//                 <span className="nav-right">
//                     <Link to="/">Dashboard</Link>
//                     <Link to="pageB">Page B</Link>
//                     <Link to="/forecast">Forecast</Link>
//                 </span>
//                 </nav>
//         </header>
//     )
// }

// export default Navbar