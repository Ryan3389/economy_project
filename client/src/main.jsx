import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Dashboard from './pages/Dashboard.jsx'
// import PageB from './pages/PageB.jsx'
import InsightsPage from './pages/InsightsPage.jsx'
import ForecastPage from './pages/ForecastPage.jsx'

import {createBrowserRouter, Route, RouterProvider} from "react-router-dom"

const router = createBrowserRouter([
    {
        path: "/",
        element: <App/>,
        errorElement: <h1>An error occured</h1>,
        children: [
            {
                index: true,
                element: <Dashboard/>
            },
            {
                path: "/insights",
                element: <InsightsPage/>
            },
            {
                path: "/forecast",
                element: <ForecastPage/>
            }
        ]
    }
])
createRoot(document.getElementById('root')).render(
   <RouterProvider router={router} />
)
