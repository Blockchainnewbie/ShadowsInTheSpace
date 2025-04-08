<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark cyberpunk-nav">
      <div class="container">
        <!-- Logo mit Glitch-Effekt -->
        <router-link class="navbar-brand cyberpunk-logo" to="/">
          <span class="glitch-text" data-text="ShadowsInThe.Space"
            >ShadowsInThe.Space</span
          >
        </router-link>

        <!-- RSS Feed Icon -->
        <button @click="toggleFeed" class="cyberpunk-btn me-3">
          <i class="bi bi-rss-fill"></i>
          <span class="cyber-glow">FEED</span>
        </button>

        <!-- Navbar toggler -->
        <button
          class="navbar-toggler cyber-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="toggler-icon"></span>
        </button>

        <!-- Navigation Links -->
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/about">About</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/impressum"
                >Impressum</router-link
              >
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/dsgvo">DSGVO</router-link>
            </li>
            <!-- Zeige den Login-Link nur, wenn der Nutzer NICHT eingeloggt ist -->
            <li class="nav-item" v-if="!isLoggedIn">
              <router-link class="nav-link" to="/login">Login</router-link>
            </li>
            <!-- Zeige den Dashboard-Link nur, wenn der Nutzer eingeloggt ist -->
            <li class="nav-item" v-if="isLoggedIn">
              <router-link class="nav-link" to="/dashboard"
                >Dashboard</router-link
              >
            </li>
            <!-- Logout-Link nur anzeigen, wenn eingeloggt -->
            <li class="nav-item" v-if="isLoggedIn">
              <a class="nav-link" href="#" @click.prevent="handleLogout"
                >Logout</a
              >
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- RSS Feed Panel -->
    <div class="cyber-feed-panel" :class="{ 'feed-active': feedActive }">
      <div class="cyber-feed-header">
        <h3 class="cyber-feed-title">// INCOMING TRANSMISSIONS</h3>
        <button @click="toggleFeed" class="cyber-close-btn">&times;</button>
      </div>
      <div class="cyber-feed-content">
        <div v-if="loading" class="cyber-loading">
          <div class="scanner"></div>
          <p>SCANNING NETWORKS...</p>
        </div>
        <div v-else-if="feedError" class="cyber-error">
          <p>SIGNAL DISRUPTION: {{ feedError }}</p>
        </div>
        <div v-else-if="feedItems.length === 0" class="cyber-empty">
          <p>NO TRANSMISSIONS DETECTED</p>
        </div>
        <div v-else class="cyber-feed-items">
          <div
            v-for="(item, index) in feedItems"
            :key="index"
            class="cyber-feed-item"
          >
            <div class="feed-time">{{ formatDate(item.pubDate) }}</div>
            <h4 class="feed-title">{{ item.title }}</h4>
            <p class="feed-desc">{{ truncateText(item.description, 100) }}</p>
            <a :href="item.link" target="_blank" class="nav-link-small"
              >READ MORE &gt;&gt;</a
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * Navigation Bar Component
 *
 * SOLID - Single Responsibility Principle:
 * This component has the single responsibility of providing site navigation.
 *
 * SOLID - Open/Closed Principle:
 * The navbar is structured to be easily extended with new navigation items
 * without modifying the existing component structure.
 * // Wenn du Logik zur bedingten Anzeige (z. B. abhängig vom Auth-Status) implementieren möchtest, kannst du das hier ergänzen.
 */
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";
import emitter from "../utils/eventBus";
import authService from "../services/auth";
import { fetchRssFeed } from "../services/api";

// Computed-Property: Prüfe, ob ein Token im LocalStorage existiert
const isLoggedIn = ref(authService.isAuthenticated());

// Update the auth state when localStorage changes
const updateAuthState = () => {
  isLoggedIn.value = authService.isAuthenticated();
};

// Listen for auth change events
onMounted(() => {
  emitter.on("auth-change", updateAuthState);
});

// Clean up event listener when component unmounts
onBeforeUnmount(() => {
  emitter.off("auth-change", updateAuthState);
});

const router = useRouter();

// Logout-Funktion: Entfernt den JWT-Token und navigiert zur Login-Seite
const handleLogout = () => {
  authService.logout();
  router.push("/login");
};

// Feed state
const feedActive = ref(false);
const feedItems = ref([]);
const loading = ref(false);
const feedError = ref(null);

// Toggle feed visibility
const toggleFeed = () => {
  console.log("toggleFeed called, current state:", feedActive.value);
  feedActive.value = !feedActive.value;
  console.log("toggleFeed new state:", feedActive.value);

  if (feedActive.value && feedItems.value.length === 0) {
    loadFeed();
  }
};

// Fetch RSS feed
const loadFeed = async () => {
  console.log("loadFeed called");
  loading.value = true;
  feedError.value = null;

  try {
    console.log("Attempting to fetch RSS feed");
    feedItems.value = await fetchRssFeed();
    console.log("RSS feed fetched successfully:", feedItems.value);
  } catch (error) {
    console.error("Error fetching RSS feed:", error);
    feedError.value = error.message;
  } finally {
    console.log("loadFeed completed, loading state:", loading.value);
    loading.value = false;
  }
};

// Helper functions
const truncateText = (text, maxLength) => {
  const strippedText = text.replace(/<[^>]*>?/gm, "");
  return strippedText.length > maxLength
    ? strippedText.substring(0, maxLength) + "..."
    : strippedText;
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return `${date.getDate().toString().padStart(2, "0")}.${(date.getMonth() + 1)
    .toString()
    .padStart(2, "0")}.${date.getFullYear()}`;
};
</script>

<style scoped>
/* Cyberpunk Navbar */
.cyberpunk-nav {
  background: var(--darker-bg);
  border-bottom: 2px solid var(--neon-cyan);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
  font-family: "Orbitron", sans-serif;
  position: relative;
  z-index: 100;
  height: 75px;
}

.navbar-brand {
  font-family: "Orbitron", sans-serif;
  font-size: 1.8rem;
}

/* Logo with glitch effect */
.cyberpunk-logo {
  font-weight: bold;
  position: relative;
  letter-spacing: 1px;
}

.glitch-text {
  position: relative;
  color: var(--neon-cyan);
  text-shadow: 0 0 5px var(--neon-cyan), 0 0 10px rgba(255, 0, 208, 0.8);
}

.glitch-text::before,
.glitch-text::after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0.8;
}

.glitch-text::before {
  color: var(--neon-magenta);
  z-index: -2;
  animation: glitch 0.7s cubic-bezier(0.25, 0.46, 0.45, 0.94) both infinite;
  animation-delay: 1s;
}

.glitch-text::after {
  color: var(--neon-yellow);
  z-index: -1;
  animation: glitch 0.7s cubic-bezier(0.25, 0.46, 0.45, 0.94) reverse both
    infinite;
  animation-delay: 1s;
}

@keyframes glitch {
  0% {
    transform: translate(0);
  }
  20% {
    transform: translate(-2px, 2px);
  }
  40% {
    transform: translate(-2px, -2px);
  }
  60% {
    transform: translate(2px, 2px);
  }
  80% {
    transform: translate(2px, -2px);
  }
  100% {
    transform: translate(0);
  }
}

/* Nav Links */
.nav-link {
  color: white !important;
  font-weight: 500;
  letter-spacing: 1px;
  position: relative;
  top: 15px;
  text-decoration: none;
  left: 0;
  transition: all 0.3s;
  padding: 0.5rem 0.75rem !important;
}

.cyber-bracket {
  color: var(--neon-cyan);
  opacity: 0;
  transition: all 0.3s;
}
.nav-link:hover .cyber-bracket,
.router-link-active .cyber-bracket {
  opacity: 1;
} 

.nav-link:hover,
.nav-link.router-link-active {
  /* .router-link-active bleibt, da es von Vue Router kommt */
  color: var(--neon-cyan) !important; /* Prüfe, ob !important nötig ist */
  text-shadow: 0 0 8px var(--neon-cyan); /* Der Glow */
  /* Ggf. !important hinzufügen, falls Bootstrap den Shadow überschreibt */
  /* text-shadow: 0 0 8px var(--neon-cyan) !important; */
  background: rgba(0, 255, 255, 0.05);
}

/* Custom Toggler */
.cyber-toggler {
  border: 1px solid var(--neon-cyan) !important;
  padding: 0.25rem 0.5rem;
}

.toggler-icon {
  display: block;
  width: 24px;
  height: 2px;
  background: var(--neon-cyan);
  position: relative;
}

.toggler-icon::before,
.toggler-icon::after {
  content: "";
  position: absolute;
  width: 24px;
  height: 2px;
  background: var(--neon-cyan);
  left: 0;
}

.toggler-icon::before {
  top: -8px;
}

.toggler-icon::after {
  bottom: -8px;
}

/* RSS Feed Button */
.cyberpunk-btn {
  background: transparent;
  color: var(--neon-yellow);
  border: 1px solid var(--neon-yellow);
  padding: 0.25rem 0.75rem;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.cyberpunk-btn:hover {
  background: rgba(255, 255, 0, 0.1);
  box-shadow: 0 0 10px rgba(255, 255, 0, 0.5);
}

.cyber-glow {
  font-size: 0.8rem;
  letter-spacing: 1px;
}

/* Feed Panel */
.cyber-feed-panel {
  position: fixed;
  top: 56px;
  right: -350px;
  width: 350px;
  height: calc(100vh - 56px);
  background: #030308;
  border-left: 2px solid var(--neon-yellow);
  transition: right 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  z-index: 99;
  display: flex;
  flex-direction: column;
}

.feed-active {
  right: 0;
  box-shadow: -5px 0 15px rgba(0, 0, 0, 0.5);
}

.cyber-feed-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.3);
  border-bottom: 2px solid var(--neon-yellow);
}

.cyber-feed-title {
  color: var(--neon-yellow);
  font-size: 1rem;
  margin: 0;
  font-family: "Courier New", monospace;
}

.cyber-close-btn {
  background: transparent;
  border: none;
  color: var(--neon-yellow);
  font-size: 1.5rem;
  cursor: pointer;
}

.cyber-feed-content {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

/* Feed Items */
.cyber-feed-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.cyber-feed-item {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 0, 0.3);
  padding: 0.75rem;
  position: relative;
  padding-top: 1.5rem; /* Mehr Platz für das Datum oben */
}

.cyber-feed-item:hover {
  border-color: var(--neon-yellow);
  box-shadow: 0 0 10px rgba(255, 255, 0, 0.3);
}

.feed-time {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.6);
  font-family: "Courier New", monospace;
}

.feed-title {
  color: var(--neon-yellow);
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.feed-desc {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
}

.nav-link-small {
  color: var(--neon-yellow);
  font-size: 0.8rem;
  text-decoration: none;
  font-family: "Courier New", monospace;
}

.nav-link-small:hover {
  text-shadow: 0 0 5px var(--neon-yellow);
}

/* Loading State */
.cyber-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 150px;
}

.scanner {
  width: 100%;
  height: 3px;
  background: var(--neon-yellow);
  position: relative;
  animation: scan 1.5s linear infinite;
  box-shadow: 0 0 8px var(--neon-yellow);
}

@keyframes scan {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(100px);
  }
  100% {
    transform: translateY(0);
  }
}

.cyber-loading p {
  margin-top: 1rem;
  color: var(--neon-yellow);
  font-family: "Courier New", monospace;
}

/* Error and Empty States */
.cyber-error,
.cyber-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 150px;
  border: 1px dashed rgba(255, 0, 255, 0.5);
  color: var(--neon-magenta);
  font-family: "Courier New", monospace;
  text-align: center;
  padding: 1rem;
}
</style>
