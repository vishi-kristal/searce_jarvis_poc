# Kristal Agent PoC - Frontend

Next.js frontend application for the Kristal Agent Proof of Concept.

## Tech Stack

- **Next.js 15** (App Router)
- **React 19**
- **TypeScript**
- **Tailwind CSS**
- **Zustand** (State management)
- **Vercel AI SDK** (for streaming support)

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Copy environment variables:
```bash
cp .env.example .env
```

3. Update `.env` with your configuration:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Development

Run the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

Build for production:
```bash
npm run build
```

Start production server:
```bash
npm start
```

### Linting

Run ESLint:
```bash
npm run lint
```

### Type Checking

Run TypeScript type checking:
```bash
npm run type-check
```

## Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
├── components/            # React components
│   ├── chat/              # Chat-related components
│   ├── sources/           # Source display components
│   ├── validation/        # Validation display components
│   └── session/           # Session management components
├── lib/                    # Utilities and helpers
│   ├── api/               # API client
│   ├── store/             # State management
│   └── types/             # TypeScript types
└── public/                 # Static assets
```

## Environment Variables

- `NEXT_PUBLIC_API_URL` - Backend API URL (required)
- `NEXT_PUBLIC_AGENT_URL` - Agent API URL (optional, if making direct calls)

## Deployment

### Vercel

1. Push code to GitHub
2. Import project in Vercel
3. Set environment variables
4. Deploy

The project is configured for automatic deployments on push to main branch.

## Features

- ✅ Chat interface with message history
- ✅ Session management
- ✅ Source attribution
- ✅ Validation results display
- ✅ Error handling
- ✅ Loading states
- ✅ Responsive design

## Next Steps

- [ ] Add query examples
- [ ] Implement query history
- [ ] Add streaming support
- [ ] Improve error messages
- [ ] Add analytics

