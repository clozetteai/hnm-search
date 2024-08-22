import React, { useState } from 'react';
import { APPLOGO, APPLOGO400 } from '../../assets';
import { Faq, GetInTouch, OurTeam, PricingCard, ProductFeatures } from '../../components';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/auth';
import { ApiClient } from '../../api/api';
import { motion } from 'framer-motion';

const Header = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [loadingButton, setLoadingButton] = useState(null);
  const [error, setError] = useState(null);

  const handleNav = async (path, buttonType) => {
    setLoadingButton(buttonType);
    setError(null);
    try {
      login("newuser5", "password123");
      setTimeout(() => {
        setLoadingButton(null);
        navigate(path);
      }, 1000); // 1 second delay, adjust as needed
    } catch (err) {
      setError(err.message || 'An error occurred during login');
      setLoadingButton(null);
    }
  };
  return (
    <header className="py-4 px-6">
      <div className="container mx-auto flex items-center justify-between">
        <div className="flex items-center">
          <img src={APPLOGO} className="h-10" alt="" />
          <span className="text-2xl font-medium text-gray-800">Clozette.AI</span>
        </div>
        <nav>
          <ul className="flex space-x-20">
            <li><a href="#services" className="text-gray-600 hover:text-gray-800">Services</a></li>
            <li><a href="#pricing" className="text-gray-600 hover:text-gray-800">Pricing</a></li>
            <li><a href="#about" className="text-gray-600 hover:text-gray-800">About us</a></li>
          </ul>
        </nav>
        <div className="">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => handleNav("chat", "login")}
            className="text-violet-500 px-4 py-2 border-2 rounded-md border-violet-500 hover:bg-violet-50 transition duration-300"
            disabled={loadingButton === "login"}
          >
            {loadingButton === "login" ? 'Loading...' : 'Log In'}
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => handleNav("chat", "start")}
            className="ml-5 bg-violet-500 text-white px-4 py-2 rounded-md hover:bg-orange-500 transition duration-300"
            disabled={loadingButton === "start"}
          >
            {loadingButton === "start" ? 'Loading...' : 'Start for Free'}
          </motion.button>
        </div>
      </div>
      {loadingButton && (
        <div className="fixed top-0 left-0 w-full h-1 bg-violet-200">
          <div className="h-full bg-violet-500 animate-pulse" style={{ width: '50%' }}></div>
        </div>
      )}
      {error && (
        <div className="fixed top-16 left-0 w-full bg-red-500 text-white p-2 text-center">
          {error}
        </div>
      )}
    </header>
  );
};

const Hero = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
      className="flex mt-[16rem] mb-[20rem] justify-center"
    >
      <div className="text-center">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.5, type: "spring", stiffness: 260, damping: 20 }}
          className="mb-8"
        >
          {/* <img src={APPLOGO400} className='h-[10rem] mx-auto' alt='' /> */}
        </motion.div>
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7, duration: 0.5 }}
          className="text-2xl md:text-5xl font-bold mb-4"
        >
          We speak <span className="bg-blue-200 px-2 py-1 rounded-2xl text-indigo-500">SQL</span>,
        </motion.h1>
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9, duration: 0.5 }}
          className="text-2xl md:text-4xl lg:text-5xl font-bold"
        >
          so you can speak <span className='bg-orange-200 px-2 py-1 rounded-2xl text-red-400'>Fashion.</span>
        </motion.h1>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.1, duration: 0.5 }}
          className='mx-auto w-[50rem] mt-10 text-xl text-gray-500'
        >
          The future of fashion search is here. With Clozette.AI,
          your natural language descriptions become powerful SQL queries, unlocking a world of clothing possibilities.
        </motion.p>
      </div>
    </motion.div>
  );
};
const Footer = () => (
  <footer className="py-12 px-6 mt-16">
    <div className="container mx-auto">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        {/* Logo and social links */}
        <div className="flex flex-col items-start">
          <div className="flex items-center mb-4">
            <img src={APPLOGO} className='h-10' alt="" />
            <span className="text-xl font-bold text-gray-800">Clozette.AI</span>
          </div>
          <div className="flex space-x-4 mt-4">
            <a href="/" className="text-gray-400 hover:text-gray-600">
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path fillRule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clipRule="evenodd" />
              </svg>
            </a>
            <a href="/" className="text-gray-400 hover:text-gray-600">
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
              </svg>
            </a>
            <a href="/" className="text-gray-400 hover:text-gray-600">
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path fillRule="evenodd" d="M12.315 2c2.43 0 2.784.013 3.808.06 1.064.049 1.791.218 2.427.465a4.902 4.902 0 011.772 1.153 4.902 4.902 0 011.153 1.772c.247.636.416 1.363.465 2.427.048 1.067.06 1.407.06 4.123v.08c0 2.643-.012 2.987-.06 4.043-.049 1.064-.218 1.791-.465 2.427a4.902 4.902 0 01-1.153 1.772 4.902 4.902 0 01-1.772 1.153c-.636.247-1.363.416-2.427.465-1.067.048-1.407.06-4.123.06h-.08c-2.643 0-2.987-.012-4.043-.06-1.064-.049-1.791-.218-2.427-.465a4.902 4.902 0 01-1.772-1.153 4.902 4.902 0 01-1.153-1.772c-.247-.636-.416-1.363-.465-2.427-.047-1.024-.06-1.379-.06-3.808v-.63c0-2.43.013-2.784.06-3.808.049-1.064.218-1.791.465-2.427a4.902 4.902 0 011.153-1.772A4.902 4.902 0 015.45 2.525c.636-.247 1.363-.416 2.427-.465C8.901 2.013 9.256 2 11.685 2h.63zm-.081 1.802h-.468c-2.456 0-2.784.011-3.807.058-.975.045-1.504.207-1.857.344-.467.182-.8.398-1.15.748-.35.35-.566.683-.748 1.15-.137.353-.3.882-.344 1.857-.047 1.023-.058 1.351-.058 3.807v.468c0 2.456.011 2.784.058 3.807.045.975.207 1.504.344 1.857.182.466.399.8.748 1.15.35.35.683.566 1.15.748.353.137.882.3 1.857.344 1.054.048 1.37.058 4.041.058h.08c2.597 0 2.917-.01 3.96-.058.976-.045 1.505-.207 1.858-.344.466-.182.8-.398 1.15-.748.35-.35.566-.683.748-1.15.137-.353.3-.882.344-1.857.048-1.055.058-1.37.058-4.041v-.08c0-2.597-.01-2.917-.058-3.96-.045-.976-.207-1.505-.344-1.858a3.097 3.097 0 00-.748-1.15 3.098 3.098 0 00-1.15-.748c-.353-.137-.882-.3-1.857-.344-1.023-.047-1.351-.058-3.807-.058zM12 6.865a5.135 5.135 0 110 10.27 5.135 5.135 0 010-10.27zm0 1.802a3.333 3.333 0 100 6.666 3.333 3.333 0 000-6.666zm5.338-3.205a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4z" clipRule="evenodd" />
              </svg>
            </a>
          </div>
        </div>

        {/* About Us and Support */}
        <div>
          <h3 className="text-lg font-semibold mb-4">About Us</h3>
          <ul className="space-y-2">
            <li><a href="/" className="text-gray-600 hover:text-gray-800">Our Story</a></li>
            <li><a href="/" className="text-gray-600 hover:text-gray-800">Team</a></li>
            <li><a href="/" className="text-gray-600 hover:text-gray-800">Careers</a></li>
          </ul>
        </div>

        {/* Support and Feedback */}
        <div>
          <h3 className="text-lg font-semibold mb-4">Support</h3>
          <ul className="space-y-2">
            <li><a href="/" className="text-gray-600 hover:text-gray-800">Help Center</a></li>
            <li><a href="/" className="text-gray-600 hover:text-gray-800">FAQs</a></li>
            <li><a href="/" className="text-gray-600 hover:text-gray-800">Feedback</a></li>
          </ul>
        </div>

        {/* Contact Us */}
        <div>
          <h3 className="text-lg font-semibold mb-4">Contact Us</h3>
          <ul className="space-y-2">
            <li className="text-gray-600">Email: support@clozette.ai</li>
            <li className="text-gray-600">Phone: +1 (555) 123-4567</li>
            <li className="text-gray-600">Address: 123 AI Street, Tech City, 12345</li>
          </ul>
        </div>
      </div>

      {/* Copyright */}
      <div className="mt-12 pt-8 border-t border-gray-200 text-center text-gray-500">
        <p>&copy; 2024 Clozette.AI. All rights reserved.</p>
      </div>
    </div>
  </footer>
)

const HeroPopOvers = () => {
  return (
    <div className="relative mt-16">

      <motion.div
        className="absolute top-[5rem] left-[20.5rem] w-[15rem] bg-amber-200 p-6 rounded-lg shadow-lg"
        whileHover={{ scale: 1.05 }}
        initial={{ opacity: 0, x: -100 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.2 }}
      >
        <h3 className="text-lg font-semibold mb-2">🏆 Rewards from brands you love</h3>
        <p>Discover and earn with your favorite fashion brands.</p>
      </motion.div>

      <motion.div
        className="absolute top-[28rem] left-[28rem] w-[15rem] bg-sky-300 p-6 rounded-lg shadow-lg"
        whileHover={{ scale: 1.05 }}
        initial={{ opacity: 0, y: 100 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <h3 className="text-lg font-semibold mb-2">🦾 Smart Search Technology</h3>
        <p>Our AI understands your style preferences.</p>
      </motion.div>

      <motion.div
        className="absolute top-[8rem] right-[12rem] w-[15rem] bg-green-300 p-6 rounded-lg shadow-lg"
        whileHover={{ scale: 1.05 }}
        initial={{ opacity: 0, x: 100 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.6 }}
      >
        <h3 className="text-lg font-semibold mb-2">🧥 We take your fashion seriously</h3>
        <p>Curated results that match your unique style.</p>
      </motion.div>
    </div>
  )
}


const Landing = () => {
  return (
    <div className='min-h-screen bg-gradient-to-br from-purple-100 via-pink-100 to-orange-100'>
      {/* Header */}
      <Header />
      {/* Hero Section */}
      <HeroPopOvers />
      <Hero />

      {/* Hero Section ENDED*/}

      {/* Product Feature */}
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        viewport={{ once: true }}
      >
        <ProductFeatures />
      </motion.div>

      {/* Pricing Plans */}
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        viewport={{ once: true }}
      >
        <PricingCard />
      </motion.div>

      {/* Get in Touch */}
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        viewport={{ once: true }}
      >
        <GetInTouch />
      </motion.div>

      {/* Our Team */}
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        viewport={{ once: true }}
      >
        <OurTeam />
      </motion.div>

      {/* FAQs */}
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        viewport={{ once: true }}
      >
        <Faq />
      </motion.div>

      <Footer />
    </div>
  )
}

export default Landing;