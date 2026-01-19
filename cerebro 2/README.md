# Project Cerebro

Workflow accountability application for job seekers. Track daily goals (job applications + LeetCode), verify completion through API integrations, and get emotional feedback through an orb system.

## Project Structure

```
cerebro/
├── backend/          # FastAPI backend
├── frontend/         # React/Next.js frontend (to be implemented)
└── data/            # User state JSON files
```

## Phase 1: Core Infrastructure ✅

- ✅ FastAPI application setup
- ✅ Basic routing structure
- ✅ JSON file storage system
- ✅ User state models (Pydantic)
- ✅ Auth0 service structure (ready for integration)

## Getting Started

### Backend Setup

1. **Create virtual environment:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Test the API:**
   - Health check: http://localhost:8000/api/health
   - API docs: http://localhost:8000/docs

## API Endpoints (Phase 1)

- `GET /` - Root endpoint
- `GET /api/health` - Health check
- `GET /api/auth/me` - Get current user (placeholder)
- `POST /api/auth/login` - Login (placeholder)
- `GET /api/tasks/today` - Get today's tasks (placeholder)
- `POST /api/tasks/generate` - Generate tasks (placeholder)
- `GET /api/verification/check-progress` - Check progress (placeholder)
- `POST /api/war-room/decide` - Decision helper (placeholder)
- `GET /api/insights/weekly` - Weekly insights (placeholder)

## Next Steps (Phase 2+)

- Phase 2: Task System (Job API, LeetCode integration)
- Phase 3: Verification System (Gmail API, LeetCode checking)
- Phase 4: Frontend (React/Next.js)
- Phase 5: Advanced Features (War Room AI, Insights)
- Phase 6: Polish

## Development Notes

- Currently using `demo_user` as placeholder for user_id
- Auth0 integration structure is ready but not fully implemented
- All service integrations are stubbed with TODO comments
- Data is stored in JSON files under `data/user_states/`
