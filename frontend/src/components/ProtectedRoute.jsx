import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

// Wraps pages that require login.
// If user is not logged in, redirects to /login automatically.
export default function ProtectedRoute({ children }) {
  const { user } = useAuth()
  return user ? children : <Navigate to="/login" replace />
}
