import axios from 'axios';

const api = axios.create({
    baseURL: '/api/v1', // Using Vite proxy
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            // Redirect to login handled at component level or via context
        }
        return Promise.reject(error);
    }
);

export default api;
