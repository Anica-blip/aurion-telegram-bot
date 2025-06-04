# Aurion Telegram Bot

This bot connects Telegram, Notion, and optionally ChatGPT (via OpenAI).

## Features:
- Queries info from Notion database
- Falls back to ChatGPT if needed (only if OPENAI_API_KEY is added)

## To deploy:
1. Upload this folder to GitHub.
2. Go to https://render.com > New Web Service
3. Link your GitHub repo.
4. Add environment variables based on `.env.example`
5. Use `web: python app.py` as your start command
6. Set the Telegram webhook to: https://your-render-url/your-telegram-token
