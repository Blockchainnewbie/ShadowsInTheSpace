# Shadows in the Space - Project Documentation

## Project Overview
Cyberpunk-themed web application with Vue.js frontend and Flask backend. Features user authentication, dashboard, and immersive UI.

## Current Status (March 2025)
✅ Frontend: Stable (Vue 3)  
✅ Backend: Functional (Flask)  
⚠️ Security: Debug mode needs fixing  

## Tech Stack
### Frontend
- Vue.js 3
- Vite
- Tailwind CSS
- Fonts: Orbitron, Roboto Mono

### Backend 
- Python 3
- Flask
- SQLAlchemy
- Alembic (migrations)

🔴 **Flask Debug Mode Enabled**     
Location: `backend/app.py:29`  
Risk: Arbitrary code execution via Werkzeug debugger  
Solution: 
```python
app.run(debug=os.getenv('FLASK_DEBUG', 'False') == 'True')
```

### Dependency Audit
✅ Frontend: No vulnerabilities in 102 packages  
✅ Backend: Bandit scan complete (1 critical issue found)

## Development Setup
### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```

## Project Structure

```mermaid
graph TD
    A[shadowsinthespace] --> B[backend]
    A --> F[frontend]
    
    B --> BA[app.py]
    B --> BB[models.py]
    B --> BC[routes.py]    <!-- Google Analytics wurde entfernt - wird dynamisch geladen -->
    
    F --> FA[src]
    FA --> FAA[assets]
    FA --> FAB[components]
    FA --> FAC[views]
    FA --> FAD[router]
    FA --> FAE[services]
    FA --> FAF[utils]
    
    FAA --> FAAA[fonts]
    FAA --> FAAB[images]
    FAA --> FAAC[main.css]
    
    FAB --> FABA[Navbar.vue]
    FAB --> FABB[Footer.vue]
    FAB --> FABC[LoginForm.vue]
    
    FAC --> FACA[LandingPage.vue]
    FAC --> FACB[Dashboard.vue]
    FAC --> FACC[About.vue]
```

Text Version:
```
backend/
  app.py         # Main application
  models.py      # Database models
  routes.py      # API endpoints
  migrations/    # Database migrations
frontend/
  src/
    assets/      # Images/fonts/CSS
    components/  # Vue components
    views/       # Page templates
    router/      # Vue router
    services/    # API services
    utils/       # Utility functions
```

## Roadmap
- [ ] Implement CI/CD pipeline
- [ ] Add unit tests
- [ ] Dockerize application
- [ ] Implement dark/light theme toggle

## Team
Sonny - Lead Developer
