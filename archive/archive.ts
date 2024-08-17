import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Image, Mic, Loader, ShoppingBag } from 'lucide-react';
import Sidebar from './Sidebar';

// API client (to be replaced with actual API calls)
const apiClient = {
  search: async (query, type, page = 1, limit = 10) => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    const totalProducts = 100; // Simulating a large number of products
    const products = Array.from({ length: limit }, (_, i) => ({
      id: (page - 1) * limit + i + 1,
      title: `Product ${(page - 1) * limit + i + 1}`,
      price: (Math.random() * 100).toFixed(2),
      imageUrl: `/api/placeholder/300/300?text=Product${(page - 1) * limit + i + 1}`,
    }));
    return {
      products,
      totalProducts,
      botResponse: `Here is what I found for "${query}"\n\nI've found some great options for you. Let me know if you need more details!`,
    };
  },
  uploadImage: async (imageFile) => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    return { success: true, message: 'Image uploaded successfully' };
  },
  recordVoice: async (audioBlob) => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    return { success: true, message: 'Voice recorded successfully' };
  },
};

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

const SearchBar = React.memo(({ onSearch, onImageUpload, onVoiceRecord }) => {
  const [input, setInput] = useState('');

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && input.trim() !== '') {
      onSearch(input, 'text');
    }
  };

  return (
    <div className="flex justify-between items-center bg-white rounded-full p-2 shadow-md">
      <button
        onClick={onImageUpload}
        className="text-gray-700 p-2 rounded-full hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-300 transition-colors duration-300"
      >
        <Image size={24} />
      </button>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Search products..."
        className="flex-grow mx-2 bg-transparent focus:outline-none"
      />
      <button
        onClick={onVoiceRecord}
        className="text-gray-700 p-2 rounded-full hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-300 transition-colors duration-300"
      >
        <Mic size={24} />
      </button>
    </div>
  );
});

const AICompanySearch = () => {
  const [searchResults, setSearchResults] = useState([]);
  const [botResponse, setBotResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const observer = useRef();
  const [query, setQuery] = useState('');
  const [searchType, setSearchType] = useState('text');

  const lastProductElementRef = useCallback(node => {
    if (isLoading) return;
    if (observer.current) observer.current.disconnect();
    observer.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && hasMore) {
        setPage(prevPage => prevPage + 1);
      }
    });
    if (node) observer.current.observe(node);
  }, [isLoading, hasMore]);

  const handleSearch = useCallback(async (newQuery, type) => {
    setIsLoading(true);
    setQuery(newQuery);
    setSearchType(type);
    setPage(1);
    setSearchResults([]);
    try {
      const response = await apiClient.search(newQuery, type);
      setSearchResults(response.products);
      setBotResponse(response.botResponse);
      setHasMore(response.products.length === 10);
    } catch (error) {
      console.error('Search failed:', error);
      setBotResponse('Sorry, there was an error processing your request.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    if (page > 1) {
      const fetchMoreProducts = async () => {
        setIsLoading(true);
        try {
          const response = await apiClient.search(query, searchType, page);
          setSearchResults(prev => [...prev, ...response.products]);
          setHasMore(response.products.length === 10);
        } catch (error) {
          console.error('Failed to fetch more products:', error);
        } finally {
          setIsLoading(false);
        }
      };
      fetchMoreProducts();
    }
  }, [page, query, searchType]);

  const handleImageUpload = async () => {
    // Implementation remains the same
  };

  const handleVoiceRecord = async () => {
    // Implementation remains the same
  };


  const [chatSessions, setChatSessions] = useState([
    { id: 1, title: "First Search" },
    { id: 2, title: "Product Inquiry" },
    { id: 3, title: "Size Comparison" },
  ]);
  const [activeSession, setActiveSession] = useState(1);

  const handleSelectSession = (sessionId) => {
    setActiveSession(sessionId);
    // Here you would typically load the chat history for the selected session
    // For now, we'll just update the botResponse
    setBotResponse(`You've selected chat session ${sessionId}`);
  };



  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar
        chatSessions={chatSessions}
        onSelectSession={handleSelectSession}
        activeSession={activeSession}
      />
      <div className="flex flex-col flex-grow">
        <header className="bg-white p-4 shadow-md sticky top-0 z-10">
          <h1 className="text-2xl font-bold text-blue-600">Company.ai</h1>
        </header>
        
        <main className="flex-grow overflow-auto p-4">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {searchResults.map((product, index) => (
              <div key={product.id} ref={index === searchResults.length - 1 ? lastProductElementRef : null}>
                <ProductCard {...product} />
              </div>
            ))}
          </div>
          {isLoading && (
            <div className="flex justify-center items-center p-4">
              <Loader className="animate-spin text-blue-500" size={48} />
            </div>
          )}
        </main>
        
        <footer className="bg-white p-4 pt-6 sticky bottom-0 z-10">
          <div className="bg-gray-100 rounded-t-3xl p-4 pb-8">
            {botResponse && (
              <div className="bg-white p-4 rounded-lg mb-4 shadow-md">
                <p className="font-semibold">{botResponse.split('\n\n')[0]}</p>
                <p>{botResponse.split('\n\n')[1]}</p>
              </div>
            )}
            <SearchBar 
              onSearch={handleSearch}
              onImageUpload={handleImageUpload}
              onVoiceRecord={handleVoiceRecord}
            />
          </div>
        </footer>
      </div>
    </div>
  );
};
export default AICompanySearch;
