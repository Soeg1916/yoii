# Multiple Channels Setup Guide

## How to Monitor Multiple Channels

Your system can monitor as many channels as you want simultaneously. Here's exactly how to set it up:

## Environment Variable Format

**Single Channel:**
```
TARGET_CHANNELS=Sport_433et
```

**Multiple Channels:**
```
TARGET_CHANNELS=Sport_433et,channel2,channel3,anotherchannel
```

## Real Examples

**Monitor 3 channels:**
```
TARGET_CHANNELS=Sport_433et,EthiopianNews,SportsUpdate
```

**Monitor 5 channels:**
```
TARGET_CHANNELS=Sport_433et,news_channel,tech_updates,business_news,entertainment
```

## On Render Dashboard

When adding environment variables in Render:

| Variable | Value |
|----------|-------|
| TARGET_CHANNELS | Sport_433et,channel2,channel3,channel4 |
| COMMENT_MESSAGES | hey this is me\|Hello everyone!\|Great post! |

## Important Notes

✅ **Use channel usernames** (not display names)
✅ **No @ symbol** needed
✅ **Separate with commas** only
✅ **No spaces** around commas
✅ **Join all channels first** before monitoring

## Channel Username Examples

- ✅ Good: `Sport_433et`
- ✅ Good: `news_channel`  
- ❌ Wrong: `@Sport_433et`
- ❌ Wrong: `Sport_433et, channel2` (space after comma)

## What Happens

- Bot monitors ALL channels simultaneously
- Comments on new posts in ANY of the channels
- Respects 10 comments/hour limit across ALL channels
- Logs activity for each channel separately

## Testing Multiple Channels

1. Deploy with multiple channels
2. Post in Channel 1 - bot comments
3. Post in Channel 2 - bot comments  
4. Post in Channel 3 - bot comments
5. All working = success!

Your bot will handle all channels automatically once deployed.