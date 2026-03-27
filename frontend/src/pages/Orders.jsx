import { useEffect, useState } from 'react'
import api from '../api/axios'

const STATUS_COLORS = {
  pending: 'bg-yellow-100 text-yellow-700',
  processing: 'bg-blue-100 text-blue-700',
  shipped: 'bg-purple-100 text-purple-700',
  delivered: 'bg-green-100 text-green-700',
}

export default function Orders() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/orders/')
      .then(res => setOrders(res.data))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p className="text-center py-20 text-gray-400">Loading orders...</p>

  return (
    <div className="max-w-3xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Order History</h1>

      {orders.length === 0 ? (
        <p className="text-center text-gray-400 py-12">You haven't placed any orders yet.</p>
      ) : (
        <div className="space-y-6">
          {orders.map(order => (
            <div key={order.id} className="bg-white border border-gray-200 rounded-lg overflow-hidden">
              {/* Order header */}
              <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
                <div>
                  <p className="text-sm font-medium text-gray-800">Order #{order.id}</p>
                  <p className="text-xs text-gray-400">{new Date(order.created_at).toLocaleDateString()}</p>
                </div>
                <div className="flex items-center gap-4">
                  <span className={`text-xs px-3 py-1 rounded-full font-medium ${STATUS_COLORS[order.status]}`}>
                    {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                  </span>
                  <p className="text-indigo-600 font-bold">${order.total_price}</p>
                </div>
              </div>

              {/* Order items */}
              <div className="divide-y divide-gray-50">
                {order.items.map(item => (
                  <div key={item.id} className="flex justify-between px-6 py-3 text-sm">
                    <span className="text-gray-600">{item.product_name} × {item.quantity}</span>
                    <span className="text-gray-700 font-medium">
                      ${(item.unit_price * item.quantity).toFixed(2)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
