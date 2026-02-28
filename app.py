"""
Vercel Python Template for Business Analytics Dashboard
"""
from flask import Flask, jsonify, send_from_directory, request
from pymongo import MongoClient
import json
from datetime import datetime
import os

app = Flask(__name__)

# Sample data for demo purposes
SAMPLE_FIELDS = [
    {"value": "Total_Revenue", "label": "Total Revenue", "type": "number"},
    {"value": "Total_Sales", "label": "Total Sales", "type": "number"},
    {"value": "Profit_Margin", "label": "Profit Margin", "type": "percentage"}
]

SAMPLE_YEARS = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]

@app.route('/')
def index():
    """Main dashboard page"""
    return send_from_directory('templates', 'simple_index.html')

@app.route('/api/years')
def get_years():
    """Get available years"""
    return jsonify({"success": True, "years": SAMPLE_YEARS})

@app.route('/api/fields')
def get_fields():
    """Get available fields"""
    return jsonify({"success": True, "fields": SAMPLE_FIELDS})

@app.route('/api/generate_report', methods=['POST'])
def generate_report():
    """Generate report endpoint"""
    try:
        data = request.json
        report_type = data.get('report_type', 'summary')
        fields = data.get('fields', [])
        years = data.get('years', [])
        
        # Handle different report types
        if report_type in ['revenue', 'sales', 'margin']:
            # Map new report types to summary with specific field
            if report_type == 'revenue':
                fields = ['Total_Revenue']
            elif report_type == 'sales':
                fields = ['Total_Sales']
            elif report_type == 'margin':
                fields = ['Profit_Margin']
            report_type = 'summary'
        elif report_type == 'trend':
            # Use all fields for trend
            fields = ['Total_Revenue', 'Total_Sales', 'Profit_Margin']
        
        # Generate sample data (no MongoDB connection needed)
        sample_data = []
        for i, year in enumerate(SAMPLE_YEARS):
            revenue = 50000000 + (i * 5000000) + (i * 2500000 * (i % 2))
            sales = 40000000 + (i * 4000000) + (i * 2000000 * (i % 2))
            margin = 0.15 + (i * 0.02) - (i * 0.01 * (i % 2))
            
            sample_data.append({
                "_id": int(year),
                "Total_Revenue": revenue,
                "Total_Sales": sales,
                "Profit_Margin": margin
            })
        
        return jsonify({
            "success": True,
            "type": report_type,
            "fields": fields,
            "years": years,
            "data": sample_data,
            "raw_data": sample_data
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "data": [],
            "raw_data": []
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
