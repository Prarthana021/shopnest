import { useEffect, useState } from 'react'
import api from '../api/axios'
import ProductCard from '../components/ProductCard'

export default function Home() {
  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('')

  // Fetch categories once on mount
  useEffect(() => {
    api.get('/products/categories/').then(res => setCategories(res.data))
  }, [])

  // Fetch products whenever search or category filter changes
  useEffect(() => {
    setLoading(true)
    const params = new URLSearchParams()
    if (search) params.append('search', search)
    if (selectedCategory) params.append('category', selectedCategory)

    api.get(`/products/?${params.toString()}`)
      .then(res => setProducts(res.data))
      .finally(() => setLoading(false))
  }, [search, selectedCategory])

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero */}
      <div className="bg-indigo-600 text-white px-6 py-12 text-center">
        <h1 className="text-3xl font-bold mb-2">Welcome to ShopNest</h1>
        <p className="text-indigo-200 mb-6">Find everything you need</p>
        <input
          type="text"
          placeholder="Search products..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full max-w-md px-4 py-2 rounded-lg text-gray-800 text-sm focus:outline-none"
        />
      </div>

      <div className="max-w-6xl mx-auto px-6 py-8">
        {/* Category filters */}
        <div className="flex gap-2 flex-wrap mb-6">
          <button
            onClick={() => setSelectedCategory('')}
            className={`px-4 py-1.5 rounded-full text-sm border transition-colors ${
              selectedCategory === '' ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-gray-600 border-gray-200 hover:border-indigo-400'
            }`}
          >
            All
          </button>
          {categories.map(cat => (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className={`px-4 py-1.5 rounded-full text-sm border transition-colors ${
                selectedCategory === cat.id ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-gray-600 border-gray-200 hover:border-indigo-400'
              }`}
            >
              {cat.name}
            </button>
          ))}
        </div>

        {/* Product grid */}
        {loading ? (
          <p className="text-center text-gray-400 py-12">Loading products...</p>
        ) : products.length === 0 ? (
          <p className="text-center text-gray-400 py-12">No products found.</p>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {products.map(product => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
