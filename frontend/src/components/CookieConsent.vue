<template>
  <div v-if="isVisible" class="cookie-banner" :class="{ 'settings-open': showSettings }">
    <div class="cookie-banner-inner">
      <!-- Hauptbanner -->
      <div v-if="!showSettings" class="consent-main">
        <div class="consent-title">
          <h2>// DEINE DATENSCHUTZ-EINSTELLUNGEN</h2>
        </div>
        <p>
          Diese Website verwendet Cookies, um deine Erfahrung zu verbessern. Einige Cookies sind technisch notwendig,
          während andere für Analysezwecke verwendet werden.
          <router-link to="/dsgvo" class="cyber-link">Mehr erfahren</router-link>
        </p>
        <div class="consent-buttons">
          <button @click="acceptAll" class="consent-btn accept-all">ALLE AKZEPTIEREN</button>
          <button @click="acceptEssential" class="consent-btn essential-only">NUR NOTWENDIGE</button>
          <button @click="showSettings = true" class="consent-btn customize">EINSTELLUNGEN</button>
        </div>
      </div>
      
      <!-- Detaillierte Einstellungen -->
      <div v-else class="consent-settings">
        <div class="consent-title">
          <h2>// COOKIE-EINSTELLUNGEN</h2>
          <button @click="showSettings = false" class="back-btn">&lt; Zurück</button>
        </div>
        
        <div class="cookie-categories">
          <!-- Notwendige Cookies - immer aktiviert -->
          <div class="cookie-category">
            <div class="category-header">
              <h3>Notwendige Cookies</h3>
              <label class="cyber-switch disabled">
                <input type="checkbox" checked disabled>
                <span class="slider"></span>
              </label>
            </div>
            <p>Diese Cookies sind für das Funktionieren der Website unerlässlich und können nicht deaktiviert werden.</p>
          </div>
          
          <!-- Analytics Cookies -->
          <div class="cookie-category">
            <div class="category-header">
              <h3>Analyse-Cookies</h3>
              <label class="cyber-switch">
                <input v-model="consents.analytics" type="checkbox">
                <span class="slider"></span>
              </label>
            </div>
            <p>Diese Cookies ermöglichen uns, die Nutzung der Website zu analysieren und das Benutzererlebnis zu verbessern.</p>
            <div class="cookie-details">
              <div class="cookie-detail">
                <strong>Google Analytics</strong>
                <p>Zweck: Analysieren der Website-Nutzung</p>
                <p>Speicherdauer: 14 Monate</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="settings-buttons">
          <button @click="saveSettings" class="consent-btn save-settings">SPEICHERN</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { initializeGoogleAnalytics, disableGoogleAnalytics } from '../utils/analytics'

// GA4 Measurement ID als Konstante
const GA_MEASUREMENT_ID = 'G-9ZZWW1DGPQ';

const isVisible = ref(true)
const showSettings = ref(false)
const consents = ref({
  essential: true,
  analytics: false
})

// Prüfen, ob Nutzer bereits Einwilligungen gespeichert hat
onMounted(() => {
  const savedConsent = localStorage.getItem('cookieConsent');
  if (savedConsent) {
    try {
      const parsedConsent = JSON.parse(savedConsent);
      consents.value = { ...consents.value, ...parsedConsent };
      isVisible.value = false;
      
      // Google Analytics NUR aktivieren, wenn Einwilligung vorliegt
      if (consents.value.analytics) {
        enableGoogleAnalytics();
      }
    } catch (e) {
      console.error('Error parsing cookie consent', e);
    }
  }
})

// Fehlende Click-Handler Methoden
const acceptAll = () => {
  consents.value.analytics = true;
  saveConsent();
  enableGoogleAnalytics();
}


const saveSettings = () => {
  saveConsent();
  if (consents.value.analytics) {
    enableGoogleAnalytics();
  } else {
    disableGoogleAnalyticsTracker();
  }
}

// Hilfsfunktionen
const saveConsent = () => {
  localStorage.setItem('cookieConsent', JSON.stringify(consents.value));
  isVisible.value = false;
}

const enableGoogleAnalytics = () => {
  initializeGoogleAnalytics(GA_MEASUREMENT_ID);
}

const disableGoogleAnalyticsTracker = () => {
  disableGoogleAnalytics(GA_MEASUREMENT_ID);
}

const acceptEssential = () => {
  consents.value.analytics = false;
  saveConsent();
  disableGoogleAnalyticsTracker(); // Analytics explizit deaktivieren
}

const resetConsent = () => {
  localStorage.removeItem('cookieConsent')
  isVisible.value = true
  showSettings.value = false
  consents.value.analytics = false
  disableGoogleAnalyticsTracker()
}

// Diese Methode für externe Aufrufe zugänglich machen
defineExpose({
  resetConsent
})
</script>

<style scoped>
.cookie-banner {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.95);
  z-index: 9999;
  border-top: 2px solid var(--neon-cyan);
  box-shadow: 0 -5px 15px rgba(0, 255, 255, 0.3);
}

.cookie-banner-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem;
  color: white;
}

.consent-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.consent-title h2 {
  color: var(--neon-cyan);
  font-size: 1.5rem;
  font-family: 'ShareTechMono', monospace;
  margin: 0;
}

.consent-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1.5rem;
}

.consent-btn {
  padding: 0.6rem 1.2rem;
  border: none;
  font-family: 'ShareTechMono', monospace;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s;
  letter-spacing: 1px;
}

.accept-all {
  background-color: var(--neon-cyan);
  color: black;
}

.accept-all:hover {
  background-color: #fff;
  box-shadow: 0 0 10px var(--neon-cyan);
}

.essential-only {
  background-color: transparent;
  border: 1px solid var(--neon-cyan);
  color: var(--neon-cyan);
}

.essential-only:hover {
  background-color: rgba(0, 255, 255, 0.1);
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.customize {
  background-color: transparent;
  border: 1px solid white;
  color: white;
}

.customize:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.back-btn {
  background: none;
  border: none;
  color: var(--neon-cyan);
  cursor: pointer;
  font-family: 'ShareTechMono', monospace;
}

.cookie-categories {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin: 1.5rem 0;
}

.cookie-category {
  border: 1px solid rgba(0, 255, 255, 0.3);
  padding: 1rem;
  background-color: rgba(0, 0, 0, 0.5);
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.category-header h3 {
  color: var(--neon-cyan);
  margin: 0;
  font-size: 1.1rem;
}

.cyber-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.cyber-switch input { 
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #333;
  transition: .4s;
  border-radius: 24px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: #fff;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: var(--neon-cyan);
}

input:focus + .slider {
  box-shadow: 0 0 1px var(--neon-cyan);
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.cyber-switch.disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.cookie-details {
  margin-top: 1rem;
  border-top: 1px dashed rgba(255, 255, 255, 0.2);
  padding-top: 0.5rem;
}

.cookie-detail {
  margin-bottom: 0.5rem;
}

.cookie-detail strong {
  color: var(--neon-pink);
  display: block;
  margin-bottom: 0.25rem;
}

.cookie-detail p {
  margin: 0.25rem 0;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
}

.cyber-link {
  color: var(--neon-cyan);
  text-decoration: none;
}

.cyber-link:hover {
  text-decoration: underline;
  text-shadow: 0 0 5px var(--neon-cyan);
}

.save-settings {
  background-color: var(--neon-cyan);
  color: black;
}

.settings-buttons {
  display: flex;
  justify-content: center;
}

/* Responsive Design */
@media (max-width: 768px) {
  .consent-buttons {
    flex-direction: column;
  }
}
</style>
