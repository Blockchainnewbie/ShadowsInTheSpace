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

// Bootstrap-CSS
import 'bootstrap/dist/css/bootstrap.min.css'

// Dein eigenes CSS
import './assets/main.css'

// Lokale Schriften - Korrekter Import aus dem src-Verzeichnis
import './assets/fonts/fonts.css'; // <-- ÄNDERN! Kein / am Anfang, kein ?url


createApp(App)
  .use(router)
  .mount('#app')
