# Vercel Deployment Debugging Guide

## 🔍 Step-by-Step Testing Process

### **Step 1: Local Testing**
```bash
# Test the app locally first
python3 app.py

# Test API endpoints
curl http://localhost:5000/api/years
curl -X POST http://localhost:5000/api/generate_report -H "Content-Type: application/json" -d '{"report_type": "revenue"}'

# Check browser console for JavaScript errors
# Open browser dev tools and monitor console
```

### **Step 2: Check Vercel Configuration**
```bash
# Verify vercel.json is correct
cat vercel.json

# Check if app.py is the entry point
grep -A "src" vercel.json
```

### **Step 3: Manual Deployment Test**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy with debug output
vercel --prod --debug

# Check deployment logs
vercel logs
```

### **Step 4: Common Issues & Solutions**

#### **Issue: Static Files Not Found**
**Problem:** 404 errors for CSS/JS files
**Solution:** Ensure files are in `templates/` folder

#### **Issue: API Routes Not Working**
**Problem:** API endpoints returning 404
**Solution:** Verify Flask routes and Vercel configuration

#### **Issue: Environment Variables Missing**
**Problem:** MongoDB connection failing
**Solution:** Set environment variables in Vercel dashboard

#### **Issue: JavaScript Errors**
**Problem:** Frontend not loading or API calls failing
**Solution:** Check browser console, test with different browsers

## 🛠️ Debugging Commands

### **Check Vercel Status**
```bash
vercel ls
vercel inspect
```

### **Test Specific Endpoints**
```bash
# Test individual endpoints
curl https://your-app.vercel.app/api/years
curl https://your-app.vercel.app/api/fields
```

### **Local vs Production Differences**
```bash
# Compare local vs production
diff local_file.py production_app.py
```

## 📋 Quick Fixes to Try

### **Fix 1: Simplify vercel.json**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "app.py",
      "dest": "/"
    }
  ]
}
```

### **Fix 2: Add Error Logging**
```python
import logging

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error)}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": str(error)}), 500
```

### **Fix 3: Add Health Check**
```python
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})
```

## 🎯 Final Deployment Steps

1. **Test locally** - Ensure everything works
2. **Deploy to Vercel** - Push changes
3. **Monitor deployment** - Check Vercel logs
4. **Debug live app** - Test all functionality
5. **Iterate quickly** - Fix issues and redeploy

---

**Last Updated:** 2026-02-27
**Status:** Ready for deployment debugging
