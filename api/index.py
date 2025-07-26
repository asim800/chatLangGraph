#!/usr/bin/env python3
"""
Vercel entry point for FastAPI Chat Engine
This file serves as the entry point when deployed to Vercel
"""

from web_chat import app

# This is the entry point that Vercel will use
# The app object from web_chat.py contains our FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)