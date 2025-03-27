<!-- src/views/LoginForm.vue -->
<template>
  <div class="container mt-5">
    <div class="hero">
      <div class="hero-content">
        <h1 class="neon-text">Login</h1>
        <form @submit.prevent="handleLogin" class="contact-form">
          <div class="form-group">
            <label for="email">E-Mail</label>
            <input
              type="email"
              id="email"
              v-model="form.email"
              class="form-control"
              placeholder="E-Mail eingeben"
              required
            />
          </div>
          <div class="form-group">
            <label for="password">Passwort</label>
            <input
              type="password"
              id="password"
              v-model="form.password"
              class="form-control"
              placeholder="Passwort eingeben"
              required
            />
          </div>
          <button type="submit" class="btn-neon-large">Einloggen</button>
        </form>
        <div v-if="error" class="form-feedback error mt-3">
          {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import emitter from '../utils/eventBus'  // Import the event bus

// Reaktive Variablen für Formulardaten und Fehlermeldung
const form = ref({
  email: '',
  password: ''
})
const error = ref('')

// Zugriff auf den Router
const router = useRouter()

// Event-Handler für den Login
const handleLogin = async () => {
  console.log("Login-Button wurde geklickt.");
  error.value = ''
  try {
    const response = await axios.post(
      'http://localhost:5000/api/login',
      form.value,
      { headers: { 'Content-Type': 'application/json' } }
    )
    console.log("Response vom Server:", response.data);
    // Stelle sicher, dass du den Token erst hier deklarierst und danach verwendest:
    const token = response.data.token;
    console.log("Erhaltener JWT-Token:", token);
    localStorage.setItem('authToken', token);
    
    // Emit an event to notify components about login
    emitter.emit('auth-change', { status: 'login' });
    
    alert("Login erfolgreich!");
    router.push('/dashboard');
  } catch (err) {
    console.error("Fehler beim Login:", err);
    if (err.response && err.response.data && err.response.data.message) {
      error.value = err.response.data.message;
    } else {
      error.value = 'Ein Fehler ist aufgetreten';
    }
  }
}
</script>


<style scoped>
/* Füge hier dein CSS für die Login-Seite hinzu */
</style>
