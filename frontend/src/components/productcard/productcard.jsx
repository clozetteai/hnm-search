import React from 'react'
import { ShoppingBag } from 'lucide-react';

const ProductCard = React.memo(({ title, price, imageUrl }) => (
  <div className="bg-white rounded-lg shadow-md overflow-hidden transition-transform duration-300 hover:shadow-xl hover:-translate-y-1">
    <img src={imageUrl} alt={title} className="w-full h-48 object-cover" />
    <div className="p-4">
      <h3 className="text-lg font-semibold truncate">{title}</h3>
      <p className="text-xl font-bold text-green-600">${price}</p>
      <button className="mt-2 w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition-colors duration-300 flex items-center justify-center">
        <ShoppingBag size={18} className="mr-2" />
        Add to Cart
      </button>
    </div>
  </div>
));


export default ProductCard;