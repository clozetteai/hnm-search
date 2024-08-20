import { API_ENDPOINT } from "./constant";

export const ApiClient = {
  // Helper function
  callApi: async (endpoint, method = 'GET', body = null, token = null, isFormData = false) => {
    const headers = {
      'Content-Type': isFormData ? 'application/x-www-form-urlencoded' : 'application/json',
    };
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    const config = { method, headers };
    if (body) {
      config.body = isFormData ? new URLSearchParams(body).toString() : JSON.stringify(body);
    }
    const response = await fetch(`${API_ENDPOINT}${endpoint}`, config);
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `API call failed: ${response.statusText}`);
    }
    return response.json();
  },
  // User Management
  createUser: (userData) => ApiClient.callApi('/api/users/', 'POST', userData),
  login: (username, password) => ApiClient.callApi('/api/login', 'POST', { username, password }, null, true),
  getCurrentUser: (token) => ApiClient.callApi('/api/users/me', 'GET', null, token),
  updateUserSettings: (token, settings) => ApiClient.callApi('/api/users/settings', 'PUT', settings, token),
  deleteUserAccount: (token) => ApiClient.callApi('/users/me', 'DELETE', null, token),
  changePassword: (token, currentPassword, newPassword, confirmNewPassword) => 
    ApiClient.callApi('/api/users/change-password', 'POST', {
      current_password: currentPassword,
      new_password: newPassword,
      confirm_new_password: confirmNewPassword
    }, token),

  // Chat Sessions
  createChatSession: (token, title) => ApiClient.callApi('/api/chat-sessions/', 'POST', { title }, token),
  listChatSessions: (token) => ApiClient.callApi('/api/chat-sessions/', 'GET', null, token),

  // Messages
  createMessage: (token, sessionId, content, messageType) =>
    ApiClient.callApi(`/chat-sessions/${sessionId}/messages/`, 'POST', { content, message_type: messageType }, token),
  listMessages: (token, sessionId) => ApiClient.callApi(`/api/chat-sessions/${sessionId}/messages/`, 'GET', null, token),

  // Bot Responses
  createBotResponse: (messageId, content, modelVersion, tokensUsed) =>
    ApiClient.callApi('/api/bot-responses/', 'POST', { message_id: messageId, content, model_version: modelVersion, tokens_used: tokensUsed }),

  // Feedback
  createFeedback: (token, messageId, rating, comment) =>
    ApiClient.callApi(`/api/messages/${messageId}/feedback`, 'POST', { rating, comment }, token),

  // API Keys
  createApiKey: (token) => ApiClient.callApi('/api/api-keys/', 'POST', null, token),
  listApiKeys: (token) => ApiClient.callApi('/api/api-keys/', 'GET', null, token),
  deleteApiKey: (token, keyId) => ApiClient.callApi(`/api/api-keys/${keyId}`, 'DELETE', null, token),

  // Prompt Templates
  createPromptTemplate: (name, content) => ApiClient.callApi('/api/prompt-templates/', 'POST', { name, content }),
  listPromptTemplates: () => ApiClient.callApi('/api/prompt-templates/'),

  // Subscriptions
  createSubscription: (token, planType) => ApiClient.callApi('/subscriptions/', 'POST', { plan_type: planType }, token),
  getCurrentSubscription: (token) => ApiClient.callApi('/subscriptions/current', 'GET', null, token),
  cancelSubscription: (token) => ApiClient.callApi('/subscriptions/cancel', 'DELETE', null, token),

  // Existing methods
  search: async (query, type, page = 1, limit = 10) => {
    const payload = { customer_message: query };
    const response = await fetch(`${API_ENDPOINT}/api/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error('Search failed');
    return new Promise((resolve) => {
      setTimeout(async () => {
        const result = await response.json();
        resolve(result);
      }, 5000);
    });
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