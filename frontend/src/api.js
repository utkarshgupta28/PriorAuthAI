import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

const API = axios.create({ baseURL: import.meta.env.VITE_API_URL
    ? `${import.meta.env.VITE_API_URL}/api`
    : 'http://localhost:8000/api' })

export const getCases = () => API.get('/cases')
export const getDemoPresets = () => API.get('/demo-presets')
export const getCase = (id) => API.get(`/cases/${id}`)
export const createCase = (data) => API.post('/cases', data)
export const deleteCase = (id) => API.delete(`/cases/${id}`)
export const runPipeline = (id, demo = false, scenario = '') =>
  API.post(`/cases/${id}/run`, null, { params: { demo, scenario } })
export const submitApplication = (id, draft) =>
  API.post(`/cases/${id}/submit`, { draft })
export const simulateDenial = (id) => API.post(`/cases/${id}/deny`)
export const simulateApproval = (id) => API.post(`/cases/${id}/approve`)
export const getCaseOutputs = (id) => API.get(`/cases/${id}/outputs`)
export const getCaseInsights = (id) => API.get(`/cases/${id}/insights`)
export const getMetrics = () => API.get('/metrics')
