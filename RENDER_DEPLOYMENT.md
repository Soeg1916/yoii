# Deploy to Render.com - Step by Step Guide

## What You'll Need First

Before deploying, you need:
1. **Telegram API credentials** (from my.telegram.org)
2. **Session string** (generated using the included script)
3. **GitHub account** (to connect your code)

## Step 1: Get Your Telegram API Credentials

1. Go to https://my.telegram.org
2. Log in with your phone number
3. Click "API Development Tools"
4. Create a new application with any name
5. Save these numbers:
   - **API ID** (looks like: 12345678)
   - **API Hash** (looks like: abc123def456...)

## Step 2: Generate Your Session String

Run this locally on your computer:

```bash
python generate_session.py
```

Follow the prompts and save the long session string it gives you.

## Step 3: Deploy on Render

1. **Create Render Account**: Go to render.com and sign up
2. **Connect GitHub**: Link your GitHub account
3. **Create New Service**: 
   - Click "New +"
   - Select "Background Worker" (NOT Web Service)
4. **Connect Repository**: Select your project repository
5. **Configure Settings**:
   - **Name**: telegram-monitor
   - **Environment**: Python 3
   - **Build Command**: `pip install telethon`
   - **Start Command**: `python main.py`

## Step 4: Add Environment Variables

In Render dashboard, add these environment variables:

| Variable Name | Example Value | Your Value |
|--------------|---------------|------------|
| `TELEGRAM_API_ID` | 12345678 | [Your API ID] |
| `TELEGRAM_API_HASH` | abc123def456... | [Your API Hash] |
| `TELEGRAM_SESSION` | 1BVtsOG8Bu... | [Your session string] |
| `TARGET_CHANNELS` | Sport_433et,channel2,channel3 | [Channels to monitor] |
| `COMMENT_MESSAGES` | hey this is me\|Hello everyone! | [Comments to post] |

### Multiple Channels Format:
- **Single channel**: `Sport_433et`
- **Multiple channels**: `Sport_433et,another_channel,third_channel`

### Multiple Comments Format:
- **Single comment**: `hey this is me`
- **Multiple comments**: `hey this is me|Hello everyone!|Nice post!`

## Step 5: Deploy

1. Click "Create Background Worker"
2. Render will automatically build and deploy
3. Check the logs to ensure it's working

## What It Will Do:

✅ Monitor all your specified channels 24/7
✅ Automatically comment on new posts
✅ Respect Telegram's limits (10 comments per hour)
✅ Handle reconnections automatically
✅ Log all activity for monitoring

## Troubleshooting:

- **"Authentication failed"**: Check your API credentials
- **"Session invalid"**: Generate a new session string
- **"Channel not found"**: Make sure you've joined the channel first
- **Build fails**: Check the logs in Render dashboard

## Free Tier Limits:

Render's free tier gives you 750 hours per month, which is enough to run this 24/7.