<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShadowsInThe.Space - Hacking Games</title>

    <script src="https://cdn.tailwindcss.com"></script>

    <script type="module" src="https://unpkg.com/lucide-static@latest/font/lucide.js"></script>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400..900&family=Press+Start+2P&display=swap" rel="stylesheet">

    <style>
        /* Grundlegende Cyberpunk-Ästhetik (wie zuvor) */
        body {
            background-color: #0a0a1a;
            color: #00ffcc;
            font-family: 'Orbitron', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            padding: 2rem;
        }

        .game-container {
            background-color: rgba(10, 10, 30, 0.8);
            border: 1px solid #00ffcc;
            border-radius: 8px;
            padding: 2rem;
            margin-top: 2rem;
            width: 100%;
            max-width: 800px;
            box-shadow: 0 0 15px rgba(0, 255, 204, 0.3);
            position: relative;
            overflow: hidden;
        }

        canvas {
            display: block;
            background-color: #050510;
            border: 1px dashed #33ffff;
            border-radius: 4px;
            margin: 1rem auto;
            max-width: 100%;
        }

        button, .button {
            background-color: transparent;
            border: 1px solid #ff00ff;
            color: #ff00ff;
            padding: 0.5rem 1rem;
            margin: 0.5rem;
            border-radius: 4px;
            font-family: 'Press Start 2P', cursive;
            font-size: 0.8rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            box-shadow: 0 0 5px rgba(255, 0, 255, 0.5);
        }

        button:hover, .button:hover {
            background-color: rgba(255, 0, 255, 0.2);
            color: #ffffff;
            box-shadow: 0 0 15px rgba(255, 0, 255, 0.8);
        }

        button:disabled {
            border-color: #555;
            color: #555;
            cursor: not-allowed;
            box-shadow: none;
        }
         button:disabled:hover {
             background-color: transparent;
         }

        input[type="text"], input[type="number"] {
            background-color: rgba(0, 0, 0, 0.5);
            border: 1px solid #00ffcc;
            color: #00ffcc;
            padding: 0.5rem;
            border-radius: 4px;
            font-family: 'Orbitron', sans-serif;
            margin: 0.5rem;
        }
        /* Spezifischer Stil für Nickname Input */
        input.nickname-input {
             font-family: 'Press Start 2P', cursive;
             text-transform: uppercase;
             text-align: center;
             font-size: 0.8rem;
             width: 150px; /* Feste Breite für Nickname */
        }


        .message-area {
            margin-top: 1rem;
            padding: 1rem;
            background-color: rgba(0, 255, 204, 0.1);
            border: 1px dashed #00ffcc;
            border-radius: 4px;
            min-height: 50px;
            font-family: 'Press Start 2P', cursive;
            font-size: 0.7rem;
            line-height: 1.5;
            color: #99ffee;
            white-space: pre-wrap;
        }

        /* Tabs (wie zuvor) */
        .tabs {
            display: flex;
            justify-content: center;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }

        .tab-button {
            background-color: transparent;
            border: none;
            border-bottom: 2px solid transparent;
            color: #00aaff;
            padding: 0.5rem 1rem;
            margin: 0 0.25rem;
            cursor: pointer;
            font-family: 'Orbitron', sans-serif;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .tab-button.active {
            color: #00ffcc;
            border-bottom: 2px solid #00ffcc;
        }
        .tab-button:hover {
             color: #ffffff;
             background-color: rgba(0, 170, 255, 0.1);
        }

        .game-content {
            display: none;
        }
        .game-content.active {
            display: block;
        }

        /* Spezifische Stile (wie zuvor) */
        /* Password Cracker */
        .cracker-input-area span { display: inline-block; width: 30px; height: 30px; border: 1px solid #00ffcc; margin: 2px; text-align: center; line-height: 30px; font-family: 'Press Start 2P', cursive; cursor: pointer; transition: background-color 0.2s; }
        .cracker-input-area span:hover { background-color: rgba(0, 255, 204, 0.2); }
        .cracker-history div { font-family: 'Courier New', Courier, monospace; margin-bottom: 5px; border-bottom: 1px dashed #336666; padding-bottom: 5px; }
         /* Data Decryption */
         #decryption-output { font-family: 'Courier New', Courier, monospace; letter-spacing: 2px; word-wrap: break-word; }
         #decryption-encrypted { color: #ff6666; font-style: italic; }
         #decryption-timer-display { color: #ff6666; font-family: 'Press Start 2P', cursive; } /* Timer-Anzeige */
        /* Network Intrusion */
        #network-canvas { cursor: pointer; }
         /* System Override */
         .override-sequence-display { display: flex; justify-content: center; margin-bottom: 1rem; }
         .override-sequence-display span { display: inline-block; width: 40px; height: 40px; border: 2px solid #ff00ff; border-radius: 50%; margin: 5px; text-align: center; line-height: 36px; font-family: 'Press Start 2P', cursive; font-size: 1rem; background-color: rgba(255, 0, 255, 0.1); box-shadow: 0 0 8px rgba(255, 0, 255, 0.6); }
         .override-buttons button { min-width: 60px; }

        /* Leaderboard Stile */
        .leaderboard-list {
            list-style: none;
            padding: 0;
            margin: 0;
            font-family: 'Press Start 2P', cursive;
            font-size: 0.8rem;
            max-height: 300px; /* Scrollbar bei vielen Einträgen */
            overflow-y: auto;
        }
        .leaderboard-list li {
            display: flex;
            justify-content: space-between;
            padding: 0.5rem 0;
            border-bottom: 1px dashed rgba(0, 255, 204, 0.3);
        }
        .leaderboard-list li:last-child {
            border-bottom: none;
        }
        .leaderboard-list .rank {
            color: #ff00ff; /* Magenta für Rang */
            min-width: 30px;
        }
        .leaderboard-list .nickname {
            color: #ffffff; /* Weiß für Nickname */
            flex-grow: 1;
            margin-left: 1rem;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .leaderboard-list .score {
            color: #00ffcc; /* Cyan für Score */
            min-width: 60px;
            text-align: right;
        }
        .nickname-prompt {
             margin-top: 1rem;
             padding: 1rem;
             background-color: rgba(255, 255, 0, 0.1); /* Leicht gelblich für Aufmerksamkeit */
             border: 1px dashed #ffff00;
             border-radius: 4px;
             text-align: center;
        }
         .nickname-prompt p {
             font-family: 'Press Start 2P', cursive;
             font-size: 0.8rem;
             color: #ffff99;
             margin-bottom: 0.5rem;
         }
    </style>
</head>
<body>

    <h1 class="text-3xl font-bold text-[#00ffcc] mb-4 font-['Orbitron']">Hacking Simulation Interface</h1>
    <p class="text-sm text-[#99ffee] mb-8 max-w-2xl text-center">Wähle eine Simulation, um deine Fähigkeiten zu testen und in die Schatten einzutauchen.</p>

    <div class="tabs">
        <button class="tab-button active" onclick="switchGame('firewall')">Firewall Breach</button>
        <button class="tab-button" onclick="switchGame('cracker')">Password Cracker</button>
        <button class="tab-button" onclick="switchGame('decryption')">Data Decryption</button>
        <button class="tab-button" onclick="switchGame('network')">Network Intrusion</button>
        <button class="tab-button" onclick="switchGame('override')">System Override</button>
        <button class="tab-button" onclick="switchGame('leaderboard')">Leaderboard</button>
    </div>

    <div class="game-container">


        <div id="game-firewall" class="game-content active">
            <h2 class="text-xl font-bold text-[#ff00ff] mb-2">Firewall Breach v1.1</h2>
            <p class="text-sm text-[#99ffee] mb-4">Schleuse das Datenpaket durch die Lücke in der Firewall. Klicke im richtigen Moment!</p>
            <canvas id="firewall-canvas" width="600" height="200"></canvas>
            <div class="flex justify-center items-center space-x-4">
                 <button id="firewall-start-btn" onclick="firewallGame.start()">Start Breach</button>
                 <div class="text-[#99ffee]">Score: <span id="firewall-score">0</span></div>
                 <div class="text-[#ff6666]">Level: <span id="firewall-level">1</span></div>
            </div>
            <div id="firewall-message" class="message-area">Status: Idle... Bereit für den Durchbruch.</div>
            <div id="firewall-nickname-prompt" class="nickname-prompt" style="display: none;">
                <p>Highscore! Gib deinen Nickname ein:</p>
                <input type="text" id="firewall-nickname" class="nickname-input" maxlength="10" placeholder="AAA">
                <button onclick="leaderboard.submitScore('firewall', firewallGame.score, document.getElementById('firewall-nickname').value)">Senden</button>
            </div>
        </div>


        <div id="game-cracker" class="game-content">
            <h2 class="text-xl font-bold text-[#ff00ff] mb-2">Password Cracker v2.0</h2>
            <p class="text-sm text-[#99ffee] mb-4">Entschlüssle den 4-stelligen Symbol-Code. Du hast 10 Versuche. Weniger Versuche sind besser!</p>
            <div class="flex flex-col items-center">
                <div class="cracker-input-area mb-4">
                    Aktueller Versuch:
                    <span id="cracker-guess-0" onclick="crackerGame.cycleSymbol(0)">?</span>
                    <span id="cracker-guess-1" onclick="crackerGame.cycleSymbol(1)">?</span>
                    <span id="cracker-guess-2" onclick="crackerGame.cycleSymbol(2)">?</span>
                    <span id="cracker-guess-3" onclick="crackerGame.cycleSymbol(3)">?</span>
                </div>
                 <div class="mb-4">
                    Verfügbare Symbole:
                    <span class="font-['Press_Start_2P'] text-sm" id="cracker-symbols"></span>
                 </div>
                <button id="cracker-submit-btn" onclick="crackerGame.submitGuess()">Submit Guess</button>
                <button onclick="crackerGame.start()">Neues Spiel</button>
            </div>
            <div id="cracker-feedback" class="message-area">Feedback: Warte auf Eingabe...</div>
             <div class="mt-4">
                <h3 class="text-lg text-[#00ffcc] mb-2">Versuchshistorie:</h3>
                <div id="cracker-history" class="text-xs h-32 overflow-y-auto p-2 border border-dashed border-[#336666] rounded"></div>
            </div>
            <div id="cracker-nickname-prompt" class="nickname-prompt" style="display: none;">
                 <p>Highscore! Gib deinen Nickname ein:</p>
                 <input type="text" id="cracker-nickname" class="nickname-input" maxlength="10" placeholder="AAA">
                 <button onclick="leaderboard.submitScore('cracker', crackerGame.attemptsUsed, document.getElementById('cracker-nickname').value)">Senden</button>
            </div>
        </div>


        <div id="game-decryption" class="game-content">
            <h2 class="text-xl font-bold text-[#ff00ff] mb-2">Data Decryption v1.0</h2>
            <p class="text-sm text-[#99ffee] mb-4">Finde den korrekten Shift-Wert so schnell wie möglich! Niedrigere Zeit ist besser.</p>
            <div class="mb-4">
                <p class="text-[#99ffee]">Verschlüsselter Text:</p>
                <p id="decryption-encrypted" class="p-2 bg-black bg-opacity-20 rounded border border-dashed border-[#ff6666]"></p>
            </div>
            <div class="flex items-center justify-center mb-4 space-x-4">
                <label for="decryption-shift" class="text-[#99ffee]">Shift-Wert (0-25):</label>
                <input type="number" id="decryption-shift" min="0" max="25" value="0" oninput="decryptionGame.decrypt()">
                <span id="decryption-timer-display">Zeit: --s</span>
                <button onclick="decryptionGame.start()">Neue Nachricht</button>
            </div>
            <div class="message-area">
                <p class="text-[#99ffee]">Entschlüsselter Text:</p>
                <p id="decryption-output"></p>
            </div>
             <div id="decryption-message" class="message-area mt-4">Finde den Shift-Wert...</div>

            <div id="decryption-nickname-prompt" class="nickname-prompt" style="display: none;">
                  <p>Highscore! Gib deinen Nickname ein:</p>
                  <input type="text" id="decryption-nickname" class="nickname-input" maxlength="10" placeholder="AAA">

                  <button onclick="leaderboard.submitScore('decryption', decryptionGame.firstCorrectTime, document.getElementById('decryption-nickname').value)">Senden</button>
             </div>
        </div>


        <div id="game-network" class="game-content">
            <h2 class="text-xl font-bold text-[#ff00ff] mb-2">Network Intrusion v0.5</h2>
            <p class="text-sm text-[#99ffee] mb-4">Navigiere durch das Netzwerk (<span class="text-green-400">Grün</span>=Start, <span class="text-red-500">Rot</span>=Ziel). Vermeide Firewalls (<span class="text-yellow-500">Gelb</span>). Klicke auf benachbarte Knoten. Weniger Züge sind besser!</p>
            <canvas id="network-canvas" width="400" height="400"></canvas>
             <div class="flex justify-center items-center space-x-4 mt-4">
                 <button onclick="networkGame.start()">Neues Netzwerk</button>
                 <div class="text-[#99ffee]">Züge: <span id="network-moves">0</span></div>
             </div>
            <div id="network-message" class="message-area">Status: Netzwerk initialisiert. Finde den Pfad.</div>
             <div id="network-nickname-prompt" class="nickname-prompt" style="display: none;">
                  <p>Highscore! Gib deinen Nickname ein:</p>
                  <input type="text" id="network-nickname" class="nickname-input" maxlength="10" placeholder="AAA">
                  <button onclick="leaderboard.submitScore('network', networkGame.moves, document.getElementById('network-nickname').value)">Senden</button>
             </div>
        </div>


        <div id="game-override" class="game-content">
            <h2 class="text-xl font-bold text-[#ff00ff] mb-2">System Override v1.0</h2>
            <p class="text-sm text-[#99ffee] mb-4">Gib die angezeigte Sequenz korrekt ein, um das System zu überbrücken. Beeile dich!</p>
            <div class="override-sequence-display"></div>
            <div class="override-buttons flex justify-center flex-wrap my-4">
                <button onclick="overrideGame.input('A')">A</button>
                <button onclick="overrideGame.input('B')">B</button>
                <button onclick="overrideGame.input('C')">C</button>
                <button onclick="overrideGame.input('X')">X</button>
                <button onclick="overrideGame.input('Y')">Y</button>
                <button onclick="overrideGame.input('Z')">Z</button>
            </div>
            <div class="flex justify-center items-center space-x-4">
                 <button id="override-start-btn" onclick="overrideGame.start()">Start Override</button>
                 <div class="text-[#99ffee]">Level: <span id="override-level">1</span></div>
                 <div class="text-[#ff6666]">Zeit: <span id="override-timer">--</span>s</div>
            </div>
            <div id="override-message" class="message-area">Status: Bereit für Systemübernahme.</div>
             <div id="override-nickname-prompt" class="nickname-prompt" style="display: none;">
                  <p>Highscore! Gib deinen Nickname ein:</p>
                  <input type="text" id="override-nickname" class="nickname-input" maxlength="10" placeholder="AAA">
                  <button onclick="leaderboard.submitScore('override', overrideGame.finalLevel, document.getElementById('override-nickname').value)">Senden</button>
             </div>
        </div>


        <div id="game-leaderboard" class="game-content">
            <h2 class="text-xl font-bold text-[#ff00ff] mb-4">Global Leaderboard</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <h3 class="text-lg text-[#00ffcc] mb-2">Firewall Breach (Top 5 Scores)</h3>
                    <ol id="leaderboard-firewall" class="leaderboard-list"></ol>
                </div>
                <div>
                    <h3 class="text-lg text-[#00ffcc] mb-2">Password Cracker (Top 5 Attempts - Lower is Better)</h3>
                    <ol id="leaderboard-cracker" class="leaderboard-list"></ol>
                </div>

                <div>
                     <h3 class="text-lg text-[#00ffcc] mb-2">Data Decryption (Top 5 Times - Lower is Better)</h3>
                     <ol id="leaderboard-decryption" class="leaderboard-list"></ol>
                 </div>
                <div>
                     <h3 class="text-lg text-[#00ffcc] mb-2">Network Intrusion (Top 5 Moves - Lower is Better)</h3>
                     <ol id="leaderboard-network" class="leaderboard-list"></ol>
                 </div>
                 <div>
                     <h3 class="text-lg text-[#00ffcc] mb-2">System Override (Top 5 Levels)</h3>
                     <ol id="leaderboard-override" class="leaderboard-list"></ol>
                 </div>
            </div>
             <div class="mt-6 text-center">
                 <button onclick="leaderboard.resetAllScores()">Reset All Leaderboards (DEBUG)</button>
             </div>
        </div>

    </div>

    <script>
        // === Leaderboard Management ===
        const leaderboard = {
            storageKey: 'shadowsInTheSpaceHackingScores',
            maxEntries: 5,

            loadScores(gameId) {
                try {
                    const allScores = JSON.parse(localStorage.getItem(this.storageKey)) || {};
                    return allScores[gameId] || [];
                } catch (e) { console.error("Error loading scores:", e); return []; }
            },

            saveAllScores(allScores) {
                try { localStorage.setItem(this.storageKey, JSON.stringify(allScores)); }
                catch (e) { console.error("Error saving scores:", e); }
            },

            isHighScore(gameId, score) {
                const scores = this.loadScores(gameId);
                if (scores.length < this.maxEntries) return true;
                // Lower score is better for cracker, network, decryption
                if (gameId === 'cracker' || gameId === 'network' || gameId === 'decryption') {
                     return score < scores[scores.length - 1].score;
                } else { // Higher score is better for firewall, override
                     return score > scores[scores.length - 1].score;
                }
            },

            addScore(gameId, nickname, score) {
                if (!nickname || nickname.trim() === '') nickname = 'ANON';
                nickname = nickname.trim().toUpperCase().substring(0, 10);

                // Format score for display (e.g., time)
                let displayScore = score;
                if (gameId === 'decryption') {
                    displayScore = score.toFixed(2) + 's'; // Zeit auf 2 Dezimalstellen
                }


                const allScores = JSON.parse(localStorage.getItem(this.storageKey)) || {};
                let gameScores = allScores[gameId] || [];

                // Wichtig: Zum Speichern den numerischen Score verwenden, nicht den formatierten String
                gameScores.push({ nickname, score: score, displayScore: displayScore });

                // Sortieren
                if (gameId === 'cracker' || gameId === 'network' || gameId === 'decryption') {
                     gameScores.sort((a, b) => a.score - b.score); // Lower is better
                } else {
                     gameScores.sort((a, b) => b.score - a.score); // Higher is better
                }

                gameScores = gameScores.slice(0, this.maxEntries);
                allScores[gameId] = gameScores;
                this.saveAllScores(allScores);
                this.displayLeaderboard();
            },

            displayLeaderboard() {
                // Hinzufügen von 'decryption' zur Liste der Spiele
                const gameIds = ['firewall', 'cracker', 'decryption', 'network', 'override'];
                gameIds.forEach(gameId => {
                    const listEl = document.getElementById(`leaderboard-${gameId}`);
                    if (!listEl) return;

                    const scores = this.loadScores(gameId);
                    listEl.innerHTML = '';

                    if (scores.length === 0) {
                        listEl.innerHTML = '<li><span class="nickname">Noch keine Einträge</span></li>';
                    } else {
                        scores.forEach((entry, index) => {
                            const li = document.createElement('li');
                            // Verwende displayScore für die Anzeige
                            li.innerHTML = `
                                <span class="rank">${index + 1}.</span>
                                <span class="nickname">${entry.nickname}</span>
                                <span class="score">${entry.displayScore !== undefined ? entry.displayScore : entry.score}</span>
                            `;
                            listEl.appendChild(li);
                        });
                    }
                });
            },

            promptForNickname(gameId, finalScore) {
                 const promptEl = document.getElementById(`${gameId}-nickname-prompt`);
                 const inputEl = document.getElementById(`${gameId}-nickname`);
                 if (promptEl && inputEl) {
                     inputEl.value = '';
                     promptEl.style.display = 'block';
                     inputEl.focus();
                     promptEl.dataset.score = finalScore; // Store score temporarily if needed
                 }
            },

             hideNicknamePrompt(gameId) {
                 const promptEl = document.getElementById(`${gameId}-nickname-prompt`);
                 if (promptEl) { promptEl.style.display = 'none'; }
             },

             submitScore(gameId, score, nickname) {
                 // Score hier erneut aus dem game object holen oder aus dataset, falls gespeichert
                 // Beispiel: const actualScore = parseFloat(document.getElementById(`${gameId}-nickname-prompt`).dataset.score);
                 this.addScore(gameId, nickname, score); // Verwende den übergebenen, numerischen Score
                 this.hideNicknamePrompt(gameId);
                 const gameMessageEl = document.getElementById(`${gameId}-message`);
                 if(gameMessageEl) { gameMessageEl.textContent += "\n> Highscore gespeichert!"; }
             },

             resetAllScores() {
                 if (confirm("Wirklich ALLE Leaderboards zurücksetzen?")) {
                     try { localStorage.removeItem(this.storageKey); this.displayLeaderboard(); alert("Leaderboards zurückgesetzt."); }
                     catch (e) { console.error("Fehler beim Zurücksetzen:", e); alert("Fehler."); }
                 }
             }
        };

        // === Spielauswahl Logik (unverändert) ===
        function switchGame(gameId) {
            document.querySelectorAll('.game-content').forEach(el => el.classList.remove('active'));
            document.getElementById(`game-${gameId}`).classList.add('active');
            document.querySelectorAll('.tab-button').forEach(el => el.classList.remove('active'));
            document.querySelector(`.tab-button[onclick="switchGame('${gameId}')"]`).classList.add('active');
            if (gameId === 'leaderboard') { leaderboard.displayLeaderboard(); }
        }

        // === Spiel 1: Firewall Breach (unverändert) ===
        const firewallGame = {
            canvas: document.getElementById('firewall-canvas'), ctx: null, packet: { x: 50, y: 100, width: 15, height: 10, speed: 0, active: false }, firewall: { x: 500, width: 20, gapY: 80, gapHeight: 40, speed: 2 }, score: 0, level: 1, gameLoopId: null, running: false, messageEl: document.getElementById('firewall-message'), scoreEl: document.getElementById('firewall-score'), levelEl: document.getElementById('firewall-level'), startBtn: document.getElementById('firewall-start-btn'),
            init() { if (!this.canvas) return; this.ctx = this.canvas.getContext('2d'); this.canvas.addEventListener('click', () => this.shootPacket()); this.reset(); this.draw(); },
            reset() { this.packet.x = 50; this.packet.y = this.canvas.height / 2 - this.packet.height / 2; this.packet.speed = 0; this.packet.active = false; this.firewall.x = this.canvas.width - 100; this.firewall.gapY = Math.random() * (this.canvas.height - this.firewall.gapHeight); this.firewall.speed = 1 + this.level * 0.5; this.updateUI(); this.setMessage("Status: Bereit. Klicke, um das Paket zu starten."); if (this.gameLoopId) cancelAnimationFrame(this.gameLoopId); this.running = false; this.startBtn.disabled = false; leaderboard.hideNicknamePrompt('firewall'); this.draw(); },
            start() { if (this.running) return; this.running = true; this.score = 0; this.level = 1; this.firewall.gapHeight = 40; this.firewall.speed = 1 + this.level * 0.5; this.packet.active = false; this.packet.x = 50; this.updateUI(); this.setMessage("Level " + this.level + ": Firewall aktiv! Klicke, um Paket zu senden."); this.startBtn.disabled = true; leaderboard.hideNicknamePrompt('firewall'); this.gameLoop(); },
            shootPacket() { if (!this.running || this.packet.active) return; this.packet.active = true; this.packet.speed = 5 + this.level; this.setMessage("Paket unterwegs..."); },
            update() { if (!this.running) return; this.firewall.gapY += this.firewall.speed; if (this.firewall.gapY < 0 || this.firewall.gapY + this.firewall.gapHeight > this.canvas.height) { this.firewall.speed *= -1; } if (this.packet.active) { this.packet.x += this.packet.speed; if (this.packet.x + this.packet.width > this.firewall.x && this.packet.x < this.firewall.x + this.firewall.width) { if (this.packet.y > this.firewall.gapY && this.packet.y + this.packet.height < this.firewall.gapY + this.firewall.gapHeight) { this.score++; this.setMessage("Treffer! Score: " + this.score); this.packet.active = false; this.packet.x = 50; if (this.score > 0 && this.score % 5 === 0) { this.level++; this.firewall.speed = 1 + this.level * 0.5; this.firewall.gapHeight *= 0.95; if (this.firewall.gapHeight < 15) this.firewall.gapHeight = 15; this.setMessage("Level Up! Level " + this.level); } } else { this.gameOver(); } this.updateUI(); } else if (this.packet.x > this.canvas.width) { this.packet.active = false; this.packet.x = 50; } } },
            gameOver() { this.running = false; this.startBtn.disabled = false; this.setMessage(`Fehler! Spiel vorbei. Score: ${this.score}`); if (leaderboard.isHighScore('firewall', this.score)) { leaderboard.promptForNickname('firewall', this.score); } },
            draw() { if (!this.ctx) return; this.ctx.fillStyle = '#050510'; this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height); this.ctx.fillStyle = '#ff00ff'; this.ctx.fillRect(this.firewall.x, 0, this.firewall.width, this.firewall.gapY); this.ctx.fillRect(this.firewall.x, this.firewall.gapY + this.firewall.gapHeight, this.firewall.width, this.canvas.height - (this.firewall.gapY + this.firewall.gapHeight)); if (this.packet.active) { this.ctx.fillStyle = '#00ffcc'; this.ctx.shadowColor = '#00ffcc'; this.ctx.shadowBlur = 10; this.ctx.fillRect(this.packet.x, this.packet.y, this.packet.width, this.packet.height); this.ctx.shadowBlur = 0; } /* Grid zeichnen optional */ },
            gameLoop() { if (!this.running) { this.draw(); return; } this.update(); this.draw(); this.gameLoopId = requestAnimationFrame(() => this.gameLoop()); },
            setMessage(msg) { this.messageEl.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`; },
            updateUI() { this.scoreEl.textContent = this.score; this.levelEl.textContent = this.level; }
        };
        window.addEventListener('load', () => firewallGame.init());

        // === Spiel 2: Password Cracker (unverändert) ===
        const crackerGame = {
            symbols: ['#', '@', '$', '%', '&', '*'], codeLength: 4, secretCode: [], currentGuess: [], attemptsLeft: 10, maxAttempts: 10, attemptsUsed: 0, history: [], feedbackEl: document.getElementById('cracker-feedback'), historyEl: document.getElementById('cracker-history'), submitBtn: document.getElementById('cracker-submit-btn'), guessElements: [], symbolsEl: document.getElementById('cracker-symbols'),
            init() { for (let i = 0; i < this.codeLength; i++) { this.guessElements.push(document.getElementById(`cracker-guess-${i}`)); } this.symbolsEl.textContent = this.symbols.join(' '); this.start(); },
            start() { this.secretCode = []; for (let i = 0; i < this.codeLength; i++) { this.secretCode.push(this.symbols[Math.floor(Math.random() * this.symbols.length)]); } this.currentGuess = Array(this.codeLength).fill('?'); this.attemptsLeft = this.maxAttempts; this.attemptsUsed = 0; this.history = []; this.updateGuessDisplay(); this.updateHistoryDisplay(); this.feedbackEl.textContent = `Neues Spiel. ${this.attemptsLeft} Versuche übrig.`; this.submitBtn.disabled = false; leaderboard.hideNicknamePrompt('cracker'); },
            cycleSymbol(index) { if (this.attemptsLeft <= 0) return; const currentSymbol = this.currentGuess[index]; let nextIndex = (currentSymbol === '?') ? 0 : (this.symbols.indexOf(currentSymbol) + 1) % this.symbols.length; this.currentGuess[index] = this.symbols[nextIndex]; this.updateGuessDisplay(); },
            updateGuessDisplay() { this.guessElements.forEach((el, i) => { el.textContent = this.currentGuess[i]; }); },
            submitGuess() { if (this.currentGuess.includes('?')) { this.feedbackEl.textContent = "Fehler: Alle Positionen ausfüllen."; return; } if (this.attemptsLeft <= 0) { this.feedbackEl.textContent = "Keine Versuche mehr."; return; } this.attemptsLeft--; this.attemptsUsed++; const guessStr = this.currentGuess.join(''); let correctPosition = 0; let correctSymbol = 0; const secretCopy = [...this.secretCode]; const guessCopy = [...this.currentGuess]; for (let i = 0; i < this.codeLength; i++) { if (guessCopy[i] === secretCopy[i]) { correctPosition++; secretCopy[i] = null; guessCopy[i] = null; } } for (let i = 0; i < this.codeLength; i++) { if (guessCopy[i] !== null) { const indexInSecret = secretCopy.indexOf(guessCopy[i]); if (indexInSecret !== -1) { correctSymbol++; secretCopy[indexInSecret] = null; } } } const feedback = `Versuch ${this.attemptsUsed}: ${guessStr} -> ${correctPosition} Korrekt/Pos, ${correctSymbol} Korrekt/Sym. ${this.attemptsLeft} Versuche übrig.`; this.history.push(feedback); this.updateHistoryDisplay(); if (correctPosition === this.codeLength) { this.feedbackEl.textContent = `Erfolg! Code ${guessStr} in ${this.attemptsUsed} Versuchen!`; this.submitBtn.disabled = true; this.attemptsLeft = 0; if (leaderboard.isHighScore('cracker', this.attemptsUsed)) { leaderboard.promptForNickname('cracker', this.attemptsUsed); } } else if (this.attemptsLeft === 0) { this.feedbackEl.textContent = `Fehlgeschlagen! Code war ${this.secretCode.join('')}.`; this.submitBtn.disabled = true; } else { this.feedbackEl.textContent = `Feedback: ${correctPosition} Korrekt/Pos, ${correctSymbol} Korrekt/Sym. ${this.attemptsLeft} Versuche übrig.`; } this.currentGuess = Array(this.codeLength).fill('?'); this.updateGuessDisplay(); },
            updateHistoryDisplay() { this.historyEl.innerHTML = this.history.slice().reverse().map(line => `<div>${line}</div>`).join(''); }
        };
        window.addEventListener('load', () => crackerGame.init());

        // === Spiel 3: Data Decryption (angepasst mit Timer) ===
        const decryptionGame = {
            encryptedEl: document.getElementById('decryption-encrypted'),
            outputEl: document.getElementById('decryption-output'),
            shiftInput: document.getElementById('decryption-shift'),
            messageEl: document.getElementById('decryption-message'),
            timerDisplayEl: document.getElementById('decryption-timer-display'), // Timer Anzeige
            possibleMessages: ["Treffpunkt um Mitternacht am Neon Drachen.", "Die Eisfee liefert das Paket morgen ab.", "Zugriffscode lautet SIEBEN ECHO VIER.", "Warnung: Systemkompromittierung erkannt.", "Projekt Chimera ist bereit fuer Phase Zwei.", "Der Kurier hat die Daten verloren. Improvisiere."],
            currentMessage: "",
            correctShift: 0,
            startTime: 0, // Zeitmessung Start
            timerIntervalId: null, // ID für setInterval
            firstCorrectTime: null, // Speichert die Zeit des ersten korrekten Fundes
            running: false, // Zeigt an, ob das Spiel (und der Timer) läuft

            init() {
                this.start();
                this.shiftInput.addEventListener('input', () => this.decrypt());
            },

            start() {
                this.running = true;
                this.firstCorrectTime = null; // Reset
                if (this.timerIntervalId) clearInterval(this.timerIntervalId); // Alten Timer löschen

                const randomIndex = Math.floor(Math.random() * this.possibleMessages.length);
                this.currentMessage = this.possibleMessages[randomIndex].toUpperCase();
                this.correctShift = Math.floor(Math.random() * 25) + 1;

                let encrypted = "";
                for (let i = 0; i < this.currentMessage.length; i++) {
                    encrypted += this.shiftChar(this.currentMessage[i], this.correctShift);
                }

                this.encryptedEl.textContent = encrypted;
                this.shiftInput.value = 0;
                this.shiftInput.disabled = false; // Input aktivieren
                this.decrypt(); // Initial mit Shift 0
                this.messageEl.textContent = "Neuer Datenstrom. Finde den Shift-Wert schnell!";
                leaderboard.hideNicknamePrompt('decryption'); // Prompt verstecken

                // Timer starten
                this.startTime = Date.now();
                this.timerIntervalId = setInterval(() => this.updateTimerDisplay(), 100); // Alle 100ms aktualisieren
                this.updateTimerDisplay(); // Sofort anzeigen
            },

            updateTimerDisplay() {
                if (!this.running) return;
                const elapsedTime = (Date.now() - this.startTime) / 1000;
                this.timerDisplayEl.textContent = `Zeit: ${elapsedTime.toFixed(1)}s`;
            },

            stopTimer() {
                 if (this.timerIntervalId) clearInterval(this.timerIntervalId);
                 this.running = false;
                 // Endgültige Zeit anzeigen
                 if (this.firstCorrectTime !== null) {
                    this.timerDisplayEl.textContent = `Zeit: ${this.firstCorrectTime.toFixed(2)}s`;
                 } else {
                     // Falls Timer gestoppt wird, bevor Lösung gefunden wurde (sollte nicht passieren)
                     const elapsedTime = (Date.now() - this.startTime) / 1000;
                     this.timerDisplayEl.textContent = `Zeit: ${elapsedTime.toFixed(1)}s (Gestoppt)`;
                 }
            },

            shiftChar(char, shift) {
                const charCode = char.charCodeAt(0);
                if (charCode >= 65 && charCode <= 90) { let shiftedCode = charCode + shift; if (shiftedCode > 90) { shiftedCode = 65 + (shiftedCode - 91); } else if (shiftedCode < 65) { shiftedCode = 91 - (65 - shiftedCode); } return String.fromCharCode(shiftedCode); } return char;
            },

            decrypt() {
                if (!this.running && this.firstCorrectTime !== null) return; // Nicht mehr entschlüsseln nach Erfolg

                const currentShift = parseInt(this.shiftInput.value) || 0;
                const encryptedText = this.encryptedEl.textContent;
                let decrypted = "";
                for (let i = 0; i < encryptedText.length; i++) {
                    decrypted += this.shiftChar(encryptedText[i], -currentShift);
                }
                this.outputEl.textContent = decrypted;

                if (decrypted === this.currentMessage && currentShift !== 0) {
                    // Nur beim ersten Finden stoppen und prüfen
                    if (this.firstCorrectTime === null) {
                        this.firstCorrectTime = (Date.now() - this.startTime) / 1000;
                        this.stopTimer();
                        this.shiftInput.disabled = true; // Input deaktivieren nach Erfolg
                        this.messageEl.textContent = `Erfolg! Shift ${currentShift} gefunden in ${this.firstCorrectTime.toFixed(2)} Sekunden!`;

                        // Highscore Check (niedrigere Zeit ist besser)
                        if (leaderboard.isHighScore('decryption', this.firstCorrectTime)) {
                            leaderboard.promptForNickname('decryption', this.firstCorrectTime);
                        }
                    }
                } else if (this.running) { // Nur Nachricht aktualisieren, wenn Timer noch läuft
                     if (currentShift !== 0) {
                         this.messageEl.textContent = `Shift ${currentShift} angewendet. Suche weiter...`;
                     } else {
                         this.messageEl.textContent = `Wähle einen Shift-Wert (1-25).`;
                     }
                }
            }
         };
        window.addEventListener('load', () => decryptionGame.init());


        // === Spiel 4: Network Intrusion (unverändert) ===
        const networkGame = {
            canvas: document.getElementById('network-canvas'), ctx: null, gridSize: 10, nodeSize: 30, gap: 10, grid: [], startNode: { x: 0, y: 0 }, targetNode: { x: 0, y: 0 }, currentNode: { x: 0, y: 0 }, moves: 0, gameOver: false, messageEl: document.getElementById('network-message'), movesEl: document.getElementById('network-moves'),
            init() { if (!this.canvas) return; this.ctx = this.canvas.getContext('2d'); this.canvas.width = this.gridSize * (this.nodeSize + this.gap) - this.gap; this.canvas.height = this.canvas.width; this.canvas.addEventListener('click', (e) => this.handleClick(e)); this.start(); },
            start() { this.grid = []; this.moves = 0; this.gameOver = false; this.updateUI(); this.messageEl.textContent = "Generiere Netzwerk..."; for (let y = 0; y < this.gridSize; y++) { this.grid[y] = []; for (let x = 0; x < this.gridSize; x++) { this.grid[y][x] = 0; } } const startSide = Math.floor(Math.random() * 4); let sx = 0, sy = 0; if (startSide === 0) { sx = 0; sy = Math.floor(Math.random() * this.gridSize); } else if (startSide === 1) { sx = this.gridSize - 1; sy = Math.floor(Math.random() * this.gridSize); } else if (startSide === 2) { sx = Math.floor(Math.random() * this.gridSize); sy = 0; } else { sx = Math.floor(Math.random() * this.gridSize); sy = this.gridSize - 1; } this.startNode = { x: sx, y: sy }; this.grid[sy][sx] = 1; this.currentNode = { ...this.startNode }; this.grid[this.currentNode.y][this.currentNode.x] = 4; let tx, ty; do { const targetSide = (startSide + 2) % 4; if (targetSide === 0) { tx = 0; ty = Math.floor(Math.random() * this.gridSize); } else if (targetSide === 1) { tx = this.gridSize - 1; ty = Math.floor(Math.random() * this.gridSize); } else if (targetSide === 2) { tx = Math.floor(Math.random() * this.gridSize); ty = 0; } else { tx = Math.floor(Math.random() * this.gridSize); ty = this.gridSize - 1; } } while (Math.abs(tx - sx) + Math.abs(ty - sy) < this.gridSize / 2); this.targetNode = { x: tx, y: ty }; this.grid[ty][tx] = 2; const firewallCount = Math.floor(this.gridSize * this.gridSize * 0.15); for (let i = 0; i < firewallCount; i++) { let fx, fy; do { fx = Math.floor(Math.random() * this.gridSize); fy = Math.floor(Math.random() * this.gridSize); } while (this.grid[fy][fx] !== 0); this.grid[fy][fx] = 3; } this.messageEl.textContent = "Netzwerk bereit."; leaderboard.hideNicknamePrompt('network'); this.draw(); },
            draw() { if (!this.ctx) return; this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height); for (let y = 0; y < this.gridSize; y++) { for (let x = 0; x < this.gridSize; x++) { const nodeX = x * (this.nodeSize + this.gap); const nodeY = y * (this.nodeSize + this.gap); let color = '#334444'; switch (this.grid[y][x]) { case 1: color = '#00ff00'; break; case 2: color = '#ff0000'; break; case 3: color = '#ffff00'; break; case 4: color = '#00aaff'; break; } this.ctx.fillStyle = color; if (this.grid[y][x] !== 0) { this.ctx.shadowColor = color; this.ctx.shadowBlur = 8; } else { this.ctx.shadowBlur = 0; } this.ctx.fillRect(nodeX, nodeY, this.nodeSize, this.nodeSize); this.ctx.shadowBlur = 0; if (x === this.currentNode.x && y === this.currentNode.y && !this.gameOver) { this.ctx.strokeStyle = '#ffffff'; this.ctx.lineWidth = 2; this.ctx.strokeRect(nodeX - 1, nodeY - 1, this.nodeSize + 2, this.nodeSize + 2); } } } },
            handleClick(event) { if (this.gameOver || !this.ctx) return; const rect = this.canvas.getBoundingClientRect(); const clickX = event.clientX - rect.left; const clickY = event.clientY - rect.top; const gridX = Math.floor(clickX / (this.nodeSize + this.gap)); const gridY = Math.floor(clickY / (this.nodeSize + this.gap)); if (gridX >= 0 && gridX < this.gridSize && gridY >= 0 && gridY < this.gridSize) { const dx = Math.abs(gridX - this.currentNode.x); const dy = Math.abs(gridY - this.currentNode.y); if ((dx === 1 && dy === 0) || (dx === 0 && dy === 1)) { const targetNodeType = this.grid[gridY][gridX]; if (targetNodeType === 3) { this.messageEl.textContent = "Alarm! Firewall getroffen!"; this.gameOver = true; } else if (targetNodeType === 4) { this.messageEl.textContent = "Knoten bereits gesichert."; } else { this.currentNode = { x: gridX, y: gridY }; this.moves++; this.updateUI(); if (targetNodeType === 2) { this.messageEl.textContent = `Erfolg! Ziel erreicht in ${this.moves} Zügen!`; this.gameOver = true; this.grid[gridY][gridX] = 4; if (leaderboard.isHighScore('network', this.moves)) { leaderboard.promptForNickname('network', this.moves); } } else { this.grid[gridY][gridX] = 4; this.messageEl.textContent = `Knoten gesichert (${this.moves} Züge)`; } } this.draw(); } else { this.messageEl.textContent = "Ungültiger Zug."; } } },
            updateUI() { this.movesEl.textContent = this.moves; }
        };
         window.addEventListener('load', () => networkGame.init());

        // === Spiel 5: System Override (unverändert) ===
        const overrideGame = {
            sequence: [], playerInput: [], level: 1, sequenceLength: 3, timeLimit: 5, timerId: null, running: false, finalLevel: 0, possibleChars: ['A', 'B', 'C', 'X', 'Y', 'Z'], sequenceDisplayEl: document.querySelector('.override-sequence-display'), buttonsContainer: document.querySelector('.override-buttons'), messageEl: document.getElementById('override-message'), levelEl: document.getElementById('override-level'), timerEl: document.getElementById('override-timer'), startBtn: document.getElementById('override-start-btn'),
            init() { this.reset(); },
            reset() { this.level = 1; this.sequenceLength = 3; this.timeLimit = 5; this.running = false; this.finalLevel = 0; if (this.timerId) clearInterval(this.timerId); this.messageEl.textContent = "Bereit für Systemübernahme."; this.levelEl.textContent = this.level; this.timerEl.textContent = "--"; this.sequenceDisplayEl.innerHTML = ""; this.startBtn.disabled = false; this.disableInputButtons(true); leaderboard.hideNicknamePrompt('override'); },
            start() { if (this.running) return; this.running = true; this.startBtn.disabled = true; this.disableInputButtons(false); this.messageEl.textContent = `Level ${this.level}: Präge dir die Sequenz ein...`; this.levelEl.textContent = this.level; this.generateSequence(); this.displaySequence(() => { this.startTimer(); this.messageEl.textContent = `Level ${this.level}: Gib die Sequenz ein!`; this.playerInput = []; }); },
            generateSequence() { this.sequence = []; for (let i = 0; i < this.sequenceLength; i++) { this.sequence.push(this.possibleChars[Math.floor(Math.random() * this.possibleChars.length)]); } },
            displaySequence(callback) { this.sequenceDisplayEl.innerHTML = ""; this.disableInputButtons(true); let i = 0; const intervalId = setInterval(() => { if (i < this.sequence.length) { this.sequenceDisplayEl.innerHTML = this.sequence.map((char, index) => `<span style="background-color: ${i === index ? 'rgba(255, 0, 255, 0.5)' : 'rgba(255, 0, 255, 0.1)'}">${char}</span>`).join(''); i++; } else { clearInterval(intervalId); this.sequenceDisplayEl.innerHTML = this.sequence.map(char => `<span>?</span>`).join(''); this.disableInputButtons(false); if (callback) callback(); } }, 800); },
            startTimer() { let timeLeft = this.timeLimit; this.timerEl.textContent = timeLeft.toFixed(1); if (this.timerId) clearInterval(this.timerId); this.timerId = setInterval(() => { timeLeft -= 0.1; this.timerEl.textContent = timeLeft.toFixed(1); if (timeLeft <= 0) { clearInterval(this.timerId); this.gameOver("Zeit abgelaufen!"); } }, 100); },
            input(char) { if (!this.running || this.playerInput.length >= this.sequence.length) return; this.playerInput.push(char); const buttonEl = Array.from(this.buttonsContainer.querySelectorAll('button')).find(b => b.textContent === char); if(buttonEl) { buttonEl.style.backgroundColor = 'rgba(0, 255, 204, 0.5)'; setTimeout(() => { buttonEl.style.backgroundColor = 'transparent'; }, 150); } if (this.sequence[this.playerInput.length - 1] !== char) { this.gameOver("Falsche Eingabe!"); return; } if (this.playerInput.length === this.sequence.length) { clearInterval(this.timerId); this.messageEl.textContent = `Level ${this.level} erfolgreich!`; this.level++; this.sequenceLength++; this.timeLimit *= 0.97; if (this.timeLimit < 2) this.timeLimit = 2; setTimeout(() => this.start(), 1500); } },
            gameOver(reason) { this.running = false; this.finalLevel = this.level; if (this.timerId) clearInterval(this.timerId); this.messageEl.textContent = `Fehlgeschlagen! Grund: ${reason}. Finales Level: ${this.finalLevel}.`; this.startBtn.disabled = false; this.disableInputButtons(true); this.timerEl.textContent = "XX"; this.sequenceDisplayEl.innerHTML = this.sequence.map(char => `<span style="color: #ff6666;">${char}</span>`).join(''); if (leaderboard.isHighScore('override', this.finalLevel)) { leaderboard.promptForNickname('override', this.finalLevel); } },
            disableInputButtons(disabled) { this.buttonsContainer.querySelectorAll('button').forEach(button => button.disabled = disabled); }
        };
        window.addEventListener('load', () => overrideGame.init());


        // Initialisiere das Leaderboard beim Laden der Seite
        window.addEventListener('load', () => leaderboard.displayLeaderboard());

    </script>

</body>
</html>
