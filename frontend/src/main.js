// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

/**
 * Application entry point
 * 
 * SOLID - Single Responsibility Principle:
 * This file has the single responsibility of bootstrapping the Vue application.
 * 
 * SOLID - Dependency Inversion Principle:
 * The application depends on abstractions (router, App component) rather than
 * concrete implementations, facilitating easier testing and maintenance.
 */

// Import order is important for CSS precedence
// Import Bootstrap CSS FIRST
import 'bootstrap/dist/css/bootstrap.min.css'

// Import our custom CSS AFTER Bootstrap to override Bootstrap styles
import './assets/main.css'

// Import local fonts
import './assets/fonts/fonts.css'

// Create and mount the Vue application
const app = createApp(App)
app.use(router)
app.mount('#app')

// Apply a CSS override to force text colors after mounting
// This ensures our styles override Bootstrap even in production
document.addEventListener('DOMContentLoaded', () => {
  // Force our CSS variables to override Bootstrap
  document.documentElement.style.setProperty('--bs-body-color', '#ffffff', 'important')
  document.documentElement.style.setProperty('--bs-body-bg', '#000913', 'important')
  
  // Apply the CSS override to ensure footer has transparent background
  const footerElements = document.querySelectorAll('.footer')
  footerElements.forEach(footer => {
    footer.style.backgroundColor = 'transparent'
    footer.style.color = '#00fff0'
  })
})