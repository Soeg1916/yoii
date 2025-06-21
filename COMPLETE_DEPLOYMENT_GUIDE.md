# Complete Render Deployment Guide - Step by Step

## PART 1: Get Your Telegram Credentials

### Step 1: Get API Credentials
1. Go to **https://my.telegram.org**
2. **Log in** with your phone number
3. Click **"API Development Tools"**
4. **Create new application**:
   - App title: `My Bot` (any name)
   - Short name: `mybot` (any name)
   - Click **"Create application"**
5. **Save these numbers**:
   - **API ID**: (example: 12345678)
   - **API Hash**: (example: abc123def456789...)

### Step 2: Generate Session String
**On your computer, run:**
```bash
python generate_session.py
```

**Enter when prompted:**
- Your API ID (from step 1)
- Your API Hash (from step 1)
- Your phone number (with country code: +1234567890)
- Verification code (Telegram will send it)

**Copy the entire session string** - it's very long text starting like "1BVtsOG8Bu..."

### Step 3: Join Your Target Channels
- Join all Telegram channels you want to monitor
- Make sure you can see messages in them
- Note down the channel usernames (example: Sport_433et)

## PART 2: Deploy on Render

### Step 4: Create Render Account
1. Go to **render.com**
2. **Sign up** with GitHub or email
3. **Verify your email**

### Step 5: Connect Your Code
1. **Upload your code to GitHub** (or use existing repo)
2. In Render dashboard, click **"New +"**
3. Select **"Background Worker"** (NOT Web Service!)
4. **Connect GitHub repository**

### Step 6: Configure Service
**Fill in these settings:**
- **Name**: `telegram-monitor`
- **Environment**: `Python 3`
- **Build Command**: `pip install telethon`
- **Start Command**: `python main.py`

### Step 7: Add Environment Variables
**In Render, scroll to "Environment Variables" and add these:**

| Variable Name | Your Value | Example |
|--------------|------------|---------|
| **TELEGRAM_API_ID** | Your API ID | 12345678 |
| **TELEGRAM_API_HASH** | Your API Hash | abc123def456... |
| **TELEGRAM_SESSION** | Your session string | 1BVtsOG8Bu... |
| **TARGET_CHANNELS** | Channels to monitor | Sport_433et,channel2,channel3 |
| **COMMENT_MESSAGES** | Comments to post | hey this is me\|Great post! |

**Important Notes:**
- For **multiple channels**: `Sport_433et,channel2,channel3` (comma-separated, no spaces)
- For **multiple comments**: `comment1|comment2|comment3` (pipe-separated)
- **No @ symbol** in channel names

### Step 8: Deploy
1. Click **"Create Background Worker"**
2. **Wait for build** (2-3 minutes)
3. **Check logs** for success

## PART 3: Verify Deployment

### Step 9: Check Logs
**Look for these SUCCESS messages:**
```
✓ Session string loaded from environment variables
✓ Using string session for cloud deployment  
✓ Authenticated as: [Your Name]
✓ Setting up target channels...
✓ Started monitoring...
```

**If you see ERROR messages:**
```
✗ Using file session for local deployment
✗ AuthKeyDuplicatedError
```
→ Your TELEGRAM_SESSION variable is missing or wrong

### Step 10: Test Your Bot
1. **Post a message** in one of your monitored channels
2. **Check if bot comments** within 1-3 seconds
3. **Try multiple channels** to verify all work

## PART 4: Multiple Channels Setup

### For Multiple Channels:
**Environment Variable:**
```
TARGET_CHANNELS=Sport_433et,news_channel,tech_updates
```

**What happens:**
- Bot monitors ALL channels simultaneously
- Comments on new posts in ANY channel
- Respects 10 comments/hour limit across all channels

### For Multiple Comments:
**Environment Variable:**
```
COMMENT_MESSAGES=hey this is me|Hello everyone!|Great post!|Thanks for sharing!
```

**What happens:**
- Bot randomly picks one comment from the list
- Different comments for variety

## PART 5: Troubleshooting

### Common Issues:

**"Build failed":**
- Check GitHub repo is public
- Verify all files are committed

**"Using file session for local deployment":**
- Add TELEGRAM_SESSION environment variable
- Regenerate session string if needed

**"Channel not found":**
- Join channels first
- Use exact channel usernames (no @)

**"Authentication failed":**
- Double-check API ID and Hash
- Generate new session string

### Success Indicators:
✅ Service shows "Running" status
✅ Logs show "Using string session for cloud deployment"
✅ Bot comments on new posts
✅ Works across all monitored channels

## Your Bot Is Now Live!

After successful deployment:
- Monitors channels 24/7
- Comments automatically on new posts
- Handles multiple channels
- Respects rate limits
- Auto-reconnects if needed

Total time: 15-20 minutes for complete setup.