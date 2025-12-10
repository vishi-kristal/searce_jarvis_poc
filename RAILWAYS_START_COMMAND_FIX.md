# Fix Railways Custom Start Command

## Issue

Railways has a custom start command that's overriding the Dockerfile:
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

The `$PORT` is not being expanded, causing the error.

## Solution: Update Start Command in Railways

### Option 1: Use Shell Expansion (Recommended)

1. Go to **Railways** → Your Service → **Settings**
2. Find **"Custom Start Command"** or **"Start Command"** field
3. Change it to:
   ```bash
   sh -c "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"
   ```
4. Click **Save**
5. **Redeploy** the service

### Option 2: Remove Custom Start Command (Let Dockerfile Handle It)

1. Go to **Railways** → Your Service → **Settings**
2. Find **"Custom Start Command"** or **"Start Command"** field
3. **Clear/Delete** the value (leave it empty)
4. Click **Save**
5. **Redeploy** the service

This will let the Dockerfile CMD handle the startup, which we've already fixed.

---

## Why This Happens

- Railways custom start command **overrides** the Dockerfile CMD
- The start command field might not expand shell variables
- Using `sh -c` ensures shell expansion happens
- Or removing it lets Dockerfile handle it properly

---

## Verify Fix

After updating and redeploying, check logs for:

✅ **Success:**
```
INFO:     Uvicorn running on http://0.0.0.0:XXXX
INFO:     Application startup complete.
```

❌ **Still broken:**
```
Error: Invalid value for '--port': '$PORT' is not a valid integer.
```

---

## Recommended: Option 2 (Remove Custom Command)

I recommend **Option 2** - removing the custom start command entirely. This way:
- Dockerfile handles everything
- Less configuration to manage
- Easier to maintain

The Dockerfile CMD we fixed will handle the PORT expansion correctly.

