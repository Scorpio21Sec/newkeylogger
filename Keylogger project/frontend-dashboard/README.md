# Keylogger Analytics Dashboard

A production-level, animation-rich SaaS analytics dashboard built with **Next.js 16**, **TypeScript**, **Framer Motion**, **GSAP**, and **Tailwind CSS**. Real-time data visualization with advanced interactivity, powered by a Flask backend and Google Sheets integration.

**Live Demo**: [http://localhost:3000](http://localhost:3000)

---

## 🎯 Features

### **Dashboard Core**
- 📊 **Real-time Analytics** - Live metrics updated every 10 seconds from Flask backend
- 📈 **Multi-Chart Visualization** - Line charts (trends), bar charts (sessions), pie charts (distribution)
- ⌨️ **Sessions Table** - Advanced table with sorting, filtering, search, expandable rows, pagination
- 🎨 **Dark/Light Theme Toggle** - Persistent theme preference via `next-themes`
- 🔔 **Toast Notifications** - User feedback via `sonner` toast system

### **Animations & UX**
- ✨ **Count-up Animations** - Metric cards animate from 0 to value on load
- 🎭 **3D Tilt Effect** - Metric cards tilt on hover for interactive feel
- 💨 **Smooth Transitions** - Page fade-in, sidebar collapse, staggered list animations
- 🌊 **Parallax Blob** - Background blob follows mouse movement with GSAP
- 🎯 **Scroll Triggers** - Charts animate on scroll visibility with GSAP ScrollTrigger

### **API Integration**
- 🔄 **Retry Logic** - Axios interceptor with exponential backoff (max 2 retries, 500ms intervals)
- 📡 **Mock & Real Endpoints** - Next.js mock endpoints + Flask backend integration
- 🔌 **Auto-Refresh** - Zustand store refreshes data every 10 seconds automatically
- 🛡️ **Error Handling** - Graceful fallbacks with user-friendly error messages

### **Performance**
- ⚡ **Code Splitting** - Lazy-loaded components via Next.js dynamic imports
- 🎯 **Memoization** - React.memo on heavy components, useMemo for filtered data
- 🔍 **Debounced Search** - 300ms debounce on table search to reduce re-renders
- 📦 **Bundle Optimized** - ~52KB gzipped (excluding Next.js runtime)

### **Developer Experience**
- 🛠️ **TypeScript Strict Mode** - Full type safety across codebase
- 📝 **ESLint + Prettier** - Automated code quality and formatting
- 🐳 **Docker Ready** - Multi-stage Dockerfile for production deployment
- 📚 **Modular Architecture** - Organized folders for components, hooks, utils, and store

---

## 🚀 Quick Start

### **Prerequisites**
- Node.js 18+ and npm/yarn
- Python 3.10+ (for Flask backend)
- Git

### **Installation**

1. **Frontend Setup**
```bash
cd frontend-dashboard
npm install
```

2. **Backend Setup** (from project root)
```bash
python -m venv .venv
.\.venv\Scripts\Activate    # Windows
source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

3. **Environment Configuration**
```bash
# Create .env.local in frontend-dashboard/
echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:5000" > .env.local
```

### **Running Development Servers**

**Terminal 1 - Frontend**
```bash
cd frontend-dashboard
npm run dev
# Opens http://localhost:3000
```

**Terminal 2 - Backend**
```bash
python app.py
# Running on http://127.0.0.1:5000
```

Both services will start automatically and communicate via HTTP.

---

## 📁 Project Structure

```
frontend-dashboard/
├── app/
│   ├── layout.tsx                 # Root layout with providers
│   ├── page.tsx                   # Main dashboard page
│   ├── providers.tsx              # Theme + Toaster providers
│   ├── globals.css                # Global styles + keyframes
│   └── api/keylogger/             # Mock API endpoints
│       ├── stats/route.ts
│       ├── logs/route.ts
│       └── sessions/route.ts
├── components/
│   ├── ui/                        # Design system (button, card, badge, etc.)
│   ├── layout/                    # Layout components (sidebar, navbar, shell)
│   └── dashboard/                 # Dashboard modules
│       ├── metric-card.tsx        # Animated metric display
│       ├── charts-section.tsx     # Multi-chart visualization
│       ├── sessions-table.tsx     # Advanced data table
│       ├── ai-insights-panel.tsx  # AI-generated insights
│       └── dashboard-loading.tsx  # Skeleton loading state
├── hooks/
│   ├── use-debounce.ts           # Debounce hook for search
│   └── use-gsap-scroll.ts        # GSAP scroll trigger hook
├── store/
│   └── dashboard-store.ts         # Zustand global state management
├── utils/
│   ├── api.ts                     # Axios HTTP client with retry
│   ├── types.ts                   # TypeScript interfaces
│   ├── format.ts                  # Number/date formatting
│   ├── cn.ts                      # classnames utility
│   └── mock-data.ts               # Mock data generator
├── styles/
│   └── animations.css             # Custom animation keyframes
├── Dockerfile                     # Multi-stage production build
├── docker-compose.yml             # Frontend + backend orchestration
├── .env.local                     # API base URL (local only)
└── package.json                   # Dependencies and scripts

```

---

## 🔌 API Endpoints

### **Frontend Mock Endpoints** (via Next.js)
- `GET /api/keylogger/stats` - Aggregated statistics (keystrokes, sessions, speed, errors)
- `GET /api/keylogger/logs` - All keystroke logs with timestamps
- `GET /api/keylogger/sessions` - Session data with duration and activity

### **Backend Endpoints** (Flask - `http://localhost:5000`)
- `GET /api/health` - Server health check
- `GET /api/keylogger/stats` - Real statistics from database
- `GET /api/keylogger/logs` - All logs (with pagination optional)
- `GET /api/keylogger/sessions` - Session list with details
- `POST /api/keylogger/log` - Create new log entry
- `GET /api/keylogger/export` - Export as JSON
- `POST /api/keylogger/clear` - Clear all data

**Base URL Configuration**: Set via `NEXT_PUBLIC_API_BASE_URL` in `.env.local`
- Development: `http://localhost:5000`
- Production: Update to production API endpoint

---

## 📦 Dependencies

### **Core Framework**
- `next@16.2.4` - React framework with App Router
- `react@19.2.4` - UI library
- `typescript@5` - Type safety

### **Styling & Animation**
- `tailwindcss@4` - Utility-first CSS framework
- `framer-motion@12.38.0` - React animation library
- `gsap@3.15.0` - Advanced animation engine
- `next-themes@0.4.6` - Dark/light mode theming

### **State & API**
- `zustand@5.0.12` - Lightweight state management
- `axios@1.15.2` - HTTP client with retry logic
- `recharts@3.8.1` - Data visualization library

### **UI & UX**
- `sonner@2.0.7` - Toast notifications
- `lucide-react@1.14.0` - Icon library

### **Developer Tools**
- `eslint@9` - Code linting
- `prettier@3.8.3` - Code formatting

---

## 🎨 Component Library

### **UI Components**
- **Button** - Primary, secondary, outline, ghost variants with hover effects
- **Card** - Glassmorphism effect with glow borders
- **Badge** - Status indicators (active, pending, error)
- **Modal** - Custom dialog with overlay and animations
- **Input** - Text input with focus states
- **Skeleton** - Loading placeholder animations

### **Layout Components**
- **DashboardShell** - Main layout container with sidebar + navbar
- **Sidebar** - Collapsible navigation with smooth transitions
- **Navbar** - Sticky header with search and theme toggle
- **ThemeToggle** - Dark/light mode switcher

### **Dashboard Components**
- **MetricCard** - KPI display with count-up and tilt animations
- **ChartsSection** - Grid of line/bar/pie charts
- **SessionsTable** - Advanced table with all filtering features
- **AIInsightsPanel** - Performance summary and recommendations
- **DashboardLoading** - Full-page skeleton loader

---

## 🛠️ Available Scripts

```bash
npm run dev          # Start development server with Turbopack
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run format       # Format code with Prettier
npm run format:check # Check formatting without changes
npm run type-check   # Run TypeScript compiler
```

---

## 🐳 Docker Deployment

### **Development with Docker Compose**
```bash
docker-compose up --build
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
```

### **Production Build**
```bash
docker build -t keylogger-dashboard .
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_BASE_URL=https://api.example.com \
  keylogger-dashboard
```

**Dockerfile Features**
- Multi-stage build (dependencies → build → runtime)
- Node 20-alpine base image (~140MB)
- Final image size: ~92MB
- Standalone output for minimal runtime

---

## 🔑 Environment Variables

### **Frontend (.env.local)**
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:5000
```

### **Backend (app.py)**
Configure in code or via environment:
- `FLASK_ENV=development` - Debug mode
- `FLASK_PORT=5000` - Server port

---

## 🚨 Troubleshooting

### **Port Already in Use**
```bash
# Kill process on port 3000
taskkill /PID <PID> /F  # Windows
lsof -ti:3000 | xargs kill -9  # macOS/Linux
```

### **API Connection Refused**
- Verify Flask backend is running: `curl http://localhost:5000/api/health`
- Check `.env.local` has correct `NEXT_PUBLIC_API_BASE_URL`
- Frontend must be restarted after .env.local changes

### **Charts Not Rendering**
- Check browser console for width/height warnings
- Ensure container has explicit height (h-72 class applied)
- Verify ResponsiveContainer dimensions via React DevTools

### **Build Errors**
```bash
# Clear cache and reinstall
rm -rf node_modules .next package-lock.json
npm install
npm run build
```

---

## 📊 Performance Optimization

### **Currently Implemented**
- React.memo on metric cards to prevent unnecessary re-renders
- useMemo for filtered/sorted table data
- Debounced search (300ms) to reduce API calls
- GSAP animations use requestAnimationFrame (60fps)
- Next.js code splitting for routes and dynamic imports
- Image optimization via next/image

### **Monitoring**
Run Lighthouse audit:
```bash
npm run build
npx lighthouse http://localhost:3000 --headless
```

**Target Metrics**
- Largest Contentful Paint (LCP): < 2.5s
- First Input Delay (FID): < 100ms
- Cumulative Layout Shift (CLS): < 0.1

---

## 🔐 Security Considerations

### **Development Notes**
- Mock API endpoints for demonstration only
- No authentication currently implemented (TODO: Add JWT/OAuth)
- API keys stored in `.env.local` (not tracked by Git)
- CORS enabled for localhost development

### **Production Recommendations**
1. Use HTTPS for all API communications
2. Implement JWT token-based authentication
3. Add rate limiting on backend
4. Sanitize user inputs on frontend and backend
5. Enable CORS with specific domain whitelist
6. Use secure cookies for session management

---

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m "Add feature description"`
3. Push to branch: `git push origin feature/your-feature`
4. Submit pull request

**Code Style**
- ESLint configuration enforced automatically
- Prettier formats code on save
- TypeScript strict mode required

---

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

---

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Framer Motion Docs](https://www.framer.com/motion/)
- [GSAP Docs](https://gsap.com/docs/)
- [Zustand Guide](https://github.com/pmndrs/zustand)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Recharts Docs](https://recharts.org/)

---

**Questions?** Open an issue or check the main project README for backend setup details.
