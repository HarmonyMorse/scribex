import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    // For development, accept all certificates
    validateStatus: () => true
});

// Add response interceptor to handle errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error('API Error:', error);
        if (error.code === 'ERR_BAD_SSL_CLIENT_AUTH_CERT') {
            console.warn('SSL Certificate Error - Development Mode');
            return error.response;
        }
        return Promise.reject(error);
    }
);

export const checkHealth = async () => {
    try {
        const response = await api.get('/health');
        return response.data;
    } catch (error) {
        console.error('Error checking API health:', error);
        throw error;
    }
};

export default api; 