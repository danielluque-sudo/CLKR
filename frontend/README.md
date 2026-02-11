# 🎨 Colombian Legal Database - Frontend

Modern, beautiful frontend for the Colombian Legal Database built with Next.js 15, TypeScript, and Tailwind CSS.

## ✨ Features

- 🔍 **Smart Search** - Semantic search interface for Colombian laws
- ⚙️ **Scraper Dashboard** - Control and monitor scraping operations
- 📊 **Statistics** - Visual analytics and insights
- 🎨 **Modern Design** - Glassmorphism, gradients, and smooth animations
- 📱 **Fully Responsive** - Works on all devices
- 🌙 **Dark Mode** - Automatic dark mode support
- ⚡ **Fast** - Built with Next.js 15 App Router

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn
- Backend API running (see main README)

### Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env.local

# Edit .env.local with your API URL
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Development

```bash
# Start development server
npm run dev

# Open http://localhost:3000
```

### Build for Production

```bash
# Build
npm run build

# Start production server
npm start
```

## 📁 Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── page.tsx           # Home page
│   ├── search/            # Search page
│   ├── scraper/           # Scraper dashboard
│   ├── stats/             # Statistics page
│   ├── layout.tsx         # Root layout
│   └── globals.css        # Global styles
├── components/            # Reusable components
│   ├── Navbar.tsx         # Navigation bar
│   ├── FeatureCard.tsx    # Feature cards
│   └── StatsCard.tsx      # Statistics cards
├── lib/                   # Utilities
│   └── api.ts            # API client
└── public/               # Static assets
```

## 🎨 Design System

### Colors

- **Primary**: Blue (#3b82f6) → Purple (#8b5cf6)
- **Secondary**: Various gradients
- **Accent**: Cyan (#06b6d4)
- **Success**: Green (#10b981)
- **Error**: Red (#ef4444)

### Components

- **Glass Effect**: Glassmorphism with backdrop blur
- **Gradient Text**: Multi-color gradient headings
- **Cards**: Hover effects with shadow and scale
- **Buttons**: Gradient backgrounds with glow effects

## 🔌 API Integration

The frontend connects to the FastAPI backend. Configure the API URL in `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production (Railway):
```env
NEXT_PUBLIC_API_URL=https://your-api.railway.app
```

## 📱 Pages

### Home (`/`)
- Hero section with CTAs
- Feature showcase
- Statistics overview
- Call-to-action sections

### Search (`/search`)
- Search bar with filters
- Results display
- Year and type filters
- Pagination (coming soon)

### Scraper (`/scraper`)
- Configuration panel
- Start/Stop controls
- Real-time progress
- Statistics dashboard

### Stats (`/stats`)
- Coming soon: Charts and analytics

## 🚀 Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Railway

1. Push to GitHub
2. Connect Railway to your repo
3. Set environment variables
4. Deploy automatically

## 🛠️ Tech Stack

- **Framework**: Next.js 15
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4.0
- **Fonts**: Geist Sans & Mono
- **Deployment**: Vercel / Railway

## 📄 License

MIT

---

**Built with ❤️ for Colombian Legal Research**
