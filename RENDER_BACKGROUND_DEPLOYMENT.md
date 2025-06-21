# Deploy Telegram Monitor on Render Background Worker

## Step 1: Get Your Telegram Credentials

### Get API Credentials:
1. Go to **https://my.telegram.org**
2. Log in with your phone number
3. Click **"API Development Tools"**
4. Create new application (any name)
5. Save your **API ID** and **API Hash**

### Generate Session String:
```bash
python generate_session.py
```
- Enter your API ID, API Hash, and phone number
- Save the long session string it gives you

## Step 2: Create Render Account
1. Go to **render.com**
2. Sign up with GitHub
3. Verify your email

## Step 3: Create Background Worker (NOT Web Service)

### In Render Dashboard:
1. Click **"New +"**
2. Select **"Background Worker"** (very important - NOT Web Service)
3. Connect your GitHub repository
4. Configure service:
   - **Name**: telegram-monitor
   - **Environment**: Python 3
   - **Build Command**: `pip install telethon`
   - **Start Command**: `python main.py`

## Step 4: Add Environment Variables

**Click "Environment Variables" and add these 5 variables:**

| Variable Name | Your Value | Example |
|--------------|------------|---------|
| TELEGRAM_API_ID | Your API ID | 12345678 |
| TELEGRAM_API_HASH | Your API Hash | abc123def456... |
| TELEGRAM_SESSION | Your session string | 1BVtsOG8Bu... |
| TARGET_CHANNELS | Channels to monitor | Sport_433et,channel2 |
| COMMENT_MESSAGES | Comments to post | hey this is me |

**For multiple channels:**
```
TARGET_CHANNELS=Sport_433et,news_channel,tech_updates
```

**For multiple comments:**
```
COMMENT_MESSAGES=hey this is me|Great post!|Thanks for sharing!
```

## Step 5: Deploy
1. Click **"Create Background Worker"**
2. Wait 2-3 minutes for build
3. Service should show "Running" status

## Step 6: Verify Success

**Check logs for these messages:**
```
✓ Session string loaded from environment variables
✓ Using string session for cloud deployment
✓ Authenticated as: [Your Name]
✓ Started monitoring...
```

**If you see errors:**
```
✗ Using file session for local deployment
✗ AuthKeyDuplicatedError
```
→ Check your TELEGRAM_SESSION variable

## Step 7: Test Your Bot
- Post in one of your monitored channels
- Bot should comment within 1-3 seconds
- Check Render logs to see activity

## Important Notes:

**Background Worker vs Web Service:**
- ✅ Background Worker: Runs continuously, perfect for monitoring
- ❌ Web Service: For websites, will fail for this bot

**Environment Variables:**
- All 5 variables are required
- TELEGRAM_SESSION is the most critical one
- No spaces in channel names

**Success Indicators:**
- Service status shows "Running"
- Logs show successful authentication
- Bot comments on new posts

Your bot will now monitor all specified channels 24/7 and automatically comment on new posts.
