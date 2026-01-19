# Quick Start Guide - Cerebro

## Prerequisites

- Python 3.11+ (backend)
- Node.js 18+ and npm (frontend)
- Backend server running on port 8000
- Frontend server running on port 3000

## Starting the Application

### 1. Start Backend Server

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```

Backend will run on: **http://localhost:8000**

### 2. Start Frontend Server

```bash
cd frontend
npm install  # First time only
npm run dev
```

Frontend will run on: **http://localhost:3000**

### 3. Open Application

Open your browser and go to: **http://localhost:3000**

## First Time Setup

1. **You'll see the Setup Form**
   - Set your daily job application target (0-10)
   - Set your daily LeetCode problem target (0-5)
   - Click "Start Tracking"

2. **Dashboard Loads**
   - See your daily targets
   - View generated tasks (jobs + LeetCode)
   - See your orb jar (starts empty)

## Daily Workflow

### Morning Routine (Check Progress)
1. Click "Check Progress (Morning Routine)" button
2. System verifies:
   - Gmail sent emails (job applications)
   - LeetCode submissions
3. Orbs are awarded:
   - **Gold**: Target met
   - **Blue**: Target missed
4. View agent feedback messages

### Generate New Tasks
- Click "Generate New Tasks" to get fresh job listings and LeetCode problems

### Reset for New Day
- Click "Reset for New Day" to archive yesterday's tasks and generate new ones

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/setup` - Initialize user
- `GET /api/tasks/today` - Get today's tasks
- `POST /api/tasks/generate` - Generate new tasks
- `POST /api/tasks/reset` - Reset for new day
- `GET /api/verification/check-progress` - Check progress and award orbs

## Troubleshooting

### Backend won't start
- Check `.env` file exists in `backend/` directory
- Verify Python virtual environment is activated
- Check port 8000 is not in use

### Frontend won't start
- Run `npm install` in `frontend/` directory
- Check Node.js version: `node --version` (should be 18+)
- Check port 3000 is not in use

### "Failed to load dashboard data"
- Complete the setup form first
- Or manually call `/api/setup` endpoint

### CORS errors
- Ensure backend CORS is configured for `http://localhost:3000`
- Check backend is running on port 8000

## Development Notes

- Backend uses mock data for Gmail and LeetCode (no API keys required)
- All user data stored in `data/user_states/` as JSON files
- Frontend uses `demo_user` as default user ID
- API documentation available at: http://localhost:8000/docs

## Next Steps

- Add Auth0 authentication (replace `demo_user`)
- Set up Gmail API for real email verification
- Set up LeetCode API for real submission checking
- Add War Room feature
- Add Weekly Insights dashboard
