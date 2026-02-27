# MongoDB Bond Alert System

A modern, database-powered financial monitoring system using MongoDB. This project demonstrates how to build a production-ready alert system that replaces Excel-based monitoring with a scalable database solution.

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd mongodb-bond-alert
pip3 install -r requirements.txt
```

### 2. Configure MongoDB
```bash
# Copy configuration template
cp config.py.example config.py

# Edit config.py with your MongoDB Atlas details
# Get free account at: https://www.mongodb.com/cloud/atlas
```

### 3. Run the System
```bash
python3 main.py
```

## 📋 Project Structure

```
mongodb-bond-alert/
├── main.py                 # Main application entry point
├── mongodb_bond_alert.py   # Core MongoDB functionality
├── config.py.example       # Configuration template
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore            # Git ignore rules
└── data/                 # Data exports (auto-created)
```

## 🎯 Features

- **🗄️ MongoDB Storage**: Replace Excel files with robust database
- **🚨 Real-time Alerts**: Automatic threshold monitoring
- **📊 Data Analysis**: Built-in correlation and statistics
- **🔍 Historical Tracking**: Complete alert history
- **📤 Export Options**: JSON data export functionality
- **⚡ High Performance**: Optimized database queries
- **🌐 Cloud Ready**: MongoDB Atlas integration

## 🏗️ Architecture

### Database Design
- **`bond_records`**: Historical financial data
- **`alerts`**: Alert history and tracking
- **Indexes**: Optimized for performance

### Key Components
- **MongoDBBondAlert**: Core database operations
- **Alert Engine**: Threshold monitoring logic
- **Data Import**: Excel to MongoDB migration
- **Analytics**: Correlation and statistical analysis

## 📊 MongoDB vs Excel

| Feature | Excel | MongoDB |
|---------|-------|---------|
| **Scalability** | Limited | Unlimited |
| **Concurrent Access** | No | Yes |
| **Query Performance** | Slow | Instant |
| **Data Integrity** | Manual | Automatic |
| **Backup/Recovery** | Manual | Built-in |
| **Alert History** | No | Complete |

## 🔧 Configuration

### MongoDB Atlas Setup (Free)
1. **Create Account**: https://www.mongodb.com/cloud/atlas
2. **Create Cluster**: Shared (FREE) - 512MB
3. **Add User**: Database Access → Add User
4. **Whitelist IP**: Network Access → Allow Anywhere
5. **Get Connection**: Database → Connect → Python

### Environment Variables
```python
# config.py
MONGODB_CONNECTION_STRING = "mongodb+srv://user:pass@cluster.mongodb.net"
ALERT_THRESHOLD = 0.10  # 10%
```

## � Query Examples

### Interactive Shell
```bash
python3 interactive_shell.py
```

### Query Examples
```python
# Basic queries
records.find({'year': 2022})                    # Specific year
records.find({'sp500_return': {'$gt': 0.20}})   # S&P > 20%
records.count()                                 # Count all records

# Advanced queries
records.find({
    '$or': [
        {'sp500_return': {'$gt': 0.25}},
        {'baa_bond_return': {'$gt': 0.10}}
    ]
})  # OR query

# Aggregation
records.aggregate([
    {'$group': {'_id': None, 'avg_sp500': {'$avg': '$sp500_return'}}}
])
```

### Query Capabilities
- **Basic Queries**: Find, count, distinct
- **Comparison Operators**: `$gt`, `$lt`, `$gte`, `$lte`, `$ne`
- **Logical Operators**: `$and`, `$or`, `$nor`, `$not`
- **Range Queries**: Find data within ranges
- **Text Search**: Pattern matching and regex
- **Aggregation Pipelines**: Complex data analysis
- **Performance Queries**: Indexed and optimized queries

## �📈 Usage Examples

### Basic Monitoring
```python
from mongodb_bond_alert import MongoDBBondAlert

# Initialize
alert_system = MongoDBBondAlert(connection_string)

# Check alerts
alerts = alert_system.check_alerts(threshold=0.10)

# Get statistics
summary = alert_system.get_alert_summary()
```

### Data Analysis
```python
# Historical data
data = alert_system.get_historical_data(years=[2020, 2021, 2022])

# Correlation analysis
correlation = alert_system.get_correlation_analysis()
```

## 🚀 Deployment

### Local Development
```bash
python3 main.py
```

### Production
```bash
# Set up environment variables
export MONGODB_CONNECTION_STRING="your-connection-string"
export ALERT_THRESHOLD=0.10

# Run with monitoring
python3 main.py
```

## 📚 MongoDB Concepts Learned

- **Collections**: Flexible schema containers
- **Documents**: JSON-like data structures
- **Indexes**: Performance optimization
- **Aggregation**: Advanced data processing
- **Queries**: Powerful filtering capabilities

## 🔒 Security Best Practices

- ✅ Connection strings in `config.py` (not hardcoded)
- ✅ `.gitignore` excludes sensitive files
- ✅ Environment variables for production
- ✅ IP whitelisting in MongoDB Atlas

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📞 Support

- **MongoDB Docs**: https://docs.mongodb.com
- **PyMongo Docs**: https://pymongo.readthedocs.io
- **MongoDB Atlas**: https://www.mongodb.com/cloud/atlas

## 🎓 Learning Outcomes

After completing this project, you'll understand:
- MongoDB database design and operations
- Python database integration with PyMongo
- Financial data modeling and analysis
- Alert system architecture
- Cloud database deployment
- Production-ready code organization

---

**Built with ❤️ using MongoDB and Python**
