<template>
  <section class="hero">
    <div class="hero-content">
      <!-- 
        SOLID - Single Responsibility Principle:
        This component has the single responsibility of displaying about information.
        
        SOLID - Open/Closed Principle:
        The component can be extended with more content without modifying its basic structure.
      -->
      <h1 class="neon-text">Über mich</h1>

      <div class="status-indicator">
        <div class="status-dot"></div>
        <div class="status-text">Profil aktiv</div>
      </div>

      <div class="vision-wrapper">
        <div class="vision-text">
          <h2 class="neon-text-pink">Ein Blick hinter die Kulissen</h2>
          <p>
            Herzlich Willkommen!

            Mein Name ist Marc aka Sonny, und ich befinde mich aktuell in der Umschulung zum Fachinformatiker für
            Anwendungsentwicklung. Seit ich denken kann, fasziniert mich die digitale Welt: Ich bin ein
            leidenschaftlicher Entwickler, der sich besonders für Webentwicklung, Software-Architekturen und
            Cybersicherheit begeistert.<br>
            <br>
            Als Kind der 90er fühle ich mich besonders von der Cyberpunk-Kultur inspiriert – diese Faszination fließt in
            meine Projekte ein, sei es durch kreatives Design oder clevere Funktionalität.<br> 
            <br>
            Ich bin neugierig, lernbereit
            und gehe strukturiert an Herausforderungen heran. Meine Stärken liegen insbesondere darin, mich schnell in
            neue Technologien und Frameworks einzuarbeiten und diese zielorientiert anzuwenden.
          </p>

          <h3 class="neon-text">Meine Fähigkeiten auf einen Blick:</h3>
          <div class="skills-table">
            <table>
              <thead>
                <tr>
                  <th>Fähigkeit / Technologie</th>
                  <th>Kompetenz</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Python</td>
                  <td>
                    <div class="skill-bar">
                      <div class="skill-level" style="width: 65%"></div>
                      <span class="skill-percent">65%</span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td>HTML & CSS</td>
                  <td>
                    <div class="skill-bar">
                      <div class="skill-level" style="width: 70%"></div>
                      <span class="skill-percent">70%</span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td>KI-Anwendugen</td>
                  <td>
                    <div class="skill-bar">
                      <div class="skill-level" style="width: 75%"></div>
                      <span class="skill-percent">75%</span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td>JavaScript / Vue.js</td>
                  <td>
                    <div class="skill-bar">
                      <div class="skill-level" style="width: 65%"></div>
                      <span class="skill-percent">65%</span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td>Flask (Backend)</td>
                  <td>
                    <div class="skill-bar">
                      <div class="skill-level" style="width: 55%"></div>
                      <span class="skill-percent">55%</span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td>Bootstrap Framework</td>
                  <td>
                    <div class="skill-bar">
                      <div class="skill-level" style="width: 60%"></div>
                      <span class="skill-percent">60%</span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td>SQL & ORM (SQLAlchemy)</td>
                  <td>
                    <div class="skill-bar">
                      <div class="skill-level" style="width: 55%"></div>
                      <span class="skill-percent">55%</span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td>Clean Code & SOLID-Prinzipien</td>
                  <td>
                    <div class="skill-bar">
                      <div class="skill-level" style="width: 60%"></div>
                      <span class="skill-percent">60%</span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td>Linux / Shell Scripting</td>
                  <td>
                    <div class="skill-bar">
                      <div class="skill-level" style="width: 80%"></div>
                      <span class="skill-percent">80%</span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td>Git & Versionsverwaltung</td>
                  <td>
                    <div class="skill-bar">
                      <div class="skill-level" style="width: 60%"></div>
                      <span class="skill-percent">60%</span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td>Cybersicherheit Grundlagen</td>
                  <td>
                    <div class="skill-bar">
                      <div class="skill-level" style="width: 65%"></div>
                      <span class="skill-percent">65%</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <p>
            <strong>Was mich ausmacht:</strong>
          </p>
          <ul>
            <li>Lösungsorientierte Denkweise</li>
            <li>Starke Eigeninitiative und Lernbereitschaft</li>
            <li>Strukturierte und saubere Arbeitsweise</li>
            <li>Begeisterung für Technologien, die unsere digitale Zukunft prägen</li>
          </ul>
          <p>
            Ich freue mich darauf, meine Fähigkeiten in einem dynamischen Team im Rahmen eines Praktikums einzubringen
            und dabei weiter auszubauen. Wenn Sie nach jemandem suchen, der mit Begeisterung und Kompetenz Ihr Projekt
            unterstützt, freue ich mich sehr auf Ihre Nachricht!

            Beste Grüße,
            Sonny
          </p>

          <div class="cyber-link">
            <div class="center-content">
              <router-link to="/" class="btn-neon-large">Zurück zur Startseite</router-link>
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
 * About Page Component
 * 
 * SOLID - Single Responsibility Principle:
 * This component has the single responsibility of displaying information about
 * the creator/company.
 * 
 * SOLID - Open/Closed Principle:
 * The component structure allows for extension with additional content sections
 * without modifying the existing code.
 */
</script>

<style scoped>
/**
 * Component-specific styles follow the Single Responsibility Principle.
 * Reuses the hero container styling from the landing page for consistency.
 */

/* Custom scrollbar styling for cyberpunk theme */
.hero::-webkit-scrollbar {
  width: 8px;
}

.hero::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.3);
}

.hero::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, var(--neon-blue), var(--neon-purple));
  border-radius: 4px;
  box-shadow: 0 0 5px var(--neon-blue);
}

.hero::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, var(--neon-pink), var(--neon-purple));
}

.hero-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  padding-bottom: 1rem;
  position: relative;
  z-index: 2;
  padding-top: 1rem; /* Added additional top padding for content */
}


.cyber-link .btn-neon-large {
  box-shadow: 0 0 15px var(--neon-purple);
  transform: scale(1.05);
}

.cyber-link .btn-neon-large:hover {
  transform: scale(1.1);
  box-shadow: 0 0 25px var(--neon-purple);
}

/* Status indicator styling */

.status-dot {
  background-color: #0f0;
  box-shadow: 0 0 8px #0f0;
  animation: pulse 2s infinite;
}

.status-text {
  font-size: 0.9rem;
  color: #0f0;
  text-shadow: 0 0 5px #0f0;
}

/* Skills table styling */
.skills-heading {
  color: var(--neon-blue);
  text-shadow: 0 0 5px var(--neon-blue);
  margin: 1.5rem 0 1rem;
}

.skills-table {
  margin: 1rem 0 2rem;
  width: 100%;
  overflow-x: auto;
  color: white;
}

.skills-table table {
  width: 100%;
  border-collapse: collapse;
  border-spacing: 0;
}

.skills-table th, .skills-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.skills-table th {
  color: var(--neon-pink);
  text-shadow: 0 0 5px var(--neon-pink);
  font-weight: bold;
}

.skill-bar {
  background: rgba(20, 20, 20, 0.6);
  height: 20px;
  border-radius: 10px;
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(80, 80, 80, 0.5);
}

.skill-level {
  height: 100%;
  background: linear-gradient(90deg, #00ccff, #5933ff);
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 204, 255, 0.7);
}

.skill-percent {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: white;
  font-size: 0.8rem;
  text-shadow: 0 0 2px black;
}

/* List styling for "Was mich ausmacht" */
ul {
  list-style-type: none;
  padding-left: 0;
  margin: 1rem 0;
}

ul li {
  position: relative;
  padding-left: 1.5rem;
  margin-bottom: 0.5rem;
}

ul li:before {
  content: "›";
  color: var(--neon-purple);
  position: absolute;
  left: 0;
  font-size: 1.2rem;
  text-shadow: 0 0 5px var(--neon-purple);
}
</style>