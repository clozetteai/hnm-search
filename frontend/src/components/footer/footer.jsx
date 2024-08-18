import React from 'react';
import SearchBar from '../searchbar/searchbar';

const Footer = ({ botResponse, setBotResponse, handleSearch, handleImageUpload, handleVoiceRecord }) => {
  return (
    <footer className=" p-4 pt-6 sticky bottom-0 z-10">
      <div className=" rounded-t-3xl p-4 pb-8">
        {botResponse && (
          <div className="bg-white p-4 rounded-lg mb-4 shadow-md">
            <p className="font-semibold">{botResponse.split('\n\n')[0]}</p>
            <p>{botResponse.split('\n\n')[1]}</p>
          </div>
        )}
        <SearchBar
          setBotResponse={setBotResponse}
          onSearch={handleSearch}
          onImageUpload={handleImageUpload}
          onVoiceRecord={handleVoiceRecord}
        />
      </div>
    </footer>
  )
}

export default Footer;