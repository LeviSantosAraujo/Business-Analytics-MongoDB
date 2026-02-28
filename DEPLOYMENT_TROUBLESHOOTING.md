# Vercel Deployment Troubleshooting Guide

## 🚨 Common Issues and Solutions

### **Issue 1: 404 Errors on Vercel**

**Problem:** Static files not found or HTML not serving correctly

**Solutions:**
1. **Check vercel.json routes** - Ensure `src` points to correct entry file
2. **Verify static file serving** - Use `send_file()` instead of complex routing
3. **Check file paths** - Ensure HTML file exists and paths are correct

### **Issue 2: API Endpoints Not Working**

**Problem:** Backend not responding or returning errors

**Solutions:**
1. **Check Vercel logs** - Look at function execution logs
2. **Verify environment variables** - MongoDB connection string must be set
3. **Test locally** - Run `python3 index.py` to verify functionality
4. **Check API responses** - Use curl or Postman to test endpoints

### **Issue 3: JavaScript Not Loading**

**Problem:** Frontend JavaScript errors or API calls failing

**Solutions:**
1. **Check browser console** - Look for JavaScript errors
2. **Verify API URLs** - Ensure base URL is correct
3. **Test API endpoints** - Check if `/api/years` returns data
4. **Check network requests** - Use browser dev tools to inspect failed requests

### **Issue 4: Database Connection**

**Problem:** MongoDB Atlas connection failing

**Solutions:**
1. **Check connection string** - Verify format and credentials
2. **Network access** - Ensure IP is whitelisted in MongoDB Atlas
3. **Cluster status** - Verify MongoDB Atlas cluster is active
4. **Test connection locally** - Use connection test script

## 🔧 Quick Debugging Steps

### **Step 1: Check Vercel Deployment**
```bash
# Check deployment status
vercel ls

# Check logs
vercel logs

# Inspect specific function
vercel logs --filter="api/generate_report"
```

### **Step 2: Test API Endpoints**
```bash
# Test years endpoint
curl https://your-app.vercel.app/api/years

# Test report generation
curl -X POST https://your-app.vercel.app/api/generate_report \
  -H "Content-Type: application/json" \
  -d '{"report_type": "revenue", "years": ["2025", "2024"]}'
```

### **Step 3: Local Testing**
```bash
# Run locally to verify everything works
python3 index.py

# Test with different browsers
# Check console for JavaScript errors
```

### **Step 4: Common Fixes**

**Fix 1: Update vercel.json**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "index.py",
      "dest": "/"
    }
  ]
}
```

**Fix 2: Simplify API Structure**
```python
# Use single file with minimal dependencies
from flask import Flask, jsonify, send_file

@app.route('/')
def index():
    return send_file('templates/simple_index.html')

@app.route('/api/<path:path>')
def api_proxy(path):
    # Proxy to handle all API routes
    return jsonify({"message": "API endpoint not available"})
```

## 🎯 Production Deployment Checklist

### **Before Deploying to Vercel:**
- [ ] **Test locally** - Everything works on localhost:5002
- [ ] **Check API endpoints** - All endpoints return correct responses
- [ ] **Verify database connection** - MongoDB Atlas connection works
- [ ] **Test frontend** - All buttons and charts work correctly
- [ ] **Check environment variables** - All required variables set
- [ ] **Review logs** - No errors in Vercel logs

### **After Deployment:**
- [ ] **Monitor live site** - Check if dashboard loads correctly
- [ ] **Test all features** - Verify each button and chart works
- [ ] **Check mobile responsiveness** - Test on different screen sizes
- [ ] **Verify data loading** - Ensure charts display real data

## 📞 Support Resources

- **Vercel Docs**: https://vercel.com/docs
- **Flask Deployment**: https://vercel.com/guides/deploying-flask
- **MongoDB Atlas**: https://docs.mongodb.com/manual/reference/connection-string

## 🚀 Emergency Rollback

If deployment fails completely:
```bash
# Revert to working version
git checkout HEAD~1

# Deploy previous working version
git push origin main --force
```

---

**Last Updated:** 2026-02-27
**Status:** Ready for deployment with comprehensive troubleshooting guide
