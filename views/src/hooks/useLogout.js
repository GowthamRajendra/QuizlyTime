import useAuth from "./useAuth";
import axios from "../api/axios";

const useLogout = () => {
    const { setAuth } = useAuth()

    const logout = async () => {
        try {
            const response = await axios.post(
                '/logout'
            )

            console.log(JSON.stringify(response?.data))

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
        }
    }

    return { logout }
}

export default useLogout