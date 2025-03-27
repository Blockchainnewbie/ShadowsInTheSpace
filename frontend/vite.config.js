import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

/**
 * Vite-Konfiguration
 *
 * SOLID - Single Responsibility Principle (Einzelverantwortungsprinzip):
 * Diese Datei hat die einzige Verantwortung, das Vite-Build-System zu konfigurieren.
 *
 * SOLID - Open/Closed Principle (Offen-Geschlossen-Prinzip):
 * Die Konfiguration ist offen für Erweiterungen (durch Hinzufügen weiterer Plugins oder Optionen),
 * ohne die bestehende Funktionalität zu verändern.
 */
export default defineConfig({
  plugins: [vue()],
  build: {
    assetsInlineLimit: 0,
    minify: 'terser',
    sourcemap: false,
    target: 'es2015',
    rollupOptions: {
      external: [],
      output: {
        manualChunks: {
          vue: ['vue', 'vue-router'],
          bootstrap: ['bootstrap']
        },
        assetFileNames: (assetInfo) => {
          if (/\.(woff2?|eot|ttf|otf)$/.test(assetInfo.name)) {
            return 'fonts/[name][extname]'
          }
          return 'assets/[name][extname]'
        }
      }
    }
  },
  base: process.env.NODE_ENV === 'production' ? '/' : '/',
  assetsInclude: ['**/*.ttf', '**/*.woff', '**/*.woff2', '**/*.eot', '**/*.otf']
})
