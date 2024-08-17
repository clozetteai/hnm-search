import React, { useState, useCallback } from 'react';
import { Image, Mic, X } from 'lucide-react';

const SearchBar = React.memo(({ onSearch, onImageUpload, onVoiceRecord }) => {
  const [input, setInput] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const [uploadedImages, setUploadedImages] = useState([]);

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && input.trim() !== '') {
      onSearch(input, 'text');
    }
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
      onImageUpload(file);
    };
    reader.readAsDataURL(file);
  };

  const handleDeleteImage = (index) => {
    setUploadedImages(prevImages => prevImages.filter((_, i) => i !== index));
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
        <button
          onClick={onVoiceRecord}
          className="text-gray-700 p-2 rounded-full hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-300 transition-colors duration-300"
        >
          <Mic size={24} />
        </button>
      </div>
    </div>
  );
});

export default SearchBar;