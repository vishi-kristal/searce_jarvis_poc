#!/bin/bash

# Test script to verify the application setup

echo "=== Testing Backend Setup ==="
cd backend

# Check Python version
echo "Python version:"
python3 --version

# Check if venv exists
if [ -d "venv" ]; then
    echo "✓ Virtual environment exists"
    source venv/bin/activate
    
    # Check if dependencies are installed
    echo "Checking dependencies..."
    python3 -c "import fastapi, uvicorn, httpx, pydantic_settings; print('✓ All dependencies installed')" 2>&1
    
    # Test app import
    echo "Testing app import..."
    python3 -c "from main import app; print('✓ App imports successfully'); print(f'  Routes: {len([r for r in app.routes if hasattr(r, \"path\")])} routes registered')" 2>&1
    
    deactivate
else
    echo "✗ Virtual environment not found. Run: python3 -m venv venv"
fi

echo ""
echo "=== Testing Frontend Setup ==="
cd ../frontend

# Check Node version
echo "Node version:"
node --version

# Check if node_modules exists
if [ -d "node_modules" ]; then
    echo "✓ node_modules exists"
    
    # Check if Next.js is installed
    if [ -f "node_modules/.bin/next" ]; then
        echo "✓ Next.js installed"
    else
        echo "✗ Next.js not found. Run: npm install"
    fi
else
    echo "✗ node_modules not found. Run: npm install"
fi

# Check TypeScript config
if [ -f "tsconfig.json" ]; then
    echo "✓ TypeScript config exists"
fi

echo ""
echo "=== Setup Test Complete ==="
echo ""
echo "To start the application:"
echo "1. Backend: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "2. Frontend: cd frontend && npm run dev"

