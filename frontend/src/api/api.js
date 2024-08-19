import { API_ENDPOINT } from "./constant";

export const ApiClient = {
  search: async (query, type, page = 1, limit = 10) => {
    console.log(API_ENDPOINT)
    // TODO ENDPOINT NEED TO BE CHANGED /api/search
    const response = await fetch(`${API_ENDPOINT}/api/catalouge`);
    if (!response.ok) throw new Error('Search failed');
    return response.json();
  },
  uploadImage: async (imageFile) => {
    const formData = new FormData();
    formData.append('image', imageFile);

    const response = await fetch(`${API_ENDPOINT}/api/upload-image`, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) throw new Error('Image upload failed');
    return response.json();
  },
  recordVoice: async (audioBlob) => {
    const formData = new FormData();
    formData.append('audio', audioBlob);

    const response = await fetch(`${API_ENDPOINT}/api/record-voice`, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) throw new Error('Voice record failed');
    return response.json();
  },
};

