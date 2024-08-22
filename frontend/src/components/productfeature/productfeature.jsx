import React from 'react';
import { FEATURE2 } from '../../assets';

const FeatureCard = ({ title, description, icon }) => (
  <div className="bg-slate-100 rounded-2xl border-2 border-purple-300 p-6">
    <img src={FEATURE2} alt="" />
    <div className="flex justify-center mb-4"></div>
    <h3 className="text-xl font-semibold mb-2">{icon} {title}</h3>
    <p className="text-gray-600">{description}</p>
  </div>
);

const ProductFeatures = () => {
  const features = [
    {
      title: "AI-Powered Inventory Optimization",
      description: "Utilize machine learning to predict trends and optimize your stock levels automatically.",
      icon: "📊"
    },
    {
      title: "Personalized Style Recommendations",
      description: "Offer customers tailored product suggestions based on their preferences and shopping history.",
      icon: "👗"
    },
    {
      title: "Trend Analysis Dashboard",
      description: "Visualize emerging fashion trends to inform your buying and marketing strategies.",
      icon: "📈"
    },
    {
      title: "Sustainable Fashion Insights",
      description: "Track and promote eco-friendly products to appeal to environmentally conscious consumers.",
      icon: "🌿"
    }
  ];

  return (
    <div className="px-4 mb-20" id='services'>
      <div className="max-w-5xl  mx-auto">
        <h2 className="text-4xl font-bold text-center mb-2">How <span className='text-violet-600 bg-orange-200 px-4 py-1 rounded-2xl text-indigo-400'>Clozette.AI</span> Empowers Your Fashion Business</h2>
        <p className="text-center text-gray-600 mb-8">Our platform helps you stay ahead in the fast-paced world of fashion retail.</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {features.map((feature, index) => (
            <FeatureCard key={index} {...feature} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProductFeatures;