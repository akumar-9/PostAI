# PostAI
Python based app to generate social media posts using LLM

## Features:
- Automatically generate social media posts based on your input event details.
- Supports LinkedIn (professional tone), Facebook (informal tone), Twitter (short messages), and Blog (detailed content).

## Requirements:
- Python 3.7+
- Gemini API key

## Setup:

1. Clone the repository:
   ```bash
   git clone https://github.com/akumar-9/PostAI.git
   cd PostAI
2. Create and activate a virtual environment
   ```bash
   python -m venv .venv
3. Install dependencies
   ```bash
   pip install -r requirements.txt
4. Create a .env file and add your Gemini API Key
   ```bash
   touch .env
   echo "GOOGLE_API_KEY=<your-api-key-here>" > .env
5. Run the script
   ```bash
   python generate_posts.py
