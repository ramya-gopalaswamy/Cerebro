# Troubleshooting Guide

## "Not Found" Error When Clicking "Start Tracking"

### Issue
Getting 404 Not Found error when submitting the setup form.

### Solution

**The backend server needs to be restarted** to pick up the latest code changes.

### Steps to Fix

1. **Stop the current backend server:**
   - Go to the terminal where `uvicorn` is running
   - Press `Ctrl+C` to stop it

2. **Restart the backend server:**
   ```bash
   cd /Users/ramyag/cerebro/backend
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

3. **Verify the endpoint is working:**
   ```bash
   curl -X POST "http://localhost:8000/api/setup?user_id=test" \
     -H "Content-Type: application/json" \
     -d '{"daily_target": {"apps": 3, "leetcode": 1}}'
   ```

4. **Try the setup form again** in the browser

### Why This Happens

- FastAPI with `--reload` should auto-reload, but sometimes it doesn't catch all changes
- The setup router was updated to use `Query` for the `user_id` parameter
- The server needs to reload to pick up the import changes

### Alternative: Check Server Logs

If restarting doesn't work, check the server logs for errors:
- Look for import errors
- Look for route registration errors
- Check if the setup router is being loaded

### Verify Route is Registered

After restarting, you can verify the route is available:
- Visit: http://localhost:8000/docs
- Look for `/api/setup` endpoint in the Swagger UI
- Or check: http://localhost:8000/openapi.json

## Other Common Issues

### CORS Errors
- Ensure backend CORS is configured for `http://localhost:3000`
- Check `backend/app/config.py` for `cors_origins`

### Frontend Can't Connect
- Verify backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in frontend `.env.local` (or uses default)
- Test: `curl http://localhost:8000/api/health`

### "User already set up" Error
- Delete the user's JSON file: `data/user_states/demo_user.json`
- Or use a different `user_id` in the setup form
