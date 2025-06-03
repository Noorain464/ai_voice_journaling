# Voice Journal AI

Voice Journal AI is a journaling application powered by AI. It allows users to record their thoughts, analyze emotions, and reflect on their journaling history.

## Features
- **Voice Recording**: Record your thoughts using the microphone.
- **AI-Powered Analysis**: Analyze emotions and generate insights from your journal entries.
- **Reflections**: View summaries and emotional trends from past journal entries.
- **User Authentication**: Secure login and signup functionality.

## Setup Instructions

### Prerequisites
- Node.js (v16 or later)
- Python (v3.10 or later)
- Supabase account

### Frontend Setup
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
2. Install dependencies:
   ```bash
   npm install
3. Start the development server:
   ```bash
   npm run dev
### Backend Setup
1. Navigate to the `backend` directory:
   ```bash
   cd backend
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Start the development server:
   ```bash
   uvicorn app.api.main:app --reload
   