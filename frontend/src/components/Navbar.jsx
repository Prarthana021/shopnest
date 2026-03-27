import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  return (
    <nav className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
      <Link to="/" className="text-xl font-bold text-indigo-600">ShopNest</Link>

      <div className="flex items-center gap-6">
        <Link to="/" className="text-gray-600 hover:text-indigo-600 text-sm">Products</Link>

        {user ? (
          <>
            <Link to="/cart" className="text-gray-600 hover:text-indigo-600 text-sm">Cart</Link>
            <Link to="/orders" className="text-gray-600 hover:text-indigo-600 text-sm">Orders</Link>
            <span className="text-gray-400 text-sm">Hi, {user.first_name || user.email}</span>
            <button
              onClick={handleLogout}
              className="text-sm text-red-500 hover:text-red-700"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="text-sm text-gray-600 hover:text-indigo-600">Login</Link>
            <Link to="/register" className="text-sm bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700">
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  )
}
