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

<script>
import emitter from '../utils/eventBus';

export default {
  methods: {
    openCookieSettings() {
      // Open cookie banner via event bus
      emitter.emit('open-cookie-settings');
    }
  }
};
</script>

<style scoped>
.footer {
  padding: 1rem 0;
  background-color: transparent;
  border-top: 2px solid var(--neon-cyan);
  position: relative;
  z-index: 1;
  margin-top: 2rem;
  width: 100%;
  height: 50px;
  box-shadow: 0 -5px 15px var(--neon-cyan-transparent);
}

.footer p,
.footer a,
.footer button,
.footer span {
  color: var(--neon-cyan);
  text-shadow: 0 0 5px var(--neon-cyan-transparent);
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
  color: var(--text-muted);
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s;
}

.cookie-settings-btn:hover {
  color: var(--neon-cyan) !important;
}

.cyber-bracket {
  color: var(--neon-cyan) !important;
  opacity: 0.5;
  transition: opacity 0.3s;
}

.cookie-settings-btn:hover .cyber-bracket {
  opacity: 1;
}
</style>
