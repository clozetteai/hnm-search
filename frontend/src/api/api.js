
export const ApiClient = {
  search: async (query, type, page = 1, limit = 10) => {
    const response = await fetch(`http://localhost:8000/api/search?query=${query}&type=${type}&page=${page}&limit=${limit}`);
    if (!response.ok) throw new Error('Search failed');
    return response.json();
  },
  uploadImage: async (imageFile) => {
    const formData = new FormData();
    formData.append('image', imageFile);

    const response = await fetch('http://localhost:8000/api/upload-image', {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) throw new Error('Image upload failed');
    return response.json();
  },
  recordVoice: async (audioBlob) => {
    const formData = new FormData();
    formData.append('audio', audioBlob);

    const response = await fetch('http://localhost:8000/api/record-voice', {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) throw new Error('Voice record failed');
    return response.json();
  },
};

