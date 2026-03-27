import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/axios'

export default function Cart() {
  const [cart, setCart] = useState(null)
  const [loading, setLoading] = useState(true)
  const [placing, setPlacing] = useState(false)
  const navigate = useNavigate()

  const fetchCart = () => {
    api.get('/orders/cart/')
      .then(res => setCart(res.data))
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchCart() }, [])

  const handleRemove = async (itemId) => {
    await api.delete(`/orders/cart/items/${itemId}/`)
    fetchCart()
  }

  const handleQuantityChange = async (itemId, quantity) => {
    if (quantity < 1) return
    await api.patch(`/orders/cart/items/${itemId}/`, { quantity })
    fetchCart()
  }

  const handleCheckout = async () => {
    setPlacing(true)
    try {
      await api.post('/orders/')
      navigate('/orders')
    } catch (err) {
      alert(err.response?.data?.detail || 'Checkout failed.')
    } finally {
      setPlacing(false)
    }
  }

  if (loading) return <p className="text-center py-20 text-gray-400">Loading cart...</p>

  const items = cart?.items || []
  const total = items.reduce((sum, item) => sum + item.product.price * item.quantity, 0)

  return (
    <div className="max-w-3xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Your Cart</h1>

      {items.length === 0 ? (
        <p className="text-gray-400 text-center py-12">Your cart is empty.</p>
      ) : (
        <>
          <div className="space-y-4 mb-8">
            {items.map(item => (
              <div key={item.id} className="flex items-center gap-4 bg-white border border-gray-200 rounded-lg p-4">
                {/* Product image */}
                <div className="w-16 h-16 bg-gray-100 rounded overflow-hidden shrink-0">
                  {item.product.image ? (
                    <img src={`http://localhost:8000${item.product.image}`} alt={item.product.name} className="w-full h-full object-cover" />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-gray-300 text-xs">No img</div>
                  )}
                </div>

                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-800">{item.product.name}</p>
                  <p className="text-indigo-600 text-sm font-bold">${item.product.price}</p>
                </div>

                {/* Quantity controls */}
                <div className="flex items-center gap-2">
                  <button onClick={() => handleQuantityChange(item.id, item.quantity - 1)}
                    className="w-7 h-7 rounded border border-gray-200 text-gray-600 hover:bg-gray-100 text-sm">−</button>
                  <span className="text-sm w-6 text-center">{item.quantity}</span>
                  <button onClick={() => handleQuantityChange(item.id, item.quantity + 1)}
                    className="w-7 h-7 rounded border border-gray-200 text-gray-600 hover:bg-gray-100 text-sm">+</button>
                </div>

                <p className="text-sm font-bold text-gray-700 w-16 text-right">
                  ${(item.product.price * item.quantity).toFixed(2)}
                </p>

                <button onClick={() => handleRemove(item.id)}
                  className="text-red-400 hover:text-red-600 text-sm ml-2">Remove</button>
              </div>
            ))}
          </div>

          {/* Summary */}
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <div className="flex justify-between text-gray-700 font-bold text-lg mb-4">
              <span>Total</span>
              <span>${Number(total).toFixed(2)}</span>
            </div>
            <button
              onClick={handleCheckout}
              disabled={placing}
              className="w-full bg-indigo-600 text-white py-3 rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50"
            >
              {placing ? 'Placing order...' : 'Place Order'}
            </button>
          </div>
        </>
      )}
    </div>
  )
}
