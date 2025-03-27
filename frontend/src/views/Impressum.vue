<template>
  <div class="container mt-5 mb-5">
    <div class="cyber-container">
      <div class="cyber-header">
        <h1 class="glitch-text" data-text="Impressum">Impressum</h1>
        <div class="cyber-line"></div>
      </div>
      
      <div class="cyber-section">
        <h2 class="cyber-section-title">// BETREIBER DER SEITE</h2>
        <p>
          <span class="label">Name:</span> M. D. Haberland<br>
          <span class="label">Adresse:</span> Markscheide 14<br>
          <span class="label">PLZ/Ort:</span> 45143 Essen<br>
          <span class="label">Land:</span> Deutschland
        </p>
      </div>
      
      <div class="cyber-section">
        <h2 class="cyber-section-title">// KONTAKT</h2>
        <p>
          <span class="label">E-Mail:</span> contact@shadowsinthe.space<br>
          <span class="label">Telefon:</span> +49 1636830932<br>
        </p>
      </div>
      
      <div class="cyber-section">
        <h2 class="cyber-section-title">// RECHTLICHE INFORMATIONEN</h2>
        <p>
          <span class="label">Zweck der Seite:</span> Eine private Projektseite ohne wirtschaftliche Interessen.<br>

        </p>
      </div>
      
      <div class="cyber-section">
        <h2 class="cyber-section-title">// VERANTWORTLICH FÜR DEN INHALT</h2>
        <p>
          <span class="label">Gemäß § 55 Abs. 2 RStV:</span> M. D. Haberland <br>
         
        </p>
      </div>
      
      <div class="cyber-section">
        <h2 class="cyber-section-title">// HAFTUNGSHINWEIS</h2>
        <p>
          Trotz sorgfältiger inhaltlicher Kontrolle übernehmen wir keine Haftung für die Inhalte externer Links. 
          Für den Inhalt der verlinkten Seiten sind ausschließlich deren Betreiber verantwortlich.
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cyber-container {
  background: rgba(0, 0, 0, 0.7);
  border: 1px solid var(--neon-cyan);
  padding: 2rem;
  position: relative;
  margin-bottom: 3rem;
}

.cyber-header {
  margin-bottom: 2rem;
  position: relative;
}

.glitch-text {
  color: var(--neon-cyan);
  font-size: 2.5rem;
  font-weight: bold;
  text-shadow: 0 0 5px var(--neon-cyan), 0 0 10px rgba(0, 255, 255, 0.8);
  margin-bottom: 0.5rem;
}

.cyber-line {
  height: 2px;
  background: var(--neon-cyan);
  box-shadow: 0 0 10px var(--neon-cyan);
  width: 100%;
  margin-top: 1rem;
}

.cyber-section {
  margin-bottom: 2rem;
  padding-left: 1rem;
  border-left: 2px solid var(--neon-cyan);
}

.cyber-section-title {
  color: var(--neon-cyan);
  font-size: 1.2rem;
  margin-bottom: 1rem;
  font-family: 'ShareTechMono', monospace;
}

.label {
  color: var(--neon-pink);
  font-weight: bold;
  min-width: 150px;
  display: inline-block;
}

p {
  color: #fff;
  line-height: 1.8;
}
</style>
