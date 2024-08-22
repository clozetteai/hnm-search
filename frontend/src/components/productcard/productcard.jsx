import React from 'react'
import { ShoppingBag } from 'lucide-react';

// TODO Update when data is ready
// const ProductCard = React.memo(({
//   prod_name,
//   colour_group_name,
//   detail_desc,
//   image,
//   perceived_colour_value_name,
//   product_type_name
// }) => (
//   <div className="bg-white rounded-lg shadow-md overflow-hidden transition-transform duration-300 hover:shadow-xl hover:-translate-y-1">
//     <img src={`data:image/jpeg;base64,${image}`} alt={prod_name} className="w-full h-48 object-cover" />
//     <div className="p-4">
//       <h3 className="text-lg font-semibold truncate">{prod_name}</h3>
//       <p className="text-sm text-gray-600">{colour_group_name} - {perceived_colour_value_name}</p>
//       <p className="text-sm text-gray-600">{product_type_name}</p>
//       <button className="mt-4 w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition-colors duration-300 flex items-center justify-center">
//         <ShoppingBag size={18} className="mr-2" />
//         Add to Cart
//       </button>
//     </div>
//   </div>
// ));


const ProductCard = React.memo(({
  prod_name,
  colour_group_name,
  detail_desc,
  image,
  perceived_colour_value_name,
  product_type_name
}) => (
  <div className="bg-white rounded-lg shadow-md overflow-hidden transition-transform duration-300 hover:shadow-xl hover:-translate-y-1">
  <img src={`data:image/jpeg;base64,${image}`} alt={prod_name} className="w-full h-48 object-cover" />
  <div className="p-4">
    <h3 className="text-lg font-semibold truncate">{prod_name}</h3>
    <p className="text-sm text-gray-600">{colour_group_name} - {perceived_colour_value_name}</p>
    <p className="text-sm text-gray-600">{product_type_name}</p>
    <button className="mt-4 w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition-colors duration-300 flex items-center justify-center">
      <ShoppingBag size={18} className="mr-2" />
      Add to Cart
    </button>
  </div>
</div>
));


export default ProductCard;