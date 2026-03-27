import axios from 'axios'

// One axios instance shared across the whole app.
// baseURL means every api.get('/products/') call becomes
// http://localhost:8000/api/products/ automatically.
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
})

// This interceptor runs before EVERY request.
// It grabs the token from localStorage and attaches it to the header.
// Django reads this header to know who is making the request.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
