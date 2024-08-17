import React, { useState, useEffect, useCallback } from 'react';
import { Loader, ShoppingBag } from 'lucide-react';

const Sidebar = React.memo(() => {
  const chatSessions = [
    { id: 1, title: "First Search" },
    { id: 2, title: "Product Inquiry" },
    { id: 3, title: "Size Comparison" },
  ];

  return (
    <div className="w-64 bg-gray-800 text-white p-4">
      <h2 className="text-xl font-bold mb-4">Chat Sessions</h2>
      <ul>
        {chatSessions.map((session) => (
          <li key={session.id} className="mb-2">
            <button className="w-full text-left p-2 hover:bg-gray-700 rounded">
              {session.title}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
});

const apiClient = {
  fetchCatalog: async (page = 1, limit = 10) => {
    const response = await fetch(`http://localhost:8000/catalog?page=${page}&limit=${limit}`);
    if (!response.ok) throw new Error('Failed to fetch catalog');
    return response.json();
  },
  search: async (message, page = 1, limit = 10) => {
    const response = await fetch('http://localhost:8000/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, page, limit }),
    });
    if (!response.ok) throw new Error('Search failed');
    return response.json();
  },
};

const ProductCard = React.memo(({ title, price, imageUrl }) => (
  <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300">
    <img src={imageUrl} alt={title} className="w-full h-48 object-cover" />
    <div className="p-4">
      <h3 className="text-lg font-semibold truncate">{title}</h3>
      <p className="text-xl font-bold text-green-600">{price}</p>
      <button className="mt-2 w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition-colors duration-300 flex items-center justify-center">
        <ShoppingBag size={18} className="mr-2" />
        Add to Cart
      </button>
    </div>
  </div>
));

const SearchBar = React.memo(({ onSearch, isConversationMode }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSearch(input);
      setInput('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-center bg-white rounded-full p-2 shadow-md">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder={isConversationMode ? "Chat with AI..." : "Search products..."}
        className="flex-grow mx-2 bg-transparent focus:outline-none"
      />
      <button type="submit" className="p-2 rounded-full bg-blue-500 text-white hover:bg-blue-600 transition-colors duration-300">
        {isConversationMode ? "Send" : "Search"}
      </button>
    </form>
  );
});

const AICompanySearch = () => {
  const [products, setProducts] = useState([]);
  const [botResponse, setBotResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [isConversationMode, setIsConversationMode] = useState(false);
  const [conversationHistory, setConversationHistory] = useState([]);

  const fetchCatalog = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await apiClient.fetchCatalog();
      setProducts(data.products);
      setBotResponse(data.bot_response);
    } catch (error) {
      console.error('Failed to fetch catalog:', error);
      setBotResponse('Sorry, there was an error loading the catalog.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchCatalog();
  }, [fetchCatalog]);

  const handleSearch = async (message) => {
    setIsLoading(true);
    setIsConversationMode(true);
    try {
      const data = await apiClient.search(message);
      setConversationHistory(prev => [...prev, { role: 'user', content: message }, { role: 'assistant', content: data.bot_response }]);
      
      if (data.conversation_output && data.conversation_output.conversation_ended) {
        setBotResponse("Great! I'm now searching for products based on our conversation. This might take a moment...");
        setIsSearching(true);
        // Simulate a delay to show the searching message
        setTimeout(() => {
          setProducts(data.products || []);
          setBotResponse(data.bot_response);
          setIsConversationMode(false);
          setIsSearching(false);
        }, 1000); // Adjust this delay as needed
      } else {
        setBotResponse(data.bot_response);
      }
    } catch (error) {
      console.error('Search failed:', error);
      setBotResponse('Sorry, there was an error processing your request.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setIsConversationMode(false);
    setConversationHistory([]);
    fetchCatalog();
  };

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      <div className="flex flex-col flex-grow">
        <header className="bg-white p-4 shadow-md z-10">
          <h1 className="text-2xl font-bold text-blue-600">Company.ai</h1>
          {(isConversationMode || isSearching) && (
            <button onClick={handleReset} className="mt-2 text-blue-500 hover:underline">
              Back to Catalog
            </button>
          )}
        </header>

        <main className="flex-grow overflow-auto p-4">
          {isLoading || isSearching ? (
            <div className="flex flex-col justify-center items-center h-full">
              <Loader className="animate-spin text-blue-500 mb-4" size={48} />
              {isSearching && <p>Searching for products based on our conversation...</p>}
            </div>
          ) : (
            <>
              {isConversationMode ? (
                <div className="space-y-4 mb-4">
                  {conversationHistory.map((msg, index) => (
                    <div key={index} className={`p-2 rounded-lg ${msg.role === 'user' ? 'bg-blue-100 text-right' : 'bg-gray-100'}`}>
                      {msg.content}
                    </div>
                  ))}
                </div>
              ) : (
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                  {products.map((product) => (
                    <ProductCard key={product.id} {...product} />
                  ))}
                </div>
              )}
            </>
          )}
        </main>

        <footer className="bg-white p-4 shadow-md z-10">
          <div className="bg-gray-100 rounded-t-3xl p-4">
            {botResponse && (
              <div className="bg-white p-4 rounded-lg mb-4 shadow-md">
                <p className="font-semibold">{botResponse}</p>
              </div>
            )}
            <SearchBar onSearch={handleSearch} isConversationMode={isConversationMode} />
          </div>
        </footer>
      </div>
    </div>
  );
};

export default AICompanySearch;
