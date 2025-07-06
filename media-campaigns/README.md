# MarketWhine - Media Alert System for WhineAboutAI.com

A Python application to send media alerts about WhineAboutAI.com to relevant journalists and tech publications.

## Features

- **Comprehensive Media Database**: Curated list of AI and tech journalists from major publications
- **Email Templates**: Pre-built templates for different types of announcements
- **Personalized Outreach**: Automatically personalizes emails based on journalist beat and outlet
- **Flexible Targeting**: Send to all contacts or specific email addresses
- **Logging**: Detailed logging of sent emails and failures
- **Dry Run Mode**: Test campaigns without sending actual emails

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Email Credentials**:
   Set environment variables for your email account:
   ```bash
   export SENDER_EMAIL="your-email@gmail.com"
   export SENDER_PASSWORD="your-app-password"
   ```

   For Gmail, use an App Password instead of your regular password.

3. **Test the Application**:
   ```bash
   python media_alert.py --list-contacts
   ```

## Usage

### List All Contacts
```bash
python media_alert.py --list-contacts
```

### Send New Feature Announcement (Default)
```bash
python media_alert.py --template new_feature
```

### Send Site Update
```bash
python media_alert.py --template site_update
```

### Send Quick Announcement
```bash
python media_alert.py --template announcement
```

### Send to Specific Contacts
```bash
python media_alert.py --emails tips@techcrunch.com ina@axios.com
```

### Custom Email
```bash
python media_alert.py --subject "Custom Subject" --body "Custom message body"
```

### Dry Run (Test Without Sending)
```bash
python media_alert.py --dry-run --template new_feature
```

## Media Contacts

The application includes contacts from:
- **TechCrunch**: AI and enterprise tech reporters
- **The Verge**: Technology and AI coverage
- **Wired**: AI ethics and technology writers
- **Ars Technica**: Technology and AI development
- **VentureBeat**: AI industry coverage
- **Axios**: Tech policy and industry reporters
- **Mashable**: Tech and AI reporters
- **Other outlets**: Gizmodo, Engadget, MIT Tech Review, etc.

## Email Templates

### New Feature Template
Introduces WhineAboutAI.com as a new satirical platform for AI complaints.

### Site Update Template
Announces new features or milestones for existing contacts.

### Announcement Template
Quick, concise alert about the platform.

## Security Notes

- Never commit email credentials to version control
- Use environment variables for sensitive information
- Consider using OAuth2 for Gmail integration in production
- Monitor sending rates to avoid being flagged as spam

## Logging

All email activity is logged to `media_alert.log` including:
- Successful sends
- Failed attempts
- SMTP connection issues
- Contact loading problems

## File Structure

```
MarketWhine/
├── media_alert.py          # Main application
├── media_contacts.json     # Media contacts database
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
└── media_alert.log        # Log file (created on first run)
```

## Customization

### Adding New Contacts
Edit `media_contacts.json` to add new outlets and journalists:

```json
{
  "outlet": "New Publication",
  "contacts": [
    {
      "name": "Journalist Name",
      "role": "Reporter",
      "email": "journalist@publication.com",
      "beat": "AI Technology"
    }
  ]
}
```

### Creating New Templates
Modify the `create_email_templates()` method in `media_alert.py` to add new email templates.

## Best Practices

1. **Research First**: Verify journalist beats and contact information
2. **Personalize**: Use journalist names and specific beats in outreach
3. **Time Appropriately**: Send during business hours in journalist's timezone
4. **Follow Up Sparingly**: Don't spam; one follow-up maximum
5. **Track Results**: Monitor open rates and responses
6. **Respect Preferences**: Remove contacts who request no further emails

## Troubleshooting

### Common Issues

1. **SMTP Authentication Failed**:
   - Verify email credentials
   - Enable "Less secure app access" for Gmail or use App Password
   - Check if 2FA is enabled

2. **No Contacts Loaded**:
   - Verify `media_contacts.json` exists and is valid JSON
   - Check file permissions

3. **Emails Not Sending**:
   - Check internet connection
   - Verify SMTP server settings
   - Review logs for specific errors

### Getting Help

Check the log file `media_alert.log` for detailed error messages and troubleshooting information.