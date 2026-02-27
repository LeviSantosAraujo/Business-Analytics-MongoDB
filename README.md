# Business Analytics Dashboard

A modern, interactive business analytics dashboard powered by MongoDB Atlas and Flask. This project demonstrates how to build a comprehensive analytics platform with real-time data visualization, customizable reports, and professional UI design.

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/LeviSantosAraujo/Business-Analytics-MongoDB.git
cd Business-Analytics-MongoDB
pip3 install -r requirements.txt
```

### 2. Configure MongoDB Atlas
```bash
# Copy configuration template
cp config.py.example config.py

# Edit config.py with your MongoDB Atlas details
# Get free account at: https://www.mongodb.com/cloud/atlas
```

### 3. Run the Dashboard
```bash
python3 simple_app.py
```

Then open your browser and navigate to: **http://localhost:5002**

## 📋 Project Structure

```
Business-Analytics-MongoDB/
├── simple_app.py           # Main Flask application
├── templates/
│   └── simple_index.html   # Frontend dashboard
├── config.py.example       # Configuration template
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore            # Git ignore rules
├── business_analytics.py  # Analytics functions
├── simple_analytics.py   # Simple analytics
├── mongodb_atlas_setup.py # MongoDB setup
├── query_examples.py      # Query examples
└── generate_large_dataset.py # Data generation
```

## 🎯 Features

- **� Interactive Dashboard**: Modern web-based analytics interface
- **� Multiple Report Types**: Revenue, Sales, Margin, and Trend analysis
- **�️ MongoDB Atlas**: Cloud database with realistic business data
- **🎨 Professional UI**: Clean, modern design with graphite theme
- **� Chart.js Integration**: Interactive charts with toggleable legends
- **� Detailed Data Tables**: Comprehensive data with growth calculations
- **🏠 Welcome Page**: Professional landing page with navigation
- **💫 Watermark**: Developer attribution across all pages
- **📱 Responsive Design**: Works on all screen sizes

## 🏗️ Architecture

### Frontend Components
- **Dashboard Layout**: Split-panel design with navigation and results
- **Interactive Charts**: Bar charts with year-by-year comparison
- **Data Tables**: Sortable, formatted data with growth metrics
- **Navigation**: Radio button selection with visual feedback

### Backend Components
- **Flask Application**: RESTful API endpoints
- **MongoDB Integration**: PyMongo for database operations
- **Data Generation**: Realistic sample data with fluctuations
- **Report Generation**: Dynamic report creation and formatting

### Database Design
- **Business Data**: Revenue, Sales, and Profit Margin metrics
- **Time Series**: 11 years of data (2015-2025)
- **Realistic Patterns**: Business fluctuations and trends

## 📊 Report Types

### 📈 Revenue Analysis
- Total Revenue trends over time
- Year-over-year growth calculations
- Interactive bar charts with toggleable legends

### 💰 Sales Performance
- Sales data visualization
- Growth rate analysis
- Comparative year-by-year metrics

### 📊 Profit Margins
- Margin percentage tracking
- Change analysis over time
- Visual representation of profitability

### 📈 Trend Analysis
- Multi-metric comparison
- Comprehensive data overview
- All fields in one report

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
DATABASE_NAME = "business_analytics"
COLLECTION_NAME = "business_data"
```

## 🎨 UI Features

### Navigation Panel
- **Home Option**: Welcome page with feature overview
- **Report Selection**: Radio buttons with highlighting
- **Visual Feedback**: Hover effects and selection states

### Results Panel
- **Dynamic Content**: Changes based on selection
- **Chart Visualization**: Interactive Chart.js graphs
- **Data Tables**: Detailed information with formatting
- **Professional Styling**: Consistent graphite theme

### Welcome Page
- **Feature Cards**: Clickable navigation to reports
- **Database Overview**: Data volume information
- **Getting Started**: Clear user guidance
- **Professional Design**: Modern, clean interface

## 📈 Usage Examples

### Basic Navigation
```python
# Access the dashboard
http://localhost:5002

# Select report type from left panel
# Charts and data load automatically
```

### Data Visualization
```python
# Charts show 11 years of data (2015-2025)
# Toggle years on/off with chart legends
# View detailed data tables below charts
```

### Report Generation
```python
# Revenue: Total_Revenue field analysis
# Sales: Total_Sales field analysis  
# Margin: Profit_Margin field analysis
# Trend: All fields comparison
```

## 🚀 Development

### Local Development
```bash
# Install dependencies
pip3 install -r requirements.txt

# Configure database
cp config.py.example config.py
# Edit config.py with your MongoDB Atlas details

# Run the application
python3 simple_app.py
```

### Customization
```python
# Modify data generation in generate_sample_data()
# Update chart styles in createRevenueChart()
# Change UI colors in CSS section
# Add new report types in displayResults()
```

## 📚 MongoDB Concepts Demonstrated

- **Document Storage**: Flexible JSON-like data structures
- **Aggregation Pipelines**: Complex data processing
- **Query Optimization**: Efficient data retrieval
- **Cloud Integration**: MongoDB Atlas connectivity
- **Data Modeling**: Business metrics structure

## 🔒 Security Features

- ✅ Connection strings in `config.py` (not hardcoded)
- ✅ `.gitignore` excludes sensitive files
- ✅ Environment variables support
- ✅ IP whitelisting in MongoDB Atlas

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📞 Support

- **MongoDB Docs**: https://docs.mongodb.com
- **Flask Docs**: https://flask.palletsprojects.com
- **Chart.js Docs**: https://www.chartjs.org
- **MongoDB Atlas**: https://www.mongodb.com/cloud/atlas

## 🎓 Learning Outcomes

After completing this project, you'll understand:
- MongoDB Atlas cloud database integration
- Flask web application development
- Chart.js data visualization
- Professional UI/UX design
- RESTful API development
- Business analytics implementation
- Modern web development best practices

---

**Built with ❤️ by Levi Araujo using MongoDB Atlas, Flask, and Chart.js**
