# Fix: Using Start Script for PORT Expansion

## Issue

Railways is not expanding `${PORT:-8000}` in the start command. The shell syntax isn't being processed.

## Solution: Use a Start Script

Created `backend/start.sh` that properly handles PORT expansion using bash.

## What Changed

1. **Created `backend/start.sh`** - Shell script that expands PORT
2. **Updated Dockerfile** - Uses the start script instead of direct CMD
3. **Script handles PORT** - Expands `${PORT:-8000}` correctly

## Next Steps

### Option 1: Remove Custom Start Command (Recommended)

1. Go to **Railways** → Your Service → **Settings**
2. Find **"Custom Start Command"** or **"Start Command"**
3. **Clear/Delete** it completely (leave empty)
4. Click **Save**
5. **Redeploy**

The Dockerfile will now use the start script which handles PORT correctly.

### Option 2: Set Start Command to Use Script

If you must keep a custom start command, set it to:
```bash
/app/start.sh
```

But **Option 1 is better** - just remove the custom command entirely.

## How It Works

The `start.sh` script:
1. Gets PORT from environment (Railways sets this automatically)
2. Defaults to 8000 if PORT is not set
3. Runs uvicorn with the correct port

This ensures shell expansion happens properly.

## Verify

After redeploying, check logs for:

✅ **Success:**
```
INFO:     Uvicorn running on http://0.0.0.0:XXXX
```

❌ **Still broken:**
```
Error: Invalid value for '--port': '${PORT:-8000}' is not a valid integer.
```

## Important

**You MUST remove the custom start command in Railways Settings** for this to work. The Dockerfile CMD will handle everything.

