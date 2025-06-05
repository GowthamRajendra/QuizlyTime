import useAuth from "./useAuth";
import useAxios from "./useAxios";

const useLogout = () => {
    const { setAuth } = useAuth()
    const axios = useAxios()

    const logout = async () => {
        try {
            const response = await axios.post(
                '/logout'
            )

            console.log(JSON.stringify(response?.data))
            
            // remove the access_token, email and username
            axios.defaults.headers.common['Authorization'] = ''
            setAuth(null)

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
            setAuth(null)
        }
    }

    return { logout }
}

export default useLogout