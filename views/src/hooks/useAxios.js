import axios from "../api/axios";
import { useEffect } from "react";
import useRefresh from "./useRefresh";
import useAuth from "./useAuth";
import { useNavigate } from "react-router-dom";

// Set up axios interceptors to refresh access token if it is expired

const useAxios = () => {
    const { refresh } = useRefresh()
    const { setAuth } = useAuth()
    const navigate = useNavigate()
    
    useEffect(() => {      

        // Intercept failed requests and attempt a token refresh and retry original request if the reason for failure
        // was an expired access token.
        const responseInterceptor = axios.interceptors.response.use(
            response => response, // if the response is success, dont do anything
            async (error) => {
                const prevRequest = error?.config
                
                // only try to refresh if the access token is missing/invalid/expired and the request has not already been retried.
                // log the user out if the refresh token is missing/invalid/expired.
                if (error?.response?.status === 401 && !prevRequest._retry) {
                    if (error.response.data.message === 'access token is expired.' ||
                        error.response.data.message === 'access token is missing.' ||
                        error.response.data.message === 'access token is invalid.'
                    ) {
                        prevRequest._retry = true
                        console.log(`Request failed because ${error.response.data.message}. Attempting refresh...`)
                        setAuth(await refresh())
                        return axios(prevRequest)
                    }
                    else if (error.response.data.message === 'refresh token is expired.' ||
                        error.response.data.message === 'refresh token is missing.' ||
                        error.response.data.message === 'refresh token is invalid.'
                    ) {
                        // If they don't have a valid refresh token, log them out and return to landing page.
                        console.log(`${error.response.data.message} Logging out...`)

                        axios.defaults.headers.common['Authorization'] = ''
                        setAuth(null)
                        navigate('/')
                    }
                }
                return Promise.reject(error)
            }
        )

        return () => {
            axios.interceptors.response.eject(responseInterceptor)
        }
    }, [refresh])

    return axios
}

export default useAxios