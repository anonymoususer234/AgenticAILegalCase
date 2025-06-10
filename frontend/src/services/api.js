import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const legalApi = {
  research: async (query) => {
    const response = await api.post('/research', query);
    return response.data;
  },

  validateQuery: async (query) => {
    const response = await api.post('/validate-query', query);
    return response.data;
  },

  getHealth: async () => {
    const response = await api.get('/health');
    return response.data;
  },

  getAgentsStatus: async () => {
    const response = await api.get('/agents/status');
    return response.data;
  },

  searchDocuments: async (query, k = 5) => {
    const response = await api.get('/search', {
      params: { query, k }
    });
    return response.data;
  },

  addDocuments: async (documents, metadata) => {
    const response = await api.post('/add-documents', {
      documents,
      metadata
    });
    return response.data;
  }
};

export default legalApi; 