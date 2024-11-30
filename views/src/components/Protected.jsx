import { useLocation, Navigate, Outlet } from "react-router-dom";
import useAuth from "../hooks/useAuth";
import { useEffect } from "react";

// Component to protect routes from unauthenticated users

function Protected() {
    const { auth } = useAuth()
    const location = useLocation()

    useEffect(() => {
        console.log(`to: ${location.pathname}`)
    },[])

    return (
        // if the user is logged in, let them access the route
        // otherwise, redirect them to the login page, track where they wanted to go and replace the current history entry
        auth 
        ? <Outlet />
        : <Navigate to='/login' state={{ to: location.pathname }} replace />
    )
}

export default Protected