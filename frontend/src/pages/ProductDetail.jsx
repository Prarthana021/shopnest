import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import api from '../api/axios'
import { useAuth } from '../context/AuthContext'

export default function ProductDetail() {
  const { id } = useParams()   // grabs :id from the URL
  const { user } = useAuth()
  const navigate = useNavigate()
  const [product, setProduct] = useState(null)
  const [quantity, setQuantity] = useState(1)
  const [loading, setLoading] = useState(true)
  const [adding, setAdding] = useState(false)
  const [message, setMessage] = useState('')

  useEffect(() => {
    api.get(`/products/${id}/`)
      .then(res => setProduct(res.data))
      .finally(() => setLoading(false))
  }, [id])

  const handleAddToCart = async () => {
    if (!user) {
      navigate('/login')
      return
    }
    setAdding(true)
    try {
      await api.post('/orders/cart/items/', { product_id: product.id, quantity })
      setMessage('Added to cart!')
      setTimeout(() => setMessage(''), 2000)
    } catch {
      setMessage('Failed to add to cart.')
    } finally {
      setAdding(false)
    }
  }

  if (loading) return <p className="text-center py-20 text-gray-400">Loading...</p>
  if (!product) return <p className="text-center py-20 text-gray-400">Product not found.</p>

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      <div className="grid md:grid-cols-2 gap-10">
        {/* Image */}
        <div className="rounded-xl overflow-hidden border border-gray-200 bg-gray-50">
          {product.image ? (
            <img src={`http://localhost:8000${product.image}`} alt={product.name} className="w-full h-80 object-cover" />
          ) : (
            <div className="w-full h-80 flex items-center justify-center text-gray-300">No image</div>
          )}
        </div>

        {/* Info */}
        <div>
          <p className="text-indigo-500 text-sm mb-1">{product.category?.name}</p>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">{product.name}</h1>
          <p className="text-3xl font-bold text-indigo-600 mb-4">${product.price}</p>
          <p className="text-gray-500 text-sm mb-6">{product.description}</p>

          <p className={`text-sm mb-4 ${product.stock > 0 ? 'text-green-600' : 'text-red-500'}`}>
            {product.stock > 0 ? `${product.stock} in stock` : 'Out of stock'}
          </p>

          {product.stock > 0 && (
            <div className="flex items-center gap-4 mb-4">
              <label className="text-sm text-gray-600">Qty:</label>
              <input
                type="number"
                min="1"
                max={product.stock}
                value={quantity}
                onChange={(e) => setQuantity(Number(e.target.value))}
                className="w-16 border border-gray-200 rounded px-2 py-1 text-sm text-center"
              />
            </div>
          )}

          {message && <p className="text-green-600 text-sm mb-3">{message}</p>}

          <button
            onClick={handleAddToCart}
            disabled={adding || product.stock === 0}
            className="w-full bg-indigo-600 text-white py-3 rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50"
          >
            {adding ? 'Adding...' : 'Add to Cart'}
          </button>
        </div>
      </div>
    </div>
  )
}
