import { api } from './client'

// Session-cookie auth (matches the Django backend's django.contrib.auth
// session login, not a token) — the API client already sends credentials.
export const auth = {
  register: (username, password) => api.post('/guest/users/register/', { username, password }),
  login: (username, password) => api.post('/guest/users/login/', { username, password }),
  me: () => api.get('/me/'),
  logout: () => api.post('/logout/', {}),
}
