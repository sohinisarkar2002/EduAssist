# EduAssist
Being a current BSc student at IIT Madras, trying to design a comprehensive TA-support platform for IIT Madras BS courses to streamline teaching assistance, automate administrative tasks, enhance student guidance, and improve communication through intelligent tools like RAG-based assistants, structured workflows, and priority-driven learning aids.

EduAssist is an AI-powered teaching assistant platform designed to help educators create high-quality content, engage students more effectively, and reduce repetitive administrative work.

⚠️ Project Status: This project is currently under active development. Some features are partially implemented or use mock data. The roadmap below outlines what is planned next.

🌐 Live Demo: https://eduassist-nine.vercel.app/

✨ Why EduAssist?
    Educators spend a significant amount of time on:
    Preparing study materials
    Creating assessments
    Explaining complex topics repeatedly
    Managing feedback and administrative tasks
    EduAssist aims to centralize and automate these workflows using AI — so educators can focus on teaching, not tooling.

**🧠 Core Features**

Currently Implemented / In Progress:

  Knowledge Assistant
    AI-powered responses to student questions with structured explanations
  Study Guide Generator
    Generate study guides from lecture notes or topics
  Assessment Generator
    Auto-generate quizzes and assessments (logic in progress)
  Slide Deck Generator
    Convert lecture notes into structured slide outlines
  Content Priority Tagger
    Identify high-priority or confusing content areas (UI ready, logic evolving)
  Student Feedback System
    Collect feedback via structured UI (API integration pending)
  Settings Management
    Profile, security, and preference management

**🛠️ Tech Stack**

Frontend
  Next.js 14 (App Router)
  TypeScript
  Tailwind CSS
  Lucide React
  React Hooks

Backend
  FastAPI
  Python 3.12+
  PostgreSQL (Neon recommended)
  uv (Python dependency manager)
  Google Gemini API (AI layer)
  SendGrid (email workflows)

Design Philosophy
  Minimal & professional UI
  Fully responsive layout
  Accessibility-aware components
  Consistent typography and color system

**📁 Project Structure**
.
    frontend/
        app/
            page.tsx              # Landing page
            login/                # Authentication
            signup/
            forgot-password/
            dashboard/            # Main application
            settings/
            features/
                knowledge-assistant/
                study-guide-generator/
                assessment-generator/
                slide-deck-generator/
                content-priority-tagger/
            layout.tsx
            globals.css
        components/
            AppLayout.tsx
        config files
    backend/
        env.example
        launch.sh
        FastAPI source (WIP)
    README.md


**🚀 Getting Started**

Prerequisites:

  Frontend
    Node.js 18+
    npm / yarn / pnpm
    Git
  
  Backend
    Python 3.12+
    uv installed
    PostgreSQL database


Frontend Setup

  git clone <repo-url>
  cd eduassist/frontend
  npm install

  Create .env.local:
    NEXT_PUBLIC_API_URL=http://localhost:8000

  Run:
    npm run dev
    Open http://localhost:3000


Backend Setup

  cd backend
  cp .env.example .env

  Update .env:
    DATABASE_URL=postgresql://user:password@host:port/db
    GOOGLE_GEMINI_API_KEY=your_key
    SENDGRID_API_KEY=your_key
    SECRET_KEY=your_secret
    FRONTEND_URL=http://localhost:3000
  
  Start server:
    source launch.sh
  
  API Docs: http://localhost:8000/docs


**Development Workflow**
  # Frontend
  npm run dev
  npm run build
  npm run lint
  
  # Backend
  source backend/launch.sh
  
  Styling
    Color Palette
    Primary: #0d141b
    Secondary: #4c739a
    Accent: #1380ec
    Backgrounds: slate-50, neutral-50
  
  Customized in:
    frontend/tailwind.config.js


**Deployment**
  Frontend
    Deployed on Vercel
    Root directory: /frontend
    Environment variables required
  Backend
    Deployable on Railway / Render / Fly.io
    PostgreSQL via Neon
