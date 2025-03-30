<template>
  <footer class="footer">
    <div class="container">
      <div class="row">
        <div class="col-md-6">
          <p>© 2025 ShadowsInThe.Space</p>
        </div>
        <div class="col-md-6 text-md-end">
          <router-link to="/impressum" class="footer-link">Impressum</router-link> | 
          <router-link to="/dsgvo" class="footer-link">Datenschutzerklärung</router-link>
        </div>
      </div>
      <div class="cookie-settings">
        <button @click="openCookieSettings" class="cookie-settings-btn">
          <span class="cyber-bracket">[</span>Cookie-Einstellungen<span class="cyber-bracket">]</span>
        </button>
      </div>
    </div>
  </footer>
</template>

<script setup>

</script>

<script>
import emitter from '../utils/eventBus'

export default {
  methods: {
    openCookieSettings() {
      // Cookie-Banner über Event-Bus öffnen
      emitter.emit('open-cookie-settings');
    }
  }
}
</script>

<style scoped>

.footer {
  padding: 1rem 0;
  /* background-color: transparent; /* Entferne den schwarzen Hintergrund */
  border-top: 2px solid var(--neon-cyan); /* Verstärke den türkisen Streifen */
  position: relative;
  z-index: 1; /* Niedrigerer z-index als der Button */
  margin-top: 2rem; /* Weniger Abstand zum Inhalt */
  bottom: 0; /* Am unteren Rand fixieren */
  width: 100%; /* Volle Breite */
  height: 50px; /* Feste Höhe */
  box-shadow: 0 -5px 15px rgba(0, 255, 240, 0.3); /* Türkiser Glüh-Effekt nach oben */
}

.footer p {
  color: var(--neon-cyan); /* Ändere die Textfarbe zu türkis für bessere Sichtbarkeit */
  text-shadow: 0 0 5px rgba(0, 255, 240, 0.5); /* Füge einen leichten Glüh-Effekt hinzu */
}

.footer-link {
  color: var(--neon-cyan);
  text-decoration: none;
  transition: all 0.3s ease;
  margin-left: 0.5rem;
}

.footer-link:hover {
  text-shadow: 0 0 8px var(--neon-cyan);
}

.cookie-settings {
  margin-top: 1rem;
  text-align: center;
}

.cookie-settings-btn {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s;
}

.cookie-settings-btn:hover {
  color: var(--neon-cyan);
}

.cyber-bracket {
  color: var(--neon-cyan);
  opacity: 0.5;
  transition: opacity 0.3s;
}

.cookie-settings-btn:hover .cyber-bracket {
  opacity: 1;
}
</style>