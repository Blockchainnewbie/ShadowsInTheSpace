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

  // Referenz für den CookieConsent-Dialog
  const cookieConsentRef = ref(null);

  onMounted(() => {
    // Event-Listener mit mitt
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
    <!-- Cookie-Banner -->
    <CookieConsent ref="cookieConsentRef" />
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh; /* Ensure the container takes up at least the full viewport height */
  display: flex;      /* Use flexbox for layout */
  flex-direction: column; /* Stack children vertically */
  height: 100%; /* Nimmt die volle Höhe ein */
  position: relative; /* Für korrekte Positionierung der Kinder-Elemente */
  overflow: visible; /* Verhindert das Abschneiden von Inhalten */
}

main {
  flex: 1; /* Allow the main content to grow and fill available space */
  height: 100%; /* Nimmt die volle Höhe ein */
  position: relative; /* Für korrekte Positionierung */
  z-index: 2; /* Höher als der Footer */
  display: flex; /* Flexbox für die Anordnung der Inhalte */
  flex-direction: column; /* Inhalte vertikal anordnen */
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

/* Style für die Bilder */
.image-container img {
    max-width: 50%;
    height: 100vh;
    object-fit: cover;
    object-position: center;
    display: block;
    position: absolute; /* Bilder absolut positionieren */
    top: 0;
    left: 0;
    width: 50%; /* Jedes Bild nimmt 50% der Breite ein */
    z-index: 1; /* Bilder hinter dem Overlay */
}

.image-container img:nth-child(2) {
    left: auto; /* Zweites Bild rechts positionieren */
    right: 0;
}

</style>
