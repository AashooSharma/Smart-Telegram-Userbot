#!/bin/bash

# Install required packages
sudo apt-get update
sudo apt-get install python3-pip

# Clone the userbot repository
git clone https://github.com/your_username/your_userbot.git
cd your_userbot

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file and set environment variables
echo "API_ID=your_api_id" >> .env
echo "API_HASH=your_api_hash" >> .env
echo "NEWS_API_KEY=your_news_api_key" >> .env
echo "AUTHORIZED_USERS=sudo_user_id1,sudo_user_id2" >> .env

# Run the userbot
python main.py

