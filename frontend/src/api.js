// Version 1.0
// Time: Wed Dec 10,17:15
// frontend 


import axios from 'axios';

const api = axios.create({ baseURL: '/api' });
// Bingtian Qiao:核心功能
export default {
    getAll: () => api.get('/contacts'),
    create: (data) => api.post('/contacts', data),
    update: (id, data) => api.put(`/contacts/${id}`, data),
    delete: (id) => api.delete(`/contacts/${id}`),
    import: (formData) => api.post('/contacts/import', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
    }),
    export: () => api.get('/contacts/export', { responseType: 'blob' })
};