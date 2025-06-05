import useAuth from "./useAuth";
import axios from "../api/axios";

const useRefresh = () => {
    const { setAuth } = useAuth()

    const refresh = async () => {
        try {
            const response = await axios.get(
                '/auth/refresh'
            )
    
            console.log(JSON.stringify(response?.data))
    
            const email = response?.data?.email
            const username = response?.data?.username

            console.log(`refreshed: email: ${email}, username: ${username}`)

            axios.defaults.headers.common['Authorization'] = `Bearer ${response?.data?.access_token}`
    
            return {email: email, username: username}
    
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
            
            axios.defaults.headers.common['Authorization'] = ''
            return null
        }
    }

    return { refresh }
}

export default useRefresh
