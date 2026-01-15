# 🚀 React Frontend Setup Guide

## Installation & Development

### 1. Install Dependencies
```bash
cd /home/sugangokul/Desktop/blockchain-ml/src/frontend
npm install
```

### 2. Start Development Server
```bash
npm run dev
```

This will start the Vite development server on `http://localhost:3000` with proxy to backend API.

### 3. Build for Production
```bash
npm run build
```

This creates an optimized build in `../static/` directory that the Flask backend will serve.

---

## Project Structure

```
src/frontend/
├── package.json              # Dependencies
├── vite.config.js           # Vite configuration with API proxy
├── index.html               # HTML entry point
└── src/
    ├── main.jsx             # React entry with Material-UI theme
    ├── App.jsx              # Main application component
    └── components/
        ├── Header.jsx       # Top navigation bar
        ├── OptionCard.jsx   # Option selector cards
        ├── StatCard.jsx     # Statistics display cards
        ├── TransactionTable.jsx  # Transaction data table
        └── DetailModal.jsx   # Transaction detail modal
```

---

## Key Technologies

- **React 18** - UI framework
- **Vite** - Lightning-fast build tool
- **Material-UI (MUI)** - Advanced UI components
- **Framer Motion** - Smooth animations
- **Recharts** - Data visualization
- **Axios** - HTTP client

---

## Features

### Advanced UI Design
✅ Modern Material Design 3 components  
✅ Smooth Framer Motion animations  
✅ Dark theme with gradient backgrounds  
✅ Responsive grid layout  
✅ Interactive cards with hover effects  
✅ Loading skeletons  
✅ Toast notifications  

### React Hooks
✅ useState - State management  
✅ useEffect - API calls & side effects  
✅ useCallback - Optimized callbacks  

### API Integration
✅ Axios for HTTP requests  
✅ Automatic error handling  
✅ Loading states  
✅ Real-time data updates  

---

## Development Commands

```bash
# Install dependencies
npm install

# Start development server (port 3000)
npm run dev

# Build for production
npm run build

# Preview production build
npm preview
```

---

## API Proxy Setup

The Vite config automatically proxies `/api/*` requests to the Flask backend:

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:5000',
    changeOrigin: true
  }
}
```

This allows frontend to call `/api/options` instead of `http://localhost:5000/api/options`.

---

## Building & Deployment

### Local Development
```bash
# Terminal 1: Start Flask backend
python /path/to/ai_dashboard.py

# Terminal 2: Start React dev server
cd src/frontend && npm run dev
```

Access at `http://localhost:3000`

### Production Build
```bash
# Build React app
cd src/frontend && npm run build

# Flask automatically serves from /src/static
python /path/to/ai_dashboard.py
```

Access at `http://localhost:5000`

---

## Customization

### Change Colors
Edit theme in `src/main.jsx`:
```javascript
const darkTheme = createTheme({
  palette: {
    primary: { main: '#6366f1' },      // Change primary color
    secondary: { main: '#ec4899' },    // Change secondary color
    // ...
  }
})
```

### Add New Components
1. Create component in `src/components/ComponentName.jsx`
2. Export and import in `src/App.jsx`
3. Use in JSX

### Modify Animations
All components use Framer Motion. Edit animation properties:
```javascript
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
>
  Content
</motion.div>
```

---

## Troubleshooting

### Dependencies Missing
```bash
npm install
```

### Port 3000 Already in Use
```bash
npm run dev -- --port 3001
```

### Build Errors
```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

### API Not Responding
- Verify Flask backend is running on port 5000
- Check browser console (F12) for CORS errors
- Verify network tab shows requests to `/api/`

---

## Next Steps

1. Run `npm install` to install dependencies
2. Run `npm run dev` to start development
3. Open `http://localhost:3000` in browser
4. Start building amazing features!

---

**Advanced React Dashboard with Material-UI & Framer Motion** 🚀
