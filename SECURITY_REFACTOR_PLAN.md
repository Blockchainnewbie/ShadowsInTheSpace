# Security & Clean Code Refactoring Plan

## Phase 1: Kritische Sicherheitsupdates (Sofortmaßnahmen)

### 1. Authentifizierungshärtung
- [x] Passwort-Hashing von SHA-256 auf Argon2id migrieren
- [x] Rate-Limiting für Login-Endpoints (5 Versuche/Minute)
- [ ] JWT-Invalidierung implementieren

```python
# Beispiel: Flask-Limiter Konfig
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)
```

### 2. Input Validation
- [ ] Marshmallow-Schemas für alle API-Endpoints
- [ ] Zentrale Error-Handler-Klasse
- [ ] Request-Sanitization Middleware

## Phase 2: Architekturverbesserungen

### 1. Schichtenarchitektur
```
└── app/
    ├── routes/          # Nur HTTP-Handler
    ├── services/        # Business-Logik
    ├── repositories/    # DB-Interaktionen  
    └── schemas/         # Validation
```

### 2. SOLID-Prinzipien
- [ ] Single Responsibility für Routes
- [ ] Dependency Injection für Services
- [ ] Interface-Segregation für DB-Layer

## Phase 3: Monitoring & Compliance

### 1. Tool-Integration
| Tool          | Zweck                     | Konfigurationsdatei       |
|---------------|---------------------------|---------------------------|
| Bandit        | Python SAST               | `.bandit.yml`             |
| Trivy         | Container-Scans           | `trivy.yaml`              |
| OWASP ZAP     | DAST-Tests                | `zap.conf`                |

### 2. CI/CD-Pipeline
```yaml
jobs:
  security:
    steps:
      - name: SAST Scan
        run: bandit -r backend/ -f json -o sast.json
      - name: Dependency Check
        uses: dependency-check/action@v3
```

## Phase 4: Langfristige Maßnahmen

### 1. Dokumentation
- [ ] OpenAPI-Spezifikation
- [ ] Threat-Model-Dokument

### 2. Schulungen
- [ ] OWASP Top 10 Workshop
- [ ] Secure Coding Guidelines

## Implementierungsreihenfolge

1. Sicherheitskritische Patches (Phase 1)
2. Architektur-Refactoring (Phase 2) 
3. CI/CD-Integration (Phase 3)
4. Dokumentation (Phase 4)

## Verifikation

```bash
# Sicherheitstests durchführen
docker run -it --rm owasp/zap2docker-stable zap-baseline.py -t http://localhost:5000

# Code-Qualität prüfen
flake8 --config .flake8 backend/
