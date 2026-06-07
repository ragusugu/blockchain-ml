# React Frontend Setup Guide

The dashboard frontend lives in `src/frontend` and is built with Vite, React 18, Material UI, Axios, Framer Motion, Lucide React, and Recharts.

## Development

```bash
cd /home/sugangokul/Desktop/blockchain-ml/src/frontend
npm install
npm run dev
```

The Vite development server runs on `http://localhost:3000` and proxies `/api` requests to `http://localhost:5000`.

Start the backend in another terminal:

```bash
cd /home/sugangokul/Desktop/blockchain-ml/src/backend
python3 api/ai_dashboard.py
```

You can also start both services from the repository root:

```bash
./start.sh
```

## Production Build

```bash
cd /home/sugangokul/Desktop/blockchain-ml/src/frontend
npm run build
```

The build output is `src/frontend/dist`. Flask serves that directory in production-style local runs, and `docker/Dockerfile.frontend` copies it into nginx.

## Project Structure

```text
src/frontend/
├── package.json
├── package-lock.json
├── vite.config.js
├── index.html
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── hooks/
    │   └── useStreamingData.js
    └── components/
        ├── ErrorBoundary.jsx
        ├── Header.jsx
        ├── ModeSelector.jsx
        ├── OptionCard.jsx
        ├── StatCard.jsx
        ├── StreamingStatus.jsx
        ├── TransactionDetailsPanel.jsx
        └── TransactionTable.jsx
```

## Useful Commands

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build production assets
npm run build

# Preview production build
npm run preview
```

## API Proxy

`src/frontend/vite.config.js` proxies dashboard API calls:

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:5000',
    changeOrigin: true
  }
}
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Dependencies missing | Run `npm install` in `src/frontend` |
| Port 3000 in use | Run `npm run dev -- --port 3001` |
| API requests fail | Confirm the Flask backend is running on port 5000 |
| Production assets missing | Run `npm run build` and check `src/frontend/dist` |
