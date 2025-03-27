// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import Impressum from '../views/Impressum.vue'
import DSGVO from '../views/DSGVO.vue'
import About from '../views/About.vue'
import Dashboard from '../views/Dashboard.vue'
import LoginForm from '../views/LoginForm.vue'

const routes = [
  { path: '/', component: LandingPage },
  { path: '/impressum', component: Impressum },
  { path: '/dsgvo', component: DSGVO },
  { path: '/about', component: About },
  { path: '/dashboard', component: Dashboard },
  { path: '/login', component: LoginForm }
]

// Erstelle die Router-Instanz
const router = createRouter({
  history: createWebHistory(),
  routes
})

// Hier fügst du den Navigation Guard hinzu
router.beforeEach((to, from, next) => {
  if (to.path === '/dashboard' && !localStorage.getItem('authToken')) {
    next('/login')
  } else {
    next()
  }
})

export default router
