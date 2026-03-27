import { Link } from 'react-router-dom'

export default function ProductCard({ product }) {
  return (
    <Link to={`/products/${product.id}`} className="bg-white rounded-lg border border-gray-200 hover:shadow-md transition-shadow overflow-hidden">
      {product.image ? (
        <img
          src={`http://localhost:8000${product.image}`}
          alt={product.name}
          className="w-full h-48 object-cover"
        />
      ) : (
        <div className="w-full h-48 bg-gray-100 flex items-center justify-center text-gray-400 text-sm">
          No image
        </div>
      )}
      <div className="p-4">
        <p className="text-xs text-indigo-500 mb-1">{product.category?.name}</p>
        <h3 className="text-gray-800 font-medium text-sm mb-2 line-clamp-2">{product.name}</h3>
        <p className="text-indigo-600 font-bold">${product.price}</p>
        <p className="text-xs text-gray-400 mt-1">{product.stock > 0 ? `${product.stock} in stock` : 'Out of stock'}</p>
      </div>
    </Link>
  )
}
