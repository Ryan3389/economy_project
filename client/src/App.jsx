import Dashboard from "./pages/Dashboard";
import { Outlet } from "react-router-dom";
import Navbar from "./components/utils/Navbar";
import './App.css'

function App() {
 return (
    <>
        <Navbar/>
        <Outlet/>
    </>
)
}

export default App;
