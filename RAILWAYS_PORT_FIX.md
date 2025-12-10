# Fix: Invalid value for '--port': '$PORT' is not a valid integer

## Issue

Railways is trying to use `$PORT` as a literal string instead of expanding it to the actual port number.

## Solution

The Dockerfile and railway.json have been updated to properly handle the PORT environment variable.

## What Changed

### Dockerfile
Changed from:
```dockerfile
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

To:
```dockerfile
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
```

### railway.json
Updated start command to use shell expansion:
```json
"startCommand": "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"
```

## Next Steps

1. **Code has been pushed to GitHub** - The fix is ready
2. **Railways will auto-redeploy** - Or manually redeploy
3. **Check logs** - Should see "Uvicorn running on..." instead of port errors

## Alternative: Set Start Command in Railways UI

If the fix doesn't work, you can also set it manually:

1. Go to **Railways** → Your Service → **Settings**
2. Find **"Start Command"** field
3. Set it to:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
   ```
4. **Save** and **Redeploy**

## Verify Fix

After redeploying, check logs for:
```
INFO:     Uvicorn running on http://0.0.0.0:XXXX (Press CTRL+C to quit)
```

Instead of:
```
Error: Invalid value for '--port': '$PORT' is not a valid integer.
```

## How PORT Works in Railways

- Railways automatically sets `PORT` environment variable
- The `${PORT:-8000}` syntax means: use `$PORT` if set, otherwise use 8000
- This ensures it works both locally (port 8000) and on Railways (dynamic port)

