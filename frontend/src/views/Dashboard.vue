<template>
  <div class="container mt-5">
    <div class="hero">
      <div class="hero-content">
        <h1 class="neon-text">Dashboard</h1>
        <p>Willkommen, du bist eingeloggt und hast Zugriff auf geschützte Inhalte.</p>
        <button @click="fetchProtectedData" class="btn-neon-large">Daten abrufen</button>
        <div v-if="protectedData" class="mt-3">
          <h3 class="neon-text-pink">Geschützte Daten:</h3>
          <pre>{{ protectedData }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const protectedData = ref(null)

const fetchProtectedData = async () => {
  try {
    // Hol den JWT-Token aus dem LocalStorage
    const token = localStorage.getItem('authToken')
    // Sende einen GET-Request an den geschützten Endpoint
    const response = await axios.get('http://localhost:5000/api/protected', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    protectedData.value = response.data
  } catch (err) {
    console.error("Fehler beim Abrufen der geschützten Daten:", err)
    protectedData.value = { error: "Daten konnten nicht abgerufen werden." }
  }
}
</script>

<style scoped>
/* Optionale zusätzliche Styles für das Dashboard */
</style>
