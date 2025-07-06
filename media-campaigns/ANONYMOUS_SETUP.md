# Anonymous Email Setup Guide

This guide will help you configure anonymous email delivery for your media alerts.

## Overview

The anonymous email system provides several layers of protection:
- **Temporary email addresses**: Uses disposable email services
- **Randomized sender profiles**: Rotates between different sender identities
- **Delayed sending**: Adds random delays between emails
- **Tor support**: Routes traffic through Tor network (optional)

## Quick Start

### 1. Basic Anonymous Email
```bash
# Send anonymous alerts to all contacts
python3 media_alert.py --anonymous --template new_feature

# Send to specific contacts
python3 media_alert.py --anonymous --emails tips@techcrunch.com ina@axios.com

# Test anonymous functionality
python3 media_alert.py --test-anonymous
```

### 2. Dry Run (Test Mode)
```bash
# Test what would be sent anonymously
python3 media_alert.py --anonymous --dry-run --template new_feature
```

## Configuration

### Anonymous Config (`anonymous_config.json`)

The system uses several configuration options:

```json
{
  "services": {
    "guerrillamail": {
      "enabled": true,
      "priority": 1,
      "rate_limit": 10
    }
  },
  "sender_profiles": [
    {
      "name": "Tech Enthusiast",
      "from_name": "Anonymous Tech Watcher",
      "signature": "Sent anonymously for public interest"
    }
  ],
  "security": {
    "rotate_senders": true,
    "delay_between_sends": 30,
    "max_daily_sends": 50
  }
}
```

### Security Settings

- **delay_between_sends**: Wait time between emails (seconds)
- **rotate_senders**: Use different sender profiles
- **max_daily_sends**: Daily limit for anonymous emails

## Advanced: Tor Integration

For maximum anonymity, you can route emails through Tor.

### Install Tor

**Ubuntu/Debian:**
```bash
sudo apt-get install tor
```

**macOS:**
```bash
brew install tor
```

### Configure Tor

1. Start Tor service:
```bash
sudo systemctl start tor
# or
tor
```

2. Verify Tor is running:
```bash
curl --socks5 127.0.0.1:9050 https://check.torproject.org/api/ip
```

### Use Tor for Anonymous Email

```bash
# Send emails through Tor
python3 media_alert.py --tor --template new_feature

# Test Tor functionality
python3 media_alert.py --test-anonymous
```

## Anonymous Email Services

The system supports multiple anonymous email services:

### 1. GuerrillaMail
- **Pros**: Reliable, API access, multiple domains
- **Cons**: Limited features, may be blocked by some recipients
- **Rate Limit**: 10 emails/hour

### 2. HTTP Service
- **Pros**: Flexible, customizable
- **Cons**: Requires setup, may need authentication
- **Rate Limit**: 20 emails/hour

### 3. Tor + Anonymous Service
- **Pros**: Maximum anonymity, routing through Tor
- **Cons**: Requires Tor setup, slower delivery
- **Rate Limit**: Depends on service

## Email Templates

Anonymous mode includes specific templates:

### Available Templates
- `new_feature`: Introduce WhineAboutAI.com anonymously
- `site_update`: Anonymous updates about site growth
- `announcement`: Quick anonymous tips
- `whistleblower`: Confidential information sharing

### Example Anonymous Email

```
Hi Alex,

I'm writing anonymously to share information about a new platform 
that might interest your AI coverage.

WhineAboutAI.com has launched as a satirical outlet where people 
submit complaints about AI and technology failures...

Sent anonymously for public interest
```

## Best Practices

### 1. Security
- Use VPN in addition to Tor for maximum anonymity
- Rotate between different anonymous services
- Don't send too many emails from the same source
- Use realistic delays between sends

### 2. Content
- Keep messages professional and factual
- Avoid revealing identifying information
- Use generic language patterns
- Include verification suggestions

### 3. Timing
- Send during business hours
- Space out campaigns over time
- Avoid suspicious patterns (same time daily)
- Use random delays

### 4. Technical
- Test anonymous functionality regularly
- Monitor service availability
- Keep backup anonymous email services
- Update sender profiles periodically

## Troubleshooting

### Common Issues

**1. Anonymous service not working**
```bash
# Test individual services
python3 anonymous_email.py
```

**2. Tor connection failed**
```bash
# Check Tor status
sudo systemctl status tor
```

**3. Configuration errors**
```bash
# Validate JSON configuration
python3 -m json.tool anonymous_config.json
```

### Error Messages

- `"Anonymous sender not initialized"`: Check anonymous_config.json
- `"Tor connection not available"`: Install and start Tor
- `"GuerrillaMail send failed"`: Service may be down, try alternative
- `"Rate limit exceeded"`: Wait before sending more emails

## Legal and Ethical Considerations

### Important Notes
1. **Verify information**: Always ensure tips are accurate
2. **Respect privacy**: Don't expose personal information
3. **Follow laws**: Comply with local regulations
4. **Professional purpose**: Use for legitimate media outreach only
5. **Transparency**: Be honest about anonymous nature

### Recommended Disclaimers
- "This information should be verified independently"
- "Sent anonymously to protect source identity"
- "For public interest purposes only"

## Service Limitations

### Rate Limits
- GuerrillaMail: 10 emails/hour
- HTTP Service: 20 emails/hour
- Daily limit: 50 emails (configurable)

### Service Availability
- Anonymous email services may experience downtime
- Some services may be blocked by spam filters
- Tor can be slower and less reliable

### Detection
- Some email providers detect anonymous emails
- Professional journalists may verify sources
- Consider this when crafting messages

## Support

For issues with anonymous email delivery:
1. Check logs: `media_alert.log`
2. Test functionality: `--test-anonymous`
3. Verify configuration: `anonymous_config.json`
4. Check service status: Individual service APIs

Remember: Anonymous email should be used responsibly and ethically for legitimate media outreach purposes only.