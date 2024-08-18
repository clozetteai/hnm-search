import React from 'react';

const GetInTouch = () => {
  return (
    <div className="max-w-6xl mx-auto my-20">
      <div className="flex rounded-xl overflow-hidden">
        {/* Dark section */}
        <div className="bg-black text-white p-12 flex-1">
          <h2 className="text-4xl font-bold mb-4">
            It's time to revolutionize your fashion business
          </h2>
          <p className="text-gray-400 mb-8">
            Elevate your brand's performance with AI-driven insights and recommendations.
          </p>
          <button className="bg-white text-black px-6 py-3 rounded-full font-semibold hover:bg-gray-200 transition duration-300">
            Get in touch →
          </button>
        </div>

        {/* Light section */}
        <div className="bg-white p-12 flex-1">
          <div className="flex justify-between mb-8">
            <div className="w-2 h-2 bg-gray-300 rounded-full"></div>
            <div className="w-2 h-2 bg-gray-300 rounded-full"></div>
            <div className="w-2 h-2 bg-gray-300 rounded-full"></div>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-purple-600 mb-2">Clozette.AI</h3>
            <h4 className="text-2xl font-bold mb-4">
              We're ready to transform your fashion retail experience.
            </h4>
            <p className="text-gray-600 mb-6">
              Join the AI revolution in fashion. Our platform provides cutting-edge solutions for inventory management, trend prediction, and personalized customer experiences.
            </p>
            <div className="flex items-center text-sm text-gray-500 mb-6">
              <span className="mr-2">✓</span>
              <span>AI-powered insights at your fingertips</span>
            </div>
            <button className="bg-black text-white px-6 py-3 rounded-md font-semibold hover:bg-gray-800 transition duration-300">
              Learn more
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GetInTouch;