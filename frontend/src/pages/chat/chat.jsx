import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Loader } from 'lucide-react';
import { Header ,Footer, ProductCard, Sidebar, PromptCard } from '../../components';
import { ApiClient as apiClient }from '../../api/api';


const Chat = () => {
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
  // setChatSessions
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

  const handlePromptCardClick = (prompt) => {
    handleSearch(prompt, 'text');
  };

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar
        chatSessions={chatSessions}
        onSelectSession={handleSelectSession}
        activeSession={activeSession}
      />
      <div className="flex flex-col flex-grow">
        <Header />

        <main className="flex-grow overflow-auto p-4">
          {searchResults.length > 0 ? (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {searchResults.map((product, index) => (
                <div key={product.id} ref={index === searchResults.length - 1 ? lastProductElementRef : null}>
                  <ProductCard {...product} />
                </div>
              ))}
            </div>
          ) : (
            <div className="flex-grow mt-[15rem] flex items-center justify-center">
              <PromptCard handlePromptCardClick={handlePromptCardClick} />
            </div>
          )}
          {isLoading && (
            <div className="flex justify-center items-center p-4">
              <Loader className="animate-spin text-blue-500" size={48} />
            </div>
          )}
        </main>

        <Footer 
          botResponse={botResponse}
          setBotResponse={setBotResponse}
          handleImageUpload={handleImageUpload} 
          handleSearch={handleSearch}
          handleVoiceRecord={handleVoiceRecord}  
        />
      </div>
    </div>
  );
};

export default Chat;
