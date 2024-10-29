import { createContext,  useState, useEffect } from "react";
import axios from "../api/axios";

const AuthContext = createContext({})

export const AuthProvider = ({children}) => {
    const [ auth, setAuth ] = useState(null)

    // check if user is already logged in
    useEffect(() => {
        async function checkAuth() {
            try {
                const response = await axios.get(
                    '/auth/check'
                )

                console.log(JSON.stringify(response?.data))

                const email = response?.data?.email
                const username = response?.data?.username

                setAuth({email, username})

            } catch (err) {
                if (!err?.response) {
                    console.error("No response")
                }
                else if (err.response) {
                    console.error(err.response.data.message)
                }
                else {
                    console.error(err)
                }
            }
        }

        checkAuth()

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