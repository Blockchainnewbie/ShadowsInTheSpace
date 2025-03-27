import axios from 'axios'
import emitter from '../utils/eventBus'

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: parseInt(import.meta.env.VITE_API_TIMEOUT || '30000'),
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// Request interceptor for API calls
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(import.meta.env.VITE_AUTH_TOKEN_NAME || 'authToken')
    if (token) {
      config.headers[import.meta.env.VITE_AUTH_HEADER_NAME || 'Authorization'] = 
        `${import.meta.env.VITE_AUTH_TOKEN_PREFIX || 'Bearer'} ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for API calls
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    const originalRequest = error.config
    
    // Handle 401 Unauthorized errors (token expired)
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      // Clear token and notify components
      localStorage.removeItem(import.meta.env.VITE_AUTH_TOKEN_NAME || 'authToken')
      emitter.emit('auth-change', { status: 'logout', reason: 'session-expired' })
      
      // You could also implement token refresh logic here
    }
    
    return Promise.reject(error)
  }
)

// External services
export const externalServices = {
  rss2json: axios.create({
    baseURL: import.meta.env.VITE_RSS2JSON_API_URL,
    timeout: 10000
  })
}

// API endpoints
export const endpoints = {
  auth: {
    login: '/login',
    register: '/register',
    logout: '/logout',
    refreshToken: '/refresh-token'
  },
  user: {
    profile: '/user/profile',
    settings: '/user/settings'
  },
  posts: {
    list: '/posts',
    single: (id) => `/posts/${id}`,
    create: '/posts',
    update: (id) => `/posts/${id}`,
    delete: (id) => `/posts/${id}`
  }
}

// Mock data for RSS feed
// const mockFeedItems = [
//   {
//     title: "Neue Cybersecurity-Bedrohungen entdeckt",
//     pubDate: new Date().toISOString(),
//     link: "https://example.com/news/1",
//     description: "Sicherheitsexperten haben eine neue Welle von Cyberangriffen identifiziert, die auf kritische Infrastrukturen abzielen."
//   },
//   {
//     title: "KI-Durchbruch in der Quantenkryptographie",
//     pubDate: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
//     link: "https://example.com/news/2",
//     description: "Forscher haben einen KI-Algorithmus entwickelt, der Quantenverschlüsselung effizienter machen könnte."
//   },
//   {
//     title: "Neues Framework für dezentrale Anwendungen veröffentlicht",
//     pubDate: new Date(Date.now() - 172800000).toISOString(), // 2 days ago
//     link: "https://example.com/news/3",
//     description: "Ein neues Open-Source-Framework verspricht, die Entwicklung dezentraler Anwendungen zu vereinfachen."
//   },
//   {
//     title: "Globaler Tech-Gipfel kündigt neue Standards an",
//     pubDate: new Date(Date.now() - 259200000).toISOString(), // 3 days ago
//     link: "https://example.com/news/4",
//     description: "Führende Technologieunternehmen haben sich auf neue Standards für IoT-Geräte geeinigt."
//   },
//   {
//     title: "Durchbruch bei erneuerbaren Energiespeichern",
//     pubDate: new Date(Date.now() - 345600000).toISOString(), // 4 days ago
//     link: "https://example.com/news/5",
//     description: "Wissenschaftler haben eine neue Batterietechnologie entwickelt, die erneuerbare Energie effizienter speichern kann."
//   }
// ];

// Helper for RSS feed
export const fetchRssFeed = async (feedUrl = import.meta.env.VITE_RSS_FEED_URL, count = 5) => {
  console.log('fetchRssFeed called with URL:', feedUrl)
  console.log('RSS2JSON API URL:', import.meta.env.VITE_RSS2JSON_API_URL)
  console.log('RSS2JSON API Key:', import.meta.env.VITE_RSS2JSON_API_KEY ? 'Key exists' : 'Key missing')
  
  try {
    console.log('Making API request to RSS2JSON service')
    const response = await externalServices.rss2json.get('', {
      params: {
        rss_url: feedUrl,
        api_key: import.meta.env.VITE_RSS2JSON_API_KEY,
        count: count
      }
    })
    console.log('RSS2JSON response received:', response.status)
    return response.data.items
  } catch (error) {
    console.error('RSS feed error details:', {
      message: error.message,
      response: error.response ? {
        status: error.response.status,
        data: error.response.data
      } : 'No response',
      config: error.config ? {
        url: error.config.url,
        params: error.config.params
      } : 'No config'
    })
    throw error
  }
}

export default apiClient
