import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000'

// axios.defaults.headers.common['Authorization'] = `Bearer BRUH`;

export default axios.create({
    baseURL: BASE_URL,
    withCredentials: true
})