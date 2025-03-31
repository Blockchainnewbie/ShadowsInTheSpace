<script setup>
/**
 * Root Application Component
 * 
 * SOLID - Single Responsibility Principle:
 * This component has the single responsibility of setting up the main application layout.
 * 
 * SOLID - Dependency Inversion Principle:
 * The component depends on abstractions (Navbar and Footer components) rather than concrete implementations.
 */
import { ref, onMounted } from 'vue';
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';
import CookieConsent from './components/CookieConsent.vue';
import portraitShadows from './assets/portraitShadows.webp';
import portraitShadows2 from './assets/portraitShadows2.webp';
import emitter from './utils/eventBus';

// Reference for the CookieConsent dialog
const cookieConsentRef = ref(null);

onMounted(() => {
  // Event listener with mitt
  emitter.on('open-cookie-settings', () => {
    cookieConsentRef.value.resetConsent();
  });
});
</script>

<template>
  <div class="app-container">
    <Navbar />
    <main>
      <div class="image-container">
        <img :src="portraitShadows" alt="Portrait Shadows 1">
        <img :src="portraitShadows2" alt="Portrait Shadows 2">
        <div class="hero-overlay">
          <router-view />
        </div>
      </div>
    </main>
    <Footer />
    <!-- Cookie Banner -->
    <CookieConsent ref="cookieConsentRef" />
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
  overflow: visible;
}

main {
  flex: 1;
  height: 100%;
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
}

.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  min-height: 100vh;
  height: 100%;
  overflow: hidden;
  position: relative;
  z-index: 2;
}

/* Image styles */
.image-container img {
  max-width: 50%;
  height: 100vh;
  object-fit: cover;
  object-position: center;
  display: block;
  position: absolute;
  top: 0;
  left: 0;
  width: 50%;
  z-index: 1;
}

.image-container img:nth-child(2) {
  left: auto;
  right: 0;
}

/* Media queries */
@media (max-width: 768px) {
  .image-container img {
    max-width: 100%;
    width: 100%;
    height: 50vh;
    position: relative;
  }
  
  .image-container {
    flex-direction: column;
  }
  
  .image-container img:nth-child(2) {
    position: relative;
    right: auto;
  }
  
  .hero-overlay {
    position: relative;
    height: auto;
    min-height: 50vh;
  }
}
</style>