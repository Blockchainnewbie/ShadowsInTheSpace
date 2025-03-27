<template>
  <section class="hero">
    <div class="hero-content">
      <h1 class="neon-text">ShadowsInThe.Space</h1>

      <div class="status-indicator">
        <div class="status-dot"></div>
        <div class="status-text">System Online</div>
      </div>

      <div class="vision-wrapper">
        <div class="vision-text">
          <h2 class="neon-text-pink">Willkommen im Cyberpunk-Universum</h2>
          <p>
            **🌌 Welcome to Shadows in the Space 🌌**<br>

            In den verborgenen Winkeln der digitalen Welt, wo Realität und virtuelle Schatten verschwimmen, entsteht
            etwas Neues.<br>
            Etwas, das die Grenzen zwischen Mensch und Maschine verschwinden lässt.<br>

            **ShadowsInThe.space**<br>
            ist mehr als nur eine AI Agency. Es ist dein Zugang zu ungeahnten Möglichkeiten – ein
            Ort, an dem Künstliche Intelligenz nicht nur Probleme löst, sondern Ideen Wirklichkeit werden lässt.<br>
            Wir gestalten Zukunft, formen innovative Lösungen und beschreiten gemeinsam Wege, die zuvor undenkbar
            erschienen.<br>
            <br>
            Neugierig geworden? Die Schatten beginnen sich zu bewegen.<br>
            <br>

            Bleib dran, denn bald wird aus Dunkelheit Klarheit, und du erfährst, wie wir mit intelligenter Technologie
            deine Visionen zum Leben erwecken. 🔥🤖<br>
            <br>

            **🚀 Let's shape the future together! 🚀**
            <br>
          </p>

          <div class="cyber-link">
            <div class="center-content">
              <router-link to="/about" class="btn-neon-large">Entdecke mehr</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="grid-overlay"></div>
  </section>
</template>

<script setup>
/**
 * Landing Page Component
 * 
 * SOLID - Single Responsibility Principle:
 * This component has the single responsibility of being the main landing page
 * and providing the initial user experience.
 * 
 * SOLID - Interface Segregation Principle:
 * The component provides only the functionality needed for a landing page
 * without dependencies on other areas of the application.
 */
</script>

<style scoped>
/**
 * Component-specific styles would go here,
 * following the Single Responsibility Principle.
 */

/* Fix hero height to account for footer */
.hero {
  min-height: 100vh;
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
  background: linear-gradient(45deg, rgba(10, 10, 10, 0.5), rgba(0, 13, 25, 0.5));
}

.hero-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  padding-bottom: 1rem;
  position: relative; /* Wichtig für die Positionierung der Linien */
  z-index: 2; /* Stellt sicher, dass der Inhalt über dem Grid-Overlay liegt */
}

/* Keep border lines visible on hover */
.vision-wrapper {
  flex: 1;
  display: flex;
  overflow: visible;
  position: relative;
}

.vision-wrapper::before,
.vision-wrapper::after {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  width: 1px;
  background: rgba(255, 0, 80, 0.7);
  pointer-events: none;
  z-index: 5; /* Stellt sicher, dass die Linien über dem vision-text liegen */
}

.vision-wrapper::before {
  left: 0;
}

.vision-wrapper::after {
  right: 0;
}

.vision-text {
  margin-top: 0rem;
  margin-bottom: 0rem;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  transition: all 0.3s ease;
}

.vision-text:hover {
  transform: scale(1.02);
  box-shadow: 0 0 20px var(--neon-pink); /* Entferne den box-shadow vom vision-text */
}

/* Verbesserte Positionierung für den Button */
.cyber-link {
  margin-top: 2rem;
  margin-bottom: 2rem; /* Reduzierter Abstand nach unten */
  position: relative;
  z-index: 10; /* Höherer z-index als der Footer */
}

.cyber-link .center-content {
  padding-bottom: 2rem; /* Reduzierter Abstand nach unten */
}

/* Hervorhebung des Buttons */
.cyber-link .btn-neon-large {
  box-shadow: 0 0 15px var(--neon-purple); /* Stärkerer Glüh-Effekt */
  transform: scale(1.05); /* Etwas größer */
  transition: all 0.3s ease;
}

.cyber-link .btn-neon-large:hover {
  transform: scale(1.1); /* Noch größer beim Hover */
  box-shadow: 0 0 25px var(--neon-purple); /* Stärkerer Glüh-Effekt beim Hover */
}
</style>
