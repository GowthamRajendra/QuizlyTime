import { createContext,  useState, useEffect } from "react";
import useRefresh from "../hooks/useRefresh";

const AuthContext = createContext({})

export const AuthProvider = ({children}) => {
    const [ auth, setAuth ] = useState(null)
    const { refresh } = useRefresh()

    // if the user did not log out and their refresh token is still valid,
    // they will be automatically logged in
    useEffect(() => {
        async function handleRefresh() {
            const data = await refresh()
            console.log(`refreshed: ${data?.email ?? "Not logged in"}, ${data?.username ?? "Not logged in"}`)
            setAuth(data)
        }

        handleRefresh()

        return () => {
            console.log('cleanup')
        }
    }, [])

    return (
        <AuthContext.Provider value={{auth, setAuth}}>
            {children}
        </AuthContext.Provider>
    )
}

export default AuthContext