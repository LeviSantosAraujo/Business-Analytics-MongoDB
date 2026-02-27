"""
Interactive Business Analytics Dashboard
Flask web application for generating custom reports from MongoDB
"""

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import json
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

# MongoDB connection
def get_mongodb_connection():
    """Get MongoDB connection"""
    try:
        import config
        client = MongoClient(config.MONGODB_CONNECTION_STRING)
        db = client['business_data']
        return db['company_metrics']
    except:
        # Fallback connection
        client = MongoClient("mongodb+srv://leviaraujo_db_user:RAfa7170*@businesscluster0.p0k3wou.mongodb.net/?appName=BusinessCluster0")
        db = client['business_data']
        return db['company_metrics']

class ReportGenerator:
    """Generate various types of business reports"""
    
    def __init__(self, collection):
        self.collection = collection
    
    def get_available_years(self):
        """Get available years in the dataset"""
        years = list(self.collection.aggregate([
            {"$group": {"_id": "$Year"}},
            {"$sort": {"_id": 1}}
        ]))
        return [str(year['_id']) for year in years]
    
    def get_available_fields(self):
        """Get available fields for selection"""
        return [
            {"value": "Total_Revenue", "label": "Total Revenue", "type": "currency"},
            {"value": "Total_Sales", "label": "Total Sales", "type": "currency"},
            {"value": "Year", "label": "Year", "type": "number"},
            {"value": "Profit_Margin", "label": "Profit Margin", "type": "percentage"},
            {"value": "Revenue_Growth", "label": "Revenue Growth", "type": "percentage"},
            {"value": "Market_Cap", "label": "Market Cap", "type": "currency"},
            {"value": "Record_ID", "label": "Record ID", "type": "number"}
        ]
    
    def generate_summary_report(self, fields, years, filters):
        """Generate summary statistics report"""
        match_stage = {}
        if years:
            match_stage["Year"] = {"$in": [int(year) for year in years]}
        
        # Build projection stage
        projection_stage = {field: 1 for field in fields}
        projection_stage["_id"] = 0
        
        # Generate summary statistics
        pipeline = []
        if match_stage:
            pipeline.append({"$match": match_stage})
        pipeline.append({"$project": projection_stage})
        
        # Calculate statistics for each field
        results = {}
        for field in fields:
            if field in ["Total_Revenue", "Total_Sales", "Market_Cap"]:
                # Currency fields
                stats = list(self.collection.aggregate(pipeline + [
                    {"$group": {
                        "_id": None,
                        "min": {"$min": f"${field}"},
                        "max": {"$max": f"${field}"},
                        "avg": {"$avg": f"${field}"},
                        "sum": {"$sum": f"${field}"},
                        "count": {"$sum": 1}
                    }}
                ]))
            elif field in ["Profit_Margin", "Revenue_Growth"]:
                # Percentage fields
                stats = list(self.collection.aggregate(pipeline + [
                    {"$group": {
                        "_id": None,
                        "min": {"$min": f"${field}"},
                        "max": {"$max": f"${field}"},
                        "avg": {"$avg": f"${field}"},
                        "count": {"$sum": 1}
                    }}
                ]))
            else:
                # Number fields
                stats = list(self.collection.aggregate(pipeline + [
                    {"$group": {
                        "_id": None,
                        "min": {"$min": f"${field}"},
                        "max": {"$max": f"${field}"},
                        "avg": {"$avg": f"${field}"},
                        "count": {"$sum": 1}
                    }}
                ]))
            
            if stats:
                results[field] = stats[0]
        
        return {
            "type": "summary",
            "fields": fields,
            "years": years,
            "data": results,
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_trend_report(self, fields, years, filters):
        """Generate trend analysis report"""
        match_stage = {}
        if years:
            match_stage["Year"] = {"$in": [int(year) for year in years]}
        
        # Build projection stage
        projection_stage = {"Year": 1}
        for field in fields:
            projection_stage[field] = 1
        projection_stage["_id"] = 0
        
        # Generate trend data by year
        pipeline = []
        if match_stage:
            pipeline.append({"$match": match_stage})
        pipeline.append({"$project": projection_stage})
        
        trend_data = list(self.collection.aggregate(pipeline + [
            {"$group": {
                "_id": "$Year",
                **{field: {"$avg": f"${field}"} for field in fields if field != "Year"}
            }},
            {"$sort": {"_id": 1}}
        ]))
        
        return {
            "type": "trend",
            "fields": fields,
            "years": years,
            "data": trend_data,
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_comparison_report(self, fields, years, filters):
        """Generate comparison report"""
        match_stage = {}
        if years:
            match_stage["Year"] = {"$in": [int(year) for year in years]}
        
        # Build projection stage
        projection_stage = {"Year": 1}
        for field in fields:
            projection_stage[field] = 1
        projection_stage["_id"] = 0
        
        # Get top and bottom performers
        pipeline = []
        if match_stage:
            pipeline.append({"$match": match_stage})
        pipeline.append({"$project": projection_stage})
        
        # Top performers
        top_performers = list(self.collection.aggregate(pipeline + [
            {"$sort": {fields[0]: -1 if fields[0] in ["Total_Revenue", "Total_Sales", "Market_Cap"] else 1}},
            {"$limit": 10}
        ]))
        
        # Bottom performers
        bottom_performers = list(self.collection.aggregate(pipeline + [
            {"$sort": {fields[0]: 1 if fields[0] in ["Total_Revenue", "Total_Sales", "Market_Cap"] else -1}},
            {"$limit": 10}
        ]))
        
        return {
            "type": "comparison",
            "fields": fields,
            "years": years,
            "data": {
                "top_performers": top_performers,
                "bottom_performers": bottom_performers
            },
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_distribution_report(self, fields, years, filters):
        """Generate distribution report"""
        match_stage = {}
        if years:
            match_stage["Year"] = {"$in": [int(year) for year in years]}
        
        distribution_data = {}
        
        for field in fields:
            pipeline = []
            if match_stage:
                pipeline.append({"$match": match_stage})
            
            # Create distribution buckets based on field type
            if field in ["Total_Revenue", "Total_Sales", "Market_Cap"]:
                # Currency fields - create ranges
                pipeline.extend([
                    {"$bucket": {
                        "groupBy": f"${field}",
                        "boundaries": [0, 10000000, 100000000, 1000000000, 5000000000],
                        "default": "Other",
                        "output": {
                            "count": {"$sum": 1},
                            "avg": {"$avg": f"${field}"}
                        }
                    }}
                ])
            elif field in ["Profit_Margin", "Revenue_Growth"]:
                # Percentage fields - create percentage ranges
                pipeline.extend([
                    {"$bucket": {
                        "groupBy": f"${field}",
                        "boundaries": [-1, -0.2, 0, 0.1, 0.2, 0.5, 1],
                        "default": "Other",
                        "output": {
                            "count": {"$sum": 1},
                            "avg": {"$avg": f"${field}"}
                        }
                    }}
                ])
            else:
                # Number fields - create ranges
                pipeline.extend([
                    {"$bucket": {
                        "groupBy": f"${field}",
                        "boundaries": [0, 1000, 5000, 10000, 50000],
                        "default": "Other",
                        "output": {
                            "count": {"$sum": 1},
                            "avg": {"$avg": f"${field}"}
                        }
                    }}
                ])
            
            distribution = list(self.collection.aggregate(pipeline))
            distribution_data[field] = distribution
        
        return {
            "type": "distribution",
            "fields": fields,
            "years": years,
            "data": distribution_data,
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_chat_insights(self, fields, years, question):
        """Generate AI-like insights based on data"""
        match_stage = {}
        if years:
            match_stage["Year"] = {"$in": [int(year) for year in years]}
        
        # Build projection stage
        projection_stage = {"Year": 1}
        for field in fields:
            projection_stage[field] = 1
        projection_stage["_id"] = 0
        
        pipeline = []
        if match_stage:
            pipeline.append({"$match": match_stage})
        pipeline.append({"$project": projection_stage})
        
        # Get sample data for insights
        sample_data = list(self.collection.aggregate(pipeline + [{"$limit": 1000}]))
        
        # Generate insights based on available data and question
        insights = []
        
        if "revenue" in question.lower() and "Total_Revenue" in fields:
            if sample_data:
                avg_revenue = sum(d.get("Total_Revenue", 0) for d in sample_data) / len(sample_data)
                insights.append(f"The average revenue across selected years is ${avg_revenue:,.0f}")
                
                # Year over year trend
                revenue_by_year = {}
                for d in sample_data:
                    year = d.get("Year")
                    if year:
                        if year not in revenue_by_year:
                            revenue_by_year[year] = []
                        revenue_by_year[year].append(d.get("Total_Revenue", 0))
                
                if len(revenue_by_year) > 1:
                    years_sorted = sorted(revenue_by_year.keys())
                    avg_by_year = [sum(revenue_by_year[y]) / len(revenue_by_year[y]) for y in years_sorted]
                    if len(avg_by_year) > 1:
                        growth = (avg_by_year[-1] - avg_by_year[0]) / avg_by_year[0] * 100
                        insights.append(f"Revenue shows a {growth:.1f}% growth trend from {years_sorted[0]} to {years_sorted[-1]}")
        
        if "profit" in question.lower() and "Profit_Margin" in fields:
            if sample_data:
                avg_margin = sum(d.get("Profit_Margin", 0) for d in sample_data) / len(sample_data)
                insights.append(f"The average profit margin is {avg_margin:.2%}")
                
                high_profit = sum(1 for d in sample_data if d.get("Profit_Margin", 0) > 0.8)
                insights.append(f"{high_profit} out of {len(sample_data)} companies have profit margins above 80%")
        
        if "growth" in question.lower() and "Revenue_Growth" in fields:
            if sample_data:
                avg_growth = sum(d.get("Revenue_Growth", 0) for d in sample_data) / len(sample_data)
                insights.append(f"The average revenue growth is {avg_growth:.2%}")
                
                positive_growth = sum(1 for d in sample_data if d.get("Revenue_Growth", 0) > 0)
                insights.append(f"{positive_growth} out of {len(sample_data)} companies show positive growth")
        
        # General insights
        insights.append(f"Analysis based on {len(sample_data)} records from {', '.join(years) if years else 'all years'}")
        insights.append(f"Selected fields: {', '.join(fields)}")
        
        return {
            "type": "chat",
            "question": question,
            "fields": fields,
            "years": years,
            "insights": insights,
            "sample_count": len(sample_data),
            "generated_at": datetime.now().isoformat()
        }

# Initialize report generator
report_generator = ReportGenerator(get_mongodb_connection())

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/years')
def get_years():
    """Get available years"""
    try:
        years = report_generator.get_available_years()
        return jsonify({"success": True, "years": years})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/fields')
def get_fields():
    """Get available fields"""
    try:
        fields = report_generator.get_available_fields()
        return jsonify({"success": True, "fields": fields})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/generate_report', methods=['POST'])
def generate_report():
    """Generate report based on user selection"""
    try:
        data = request.json
        report_type = data.get('report_type')
        fields = data.get('fields', [])
        years = data.get('years', [])
        question = data.get('question', '')
        
        if not fields:
            return jsonify({"success": False, "error": "Please select at least one field"})
        
        # Generate report based on type
        if report_type == 'summary':
            result = report_generator.generate_summary_report(fields, years, {})
        elif report_type == 'trend':
            result = report_generator.generate_trend_report(fields, years, {})
        elif report_type == 'comparison':
            result = report_generator.generate_comparison_report(fields, years, {})
        elif report_type == 'distribution':
            result = report_generator.generate_distribution_report(fields, years, {})
        elif report_type == 'chat':
            result = report_generator.generate_chat_insights(fields, years, question)
        else:
            return jsonify({"success": False, "error": "Invalid report type"})
        
        return jsonify({"success": True, "result": result})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/sample_data')
def get_sample_data():
    """Get sample data for preview"""
    try:
        sample = list(report_generator.collection.find({}, {"_id": 0}).limit(5))
        return jsonify({"success": True, "data": sample})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    print("🚀 Starting Business Analytics Dashboard...")
    print("📊 Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
