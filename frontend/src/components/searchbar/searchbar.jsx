import React, { useState, useCallback, useRef } from 'react';
import { Image, Mic, Square, Play, X } from 'lucide-react';
import { API_ENDPOINT } from '../../api/constant';

const SearchBar = React.memo(({ onSearch, setBotResponse, onImageUpload, onVoiceRecord }) => {
  const [input, setInput] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const [uploadedImages, setUploadedImages] = useState([]);
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioRef = useRef(new Audio());

  const handleKeyPress = async (e) => {
    if (e.key === 'Enter' && (input.trim() !== '' || uploadedImages.length > 0)) {
      e.preventDefault();
      await handleSearch();
    }
  };

  const handleSearch = async () => {
    const formData = new FormData();
    formData.append('prompt', input);
    
    uploadedImages.forEach((image, index) => {
      // Convert base64 to blob
      const byteString = atob(image.split(',')[1]);
      const ab = new ArrayBuffer(byteString.length);
      const ia = new Uint8Array(ab);
      for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
      }
      const blob = new Blob([ab], { type: 'image/jpeg' });
      formData.append('images', blob, `image_${index}.jpg`);  // Changed key to 'images'
    });

    try {
      
      const response = await fetch(`${API_ENDPOINT}/api/search-by-image`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      console.log("/api/search-by-image: ", data)
      // setBotResponse(data.botResponse);

      console.log("this is the input: 1", input)
      // text search or (send the input: prompt)
      onSearch(input);
    } catch (error) {
      console.error('Error during search:', error);
    }
  
    // Clear the input and uploaded images after search
    setInput('');
    setUploadedImages([]);
  };

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleImageUpload(e.dataTransfer.files[0]);
    }
  };

  const handleImageUpload = (file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      setUploadedImages(prevImages => [...prevImages, e.target.result]);
    };
    reader.readAsDataURL(file);
  };

  const handleDeleteImage = (index) => {
    setUploadedImages(prevImages => prevImages.filter((_, i) => i !== index));
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        setAudioBlob(audioBlob);
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const cancelRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setAudioBlob(null);
    }
  };

  const playRecording = () => {
    if (audioBlob) {
      const audioUrl = URL.createObjectURL(audioBlob);
      audioRef.current.src = audioUrl;
      audioRef.current.play();
      setIsPlaying(true);
      audioRef.current.onended = () => setIsPlaying(false);
    }
  };

  const stopPlayback = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      setIsPlaying(false);
    }
  };

  return (
    <div className="flex flex-col items-start w-full">
      <div className="mb-2 flex flex-wrap gap-2">
        {uploadedImages.map((image, index) => (
          <div key={index} className="relative">
            <img src={image} alt={`Uploaded ${index + 1}`} className="h-20 w-20 object-cover rounded-lg" />
            <button
              onClick={() => handleDeleteImage(index)}
              className="absolute -top-2 -right-2 bg-white rounded-full p-1 shadow-md text-red-500 hover:text-red-700 focus:outline-none"
            >
              <X size={16} />
            </button>
          </div>
        ))}
      </div>
      <div 
        className={`w-full flex items-center bg-white rounded-full p-2 shadow-md relative ${dragActive ? 'border-2 border-blue-500' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <button
          onClick={() => document.getElementById('imageUpload').click()}
          className="text-gray-700 p-2 rounded-full hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-300 transition-colors duration-300"
        >
          <Image size={24} />
        </button>
        <input
          id="imageUpload"
          type="file"
          accept="image/*"
          onChange={(e) => handleImageUpload(e.target.files[0])}
          className="hidden"
        />
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Search products..."
          className="flex-grow mx-2 bg-transparent focus:outline-none"
        />
        {isRecording ? (
          <button
            onClick={stopRecording}
            className="text-red-500 p-2 rounded-full hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-red-300 transition-colors duration-300"
          >
            <Square size={24} />
          </button>
        ) : audioBlob ? (
          <button
            onClick={isPlaying ? stopPlayback : playRecording}
            className="text-green-500 p-2 rounded-full hover:bg-green-100 focus:outline-none focus:ring-2 focus:ring-green-300 transition-colors duration-300"
          >
            {isPlaying ? <Square size={24} /> : <Play size={24} />}
          </button>
        ) : (
          <button
            onClick={startRecording}
            className="text-gray-700 p-2 rounded-full hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-300 transition-colors duration-300"
          >
            <Mic size={24} />
          </button>
        )}
        {isRecording && (
          <button
            onClick={cancelRecording}
            className="ml-2 text-gray-500 p-2 rounded-full hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-300 transition-colors duration-300"
          >
            <X size={24} />
          </button>
        )}
      </div>
    </div>
  );
});

export default SearchBar;