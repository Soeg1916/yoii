#!/bin/bash

# Clean Git Setup Script
echo "=== Setting up clean Git configuration ==="

# Prompt for user information
echo "Enter your full name:"
read -r USER_NAME

echo "Enter your email address:"
read -r USER_EMAIL

# Configure git
git config user.name "$USER_NAME"
git config user.email "$USER_EMAIL"

echo "Git configured with:"
echo "Name: $USER_NAME"
echo "Email: $USER_EMAIL"

# Add all files
git add .

# Create a professional commit message
git commit -m "Complete Telegram Channel Monitor & Auto-Commenter

Features:
- Multi-channel monitoring support
- Real-time message detection and auto-commenting
- Rate limiting (10 comments/hour) for TOS compliance
- Cloud deployment ready (Render, Railway, Heroku)
- Session string support for stateless deployment
- Comprehensive error handling and logging
- Interactive and environment variable configuration

Deployment:
- Background worker configuration
- Environment variable templates
- Step-by-step deployment guides
- Multiple platform support

Author: $USER_NAME"

echo "Clean commit created successfully!"
echo "Run 'git push origin main' to push with your identity."