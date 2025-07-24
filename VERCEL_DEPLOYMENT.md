# FastAPI Chat Engine - Vercel Deployment Guide

## Quick Deployment Steps

### 1. Deploy to Vercel
```bash
# From this directory (/home/saahmed1/coding/projects/llms/langStuff/)
npm install -g vercel  # If not already installed
vercel login          # Login to your Vercel account
vercel                # Deploy the project
```

### 2. Set Environment Variables in Vercel
After deployment, go to your Vercel dashboard and add these environment variables:

**Required:**
- `OPENAI_API_KEY` - Your OpenAI API key (from your .env file)

**Optional (if using):**
- `ANTHROPIC_API_KEY` - Your Anthropic API key

### 3. Get Your Deployment URL
After deployment, Vercel will give you a URL like:
`https://langstuff-abc123.vercel.app`

### 4. Update Next.js Environment
In your Next.js finance app, update `.env.local`:
```bash
FASTAPI_CHAT_URL=https://your-actual-deployment-url.vercel.app
```

### 5. Test Deployment
Visit these URLs to verify deployment:
- `https://your-deployment.vercel.app/` - Chat interface
- `https://your-deployment.vercel.app/docs` - API documentation
- `https://your-deployment.vercel.app/api/chat` - API endpoint

## Files Created for Vercel Deployment

### Core Files:
- ✅ `main.py` - Vercel entry point
- ✅ `vercel.json` - Vercel configuration  
- ✅ `requirements.txt` - Updated dependencies
- ✅ `web_chat.py` - Updated CORS for mystocks.ai

### Your Existing Files (Unchanged):
- `chatbot_framework/` - Your chat framework
- `tools/` - Financial tools
- `prompts.py` - Prompt templates
- All other existing functionality

## After Deployment

### Access Points:
- **Via Next.js Proxy**: `mystocks.ai/api/fastapi/agentic/`
- **Direct Access**: `your-deployment.vercel.app/`

### Next Steps:
1. Deploy this FastAPI project to Vercel
2. Update `FASTAPI_CHAT_URL` in your Next.js `.env.local`
3. Deploy your Next.js app with the new proxy route
4. Test the integration

## Troubleshooting

### Common Issues:
1. **Import Errors**: Make sure all dependencies are in `requirements.txt`
2. **CORS Issues**: Check that mystocks.ai is in the allowed origins
3. **Environment Variables**: Ensure OpenAI API key is set in Vercel dashboard
4. **Proxy Issues**: Verify `FASTAPI_CHAT_URL` is correct in Next.js

### Testing Commands:
```bash
# Test FastAPI deployment directly
curl https://your-deployment.vercel.app/api/prompts

# Test via Next.js proxy  
curl https://mystocks.ai/api/fastapi/agentic/api/prompts
```