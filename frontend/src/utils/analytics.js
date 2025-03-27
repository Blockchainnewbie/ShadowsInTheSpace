// Google Analytics 4 Manager
import.meta.env.VITE_GA4_MEASUREMENT_ID
let isInitialized = false;

/**
 * Lädt das Google Analytics Script dynamisch
 * @param {string} measurementId - Google Analytics 4 Measurement ID (G-XXXXXXXX)
 * @returns {Promise} Promise, das erfüllt wird, wenn das Script geladen wurde
 */
const loadGoogleAnalyticsScript = (measurementId) => {
  return new Promise((resolve, reject) => {
    if (document.getElementById('ga-script')) {
      resolve(); // Script ist bereits vorhanden
      return;
    }

    const script = document.createElement('script');
    script.id = 'ga-script';
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
    
    script.onload = resolve;
    script.onerror = reject;
    
    document.head.appendChild(script);
  });
};

/**
 * Initialisiert Google Analytics 4, nachdem der Nutzer zugestimmt hat
 * @param {string} measurementId - Google Analytics 4 Measurement ID (G-XXXXXXXX)
 */
export const initializeGoogleAnalytics = async (measurementId) => {
  if (!measurementId || !measurementId.startsWith('G-')) {
    console.error('Invalid Google Analytics Measurement ID');
    return;
  }
  
  if (isInitialized || !getAnalyticsConsent()) return;
  
  try {
    // Script dynamisch laden
    await loadGoogleAnalyticsScript(measurementId);
    
    // GA4 initialisieren
    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    gtag('js', new Date());
    
    // Konfiguration mit respektvoller Datensammlung
    gtag('config', measurementId, {
      'anonymize_ip': true,           // IP-Adressen anonymisieren
      'allow_ad_personalization_signals': false, // Werbe-Personalisierung deaktivieren
      'cookie_expires': 14 * 30 * 24 * 60 * 60, // 14 Monate in Sekunden
    });
    
    isInitialized = true;
    console.log('Google Analytics initialized');
  } catch (error) {
    console.error('Error initializing Google Analytics:', error);
  }
};


function getAnalyticsConsent() {
  const savedConsent = localStorage.getItem('cookieConsent');
  if (savedConsent) {
    try {
      const parsedConsent = JSON.parse(savedConsent);
      return parsedConsent.analytics; // Gibt 'true' oder 'false' zurück
    } catch (e) {
      console.error('Error parsing cookie consent', e);
      return false; // Standardmäßig 'false', um GA4 nicht zu aktivieren, wenn ein Fehler auftritt
    }
  }
  return false; // Standardmäßig 'false', wenn keine Zustimmung gespeichert ist
};

/**
 * Deaktiviert Google Analytics und löscht Cookies
 * @param {string} measurementId - Google Analytics 4 Measurement ID (G-XXXXXXXX)
 */
export const disableGoogleAnalytics = (measurementId, deleteCookies = true) => {
  // GA4 deaktivieren
  window[`ga-disable-${measurementId}`] = true;
  
  // GA Cookies löschen nur wenn explizit gewünscht
  if (deleteCookies) {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.indexOf('_ga') === 0 || cookie.indexOf('_gid') === 0) {
        document.cookie = cookie.split('=')[0] + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=.' + window.location.hostname + ';';
      }
    }
  }
  
  isInitialized = false;
  
  // Optional: Script-Tag entfernen
  const scriptTag = document.getElementById('ga-script');
  if (scriptTag) scriptTag.remove();
  
  console.log('Google Analytics disabled and cookies deleted');
};
