# Multi-Channel Monitoring Examples

The Telegram Monitor now supports monitoring multiple channels simultaneously!

## Configuration Examples:

### Local Configuration (config.ini):
```ini
[monitor]
target_channels = Sport_433et,channel2,channel3
comment_messages = hey this is me
```

### Environment Variables for Cloud Deployment:
```bash
TARGET_CHANNELS=Sport_433et,AnotheTelegramChannnel,ThirdChannel
COMMENT_MESSAGES=hey this is me
```

### Interactive Setup:
When running locally, you can enter:
```
Enter target channels (comma-separated): Sport_433et,news_channel,sports_updates
```

## How It Works:

1. **Setup**: The monitor connects to all specified channels
2. **Monitoring**: Listens for new messages from ANY of the channels
3. **Commenting**: Posts "hey this is me" on new posts from any channel
4. **Logging**: Shows which channel each message came from

## Example Output:
```
2025-06-21 08:15:32 - INFO - Setting up 3 target channels
2025-06-21 08:15:33 - INFO - Channel setup complete: @Sport_433et -> 4-3-3 ስፖርት በኢትዮጵያ™
2025-06-21 08:15:34 - INFO - Channel setup complete: @news_channel -> Daily News Updates
2025-06-21 08:15:35 - INFO - Channel setup complete: @sports_updates -> Sports Central
2025-06-21 08:15:35 - INFO - Successfully monitoring 3 channels
2025-06-21 08:15:36 - INFO - Monitor is now active for 3 channels. Waiting for new messages...
2025-06-21 08:16:45 - INFO - New message detected in 4-3-3 ስፖርት በኢትዮጵያ™: ID 323010
2025-06-21 08:17:23 - INFO - New message detected in Daily News Updates: ID 445621
```

## Backward Compatibility:
- Still works with single channel using `TARGET_CHANNEL`
- Existing config files automatically upgrade to multi-channel format

## Rate Limiting:
- Same 10 comments/hour limit applies across ALL channels
- Fair distribution across channels when multiple posts arrive simultaneously