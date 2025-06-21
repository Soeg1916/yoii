# Quick Start Guide - Telegram Monitor

## What This Does

This monitors Telegram channels and automatically posts comments on new messages. It supports:

- **Multiple channels** at once
- **Custom comment messages** 
- **Rate limiting** (10 comments per hour max)
- **24/7 monitoring** when deployed

## Deploy to Render (Recommended)

### Step 1: Get Your Credentials

1. **Get Telegram API credentials**:
   - Go to https://my.telegram.org
   - Login with your phone
   - Go to "API Development Tools" 
   - Create new app, save your API ID and API Hash

2. **Generate session string**:
   ```bash
   python generate_session.py
   ```
   Follow prompts and save the long string it gives you.

### Step 2: Deploy on Render

1. **Create account** at render.com
2. **New Background Worker** (not Web Service!)
3. **Connect your GitHub repo**
4. **Add these environment variables**:

| Variable | Your Value |
|----------|------------|
| `TELEGRAM_API_ID` | Your API ID number |
| `TELEGRAM_API_HASH` | Your API hash string |
| `TELEGRAM_SESSION` | Your session string |
| `TARGET_CHANNELS` | `Sport_433et` (or `channel1,channel2` for multiple) |
| `COMMENT_MESSAGES` | `hey this is me` (or `message1\|message2` for multiple) |

5. **Deploy** - it will start monitoring automatically!

## Multiple Channels Example

To monitor multiple channels, set:
```
TARGET_CHANNELS=Sport_433et,@another_channel,third_channel
```

## Multiple Comments Example

To use different comment messages randomly:
```
COMMENT_MESSAGES=hey this is me|Hello everyone!|Great post!|Thanks for sharing!
```

## What Happens Next

- Monitors your channels 24/7
- Posts comments on new messages
- Respects Telegram limits (max 10 comments/hour)
- Logs everything for monitoring
- Auto-reconnects if connection drops

## Troubleshooting

- **"Auth failed"**: Check your API credentials
- **"Channel not found"**: Make sure you joined the channel first
- **Build errors**: Check Render logs for details

That's it! Your bot will start working immediately after deployment.