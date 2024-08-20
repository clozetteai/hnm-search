import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Loader } from 'lucide-react';
import { 
  Header,
  Footer, 
  ProductCard, 
  Sidebar, 
  PromptCard 
} from '../../components';
import { ApiClient as apiClient } from '../../api/api';
import { useAuth } from '../../contexts/auth';

const Chat = () => {
  const { user } = useAuth();
  const [searchResults, setSearchResults] = useState([]);
  const [botResponse, setBotResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const observer = useRef();
  const [query, setQuery] = useState('');
  const [searchType, setSearchType] = useState('text');
  const [chatSessions, setChatSessions] = useState([]);
  const [activeSession, setActiveSession] = useState(null);
  const [sessionMessages, setSessionMessages] = useState([]);

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
      console.log(newQuery)
      const response = await apiClient.search(newQuery, type);
      console.log(response)
      // setSearchResults(response);
      // setBotResponse(response.botResponse);
      // setHasMore(response.products.length === 10);
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

  useEffect(() => {
    const fetchChatSessions = async () => {
      if (user && user.token) {
        try {
          const sessions = await apiClient.listChatSessions(user.token);
          console.log(sessions)
          setChatSessions(sessions);
          if (sessions.length > 0) {
            setActiveSession(sessions[0].session_id);
          }
        } catch (error) {
          console.error('Failed to fetch chat sessions:', error);
        }
      }
    };
    fetchChatSessions();
  }, [user]);

  const handleImageUpload = async (imageFile) => {
    try {
      const response = await apiClient.uploadImage(imageFile);
      // Handle the response
    } catch (error) {
      console.error('Image upload failed:', error);
    }
  };

  const handleVoiceRecord = async (audioBlob) => {
    try {
      const response = await apiClient.recordVoice(audioBlob);
      // Handle the response
    } catch (error) {
      console.error('Voice record failed:', error);
    }
  };

  const handleSelectSession = async (sessionId) => {
    setActiveSession(sessionId);
    if (user && user.token) {
      try {
        const messages = await apiClient.listMessages(user.token, sessionId);
        setSessionMessages(messages);
        if (messages.length > 0) {
          setBotResponse(messages[messages.length - 1].content);
        }
      } catch (error) {
        console.error('Failed to fetch session messages:', error);
        setBotResponse('Failed to load chat history.');
      }
    }
  };

  const handlePromptCardClick = (prompt) => {
    handleSearch(prompt, 'text');
  };

  const createNewChatSession = async (title) => {
    if (user && user.token) {
      try {
        const newSession = await apiClient.createChatSession(user.token, title);
        setChatSessions(prevSessions => [...prevSessions, newSession]);
        setActiveSession(newSession.session_id);
      } catch (error) {
        console.error('Failed to create new chat session:', error);
      }
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar
        chatSessions={chatSessions}
        onSelectSession={handleSelectSession}
        activeSession={activeSession}
        onCreateNewSession={createNewChatSession}
      />
      <div className="flex flex-col flex-grow">
        <Header />

        <main className="flex-grow overflow-auto p-4">
          {sessionMessages.length > 0 ? (
            <div className="space-y-4">
              {sessionMessages.map((message) => (
                <div key={message.message_id} className={`p-2 rounded ${message.message_type === 'user' ? 'bg-blue-100' : 'bg-green-100'}`}>
                  {message.content}
                </div>
              ))}
            </div>
          ) : searchResults.length > 0 ? (
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