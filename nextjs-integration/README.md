# Next.js Integration with FastAPI Chat Engine

This guide shows how to integrate the FastAPI chat engine with your existing Next.js frontend.

## Quick Setup

### 1. Start FastAPI Backend
```bash
# In your langStuff directory
uv run python main.py web --port 8000
```

### 2. Install Dependencies in Next.js
```bash
npm install axios
# or
yarn add axios
```

### 3. Environment Variables
Create `.env.local` in your Next.js project:
```env
NEXT_PUBLIC_CHAT_API_URL=http://localhost:8000
```

## Usage Examples

### Basic Chat Hook
See `hooks/useChat.js` for a complete React hook implementation.

### React Components
See `components/ChatInterface.jsx` for a full chat interface component.

### API Routes (Optional)
See `pages/api/chat.js` for Next.js API route proxy implementation.

## Features Available

- ✅ Real-time chat messaging
- ✅ React pattern visualization (step-by-step AI reasoning)
- ✅ Multiple prompt types (Financial, React, Coding, etc.)
- ✅ Chat history with arrow key navigation
- ✅ Session management
- ✅ Engagement scoring
- ✅ TypeScript support

## API Endpoints

- `POST /api/chat` - Send chat messages
- `GET /api/prompts` - Get available prompts
- `GET /api/sessions/{session_id}/history` - Get chat history
- `GET /api/stats` - Get engagement statistics

## Deployment Notes

For production deployment:
1. Update CORS origins in `web_chat.py`
2. Set proper environment variables
3. Consider using API routes for better security
4. Add rate limiting and authentication as needed