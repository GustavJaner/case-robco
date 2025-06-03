import axios from 'axios'

// console.log("API baseURL:", process.env.REACT_APP_API_URL || 'http://localhost:8000');
const api = axios.create({
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000', // Need to set during building (Compiled to static files).
})

// Add a request/response interceptor for logging
api.interceptors.request.use(request => {
    console.log('Starting Request', request);
    return request;
});
api.interceptors.response.use(response => {
    console.log('Response:', response);
    return response;
}, error => {
    console.error('API Error:', error);
    return Promise.reject(error);
});

export default api;
