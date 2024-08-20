

const Landing = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 via-pink-100 to-orange-100 p-8">
      <header className="flex justify-between items-center mb-16">
        <div className="flex items-center">
          <img src={APPLOGO} className="h-10 mr-2" alt="Clozette.AI Logo" />
          <span className="text-2xl font-medium text-gray-800">Clozette.AI</span>
        </div>
        <nav>
          <ul className="flex space-x-8">
            <li><a href="#services" className="text-gray-600 hover:text-gray-800">Services</a></li>
            <li><a href="#pricing" className="text-gray-600 hover:text-gray-800">Pricing</a></li>
            <li><a href="#about" className="text-gray-600 hover:text-gray-800">About us</a></li>
          </ul>
        </nav>
        <div>
          <button className="text-violet-500 px-4 py-2 border-2 rounded-md border-violet-500 hover:bg-violet-50 transition duration-300 mr-4">
            Log In
          </button>
          <button className="bg-violet-500 text-white px-4 py-2 rounded-md hover:bg-orange-500 transition duration-300">
            Start for Free
          </button>
        </div>
      </header>

      <main className="text-center mb-16">
        <h1 className="text-5xl font-bold mb-4">The Future of Fashion Search</h1>
        <p className="text-xl text-gray-600 mb-8">
          Enjoy Frictionless Fashion Discovery With Clozette.AI's Advanced Search
          <br />Get Up To 100% Accurate Results
        </p>

        <div className="flex justify-center mb-8">
          <input
            type="email"
            placeholder="Your Email Address"
            className="px-4 py-2 w-64 rounded-l-md focus:outline-none focus:ring-2 focus:ring-violet-500"
          />
          <button className="bg-black text-white px-6 py-2 rounded-r-md hover:bg-gray-800 transition duration-300">
            Get Started
          </button>
        </div>

        <p className="text-sm text-gray-500">*No personal guarantee or personal credit check required.</p>

        <div className="relative mt-16">
          <motion.div
            className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-72 h-72"
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <img src="/path-to-your-phone-image.png" alt="Phone" className="w-full h-full object-contain" />
          </motion.div>

          <motion.div
            className="absolute top-0 left-0 bg-yellow-200 p-6 rounded-lg shadow-lg"
            whileHover={{ scale: 1.05 }}
            initial={{ opacity: 0, x: -100 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <h3 className="text-lg font-semibold mb-2">Rewards from brands you love</h3>
            <p>Discover and earn with your favorite fashion brands.</p>
          </motion.div>

          <motion.div
            className="absolute bottom-0 left-1/4 bg-red-200 p-6 rounded-lg shadow-lg"
            whileHover={{ scale: 1.05 }}
            initial={{ opacity: 0, y: 100 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <h3 className="text-lg font-semibold mb-2">Smart Search Technology</h3>
            <p>Our AI understands your style preferences.</p>
          </motion.div>

          <motion.div
            className="absolute top-1/4 right-0 bg-green-200 p-6 rounded-lg shadow-lg"
            whileHover={{ scale: 1.05 }}
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
          >
            <h3 className="text-lg font-semibold mb-2">We take your fashion seriously</h3>
            <p>Curated results that match your unique style.</p>
          </motion.div>
        </div>
      </main>
    </div>
  );
};