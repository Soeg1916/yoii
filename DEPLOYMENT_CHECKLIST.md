# Render Deployment Checklist ✓

## Pre-Deployment Requirements

### 1. Telegram API Setup
- [ ] Created account at https://my.telegram.org
- [ ] Generated API ID and API Hash
- [ ] Saved credentials securely

### 2. Session String Generation
- [ ] Run `python generate_session.py` locally
- [ ] Completed phone verification
- [ ] Saved session string (long encrypted text)

### 3. Channel Access
- [ ] Joined all target Telegram channels
- [ ] Verified you can post in channels (if required)
- [ ] Listed channel usernames (e.g., Sport_433et)

## Deployment Steps

### 1. Render Account Setup
- [ ] Created account at render.com
- [ ] Connected GitHub account
- [ ] Verified email if required

### 2. Service Creation
- [ ] Selected "Background Worker" (NOT Web Service)
- [ ] Connected your GitHub repository
- [ ] Named service (e.g., "telegram-monitor")

### 3. Environment Variables
Add these in Render dashboard:

- [ ] `TELEGRAM_API_ID` = [Your API ID number]
- [ ] `TELEGRAM_API_HASH` = [Your API hash string]  
- [ ] `TELEGRAM_SESSION` = [Your session string]
- [ ] `TARGET_CHANNELS` = [Channels to monitor]
- [ ] `COMMENT_MESSAGES` = [Comments to post]

### 4. Build Configuration
- [ ] Build Command: `pip install telethon`
- [ ] Start Command: `python main.py`
- [ ] Environment: Python 3

### 5. Deploy
- [ ] Click "Create Background Worker"
- [ ] Wait for build to complete
- [ ] Check logs for successful start

## Post-Deployment Verification

### 1. Monitor Logs
- [ ] Service shows "Running" status
- [ ] No error messages in logs
- [ ] Sees "Starting Telegram Channel Monitor..." message
- [ ] Shows successful authentication

### 2. Test Functionality
- [ ] Post a test message in monitored channel
- [ ] Verify bot comments on new posts
- [ ] Check rate limiting is working
- [ ] Monitor for 24 hours to ensure stability

## Configuration Examples

**Single Channel:**
```
TARGET_CHANNELS=Sport_433et
COMMENT_MESSAGES=hey this is me
```

**Multiple Channels:**
```
TARGET_CHANNELS=Sport_433et,channel2,channel3
COMMENT_MESSAGES=hey this is me|Hello everyone!|Great post!
```

## Troubleshooting

**Build Fails:**
- Check GitHub repository is public or Render has access
- Verify all files are committed and pushed

**Authentication Errors:**
- Regenerate session string
- Double-check API credentials
- Ensure session wasn't used elsewhere

**Channel Errors:**
- Join channels first before monitoring
- Use exact channel usernames
- Remove @ symbol from channel names

**Service Stops:**
- Check logs for error messages
- Verify Render free tier limits
- Restart service if needed

## Success Indicators

✅ Service status shows "Running"
✅ Logs show successful authentication  
✅ Bot responds to new channel posts
✅ Rate limiting prevents spam
✅ Service runs continuously for 24+ hours

Your Telegram monitor is ready for 24/7 operation!