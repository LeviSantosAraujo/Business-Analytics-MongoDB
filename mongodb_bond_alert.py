"""
MongoDB Bond Alert System
A modern database-powered version of your bond monitoring system
"""

import pandas as pd
import numpy as np
from pymongo import MongoClient
from datetime import datetime, timedelta
import json
import os

class MongoDBBondAlert:
    def __init__(self, connection_string="mongodb://localhost:27017/"):
        """Initialize MongoDB connection"""
        self.client = MongoClient(connection_string)
        self.db = self.client['bond_monitoring']
        self.records = self.db['bond_records']
        self.alerts = self.db['alerts']
        
    def setup_indexes(self):
        """Create database indexes for better performance"""
        self.records.create_index("year", unique=True)
        self.records.create_index("timestamp")
        self.alerts.create_index("alert_time")
        self.alerts.create_index("year")
        
    def import_from_excel(self, file_path):
        """Import data from Excel file to MongoDB"""
        try:
            df = pd.read_excel(file_path)
            
            # Convert DataFrame to MongoDB documents
            records = []
            for idx, row in df.iterrows():
                record = {
                    'year': int(row['Year']),
                    'sp500_return': float(row['S&P 500 (includes dividends)']),
                    'baa_bond_return': self._get_baa_value(row),
                    'us_treasury_return': float(row['US T. Bond']),
                    'timestamp': datetime.now(),
                    'data_source': os.path.basename(file_path)
                }
                records.append(record)
            
            # Insert records (upsert to avoid duplicates)
            for record in records:
                self.records.update_one(
                    {'year': record['year']}, 
                    {'$set': record}, 
                    upsert=True
                )
            
            print(f"✓ Imported {len(records)} records to MongoDB")
            return True
            
        except Exception as e:
            print(f"✗ Error importing data: {str(e)}")
            return False
    
    def _get_baa_value(self, row):
        """Extract BAA bond value from row (handles different column names)"""
        for col in row.index:
            if 'Baa' in col or 'BAA' in col:
                return float(row[col])
        return 0.0
    
    def check_alerts(self, threshold=0.10):
        """Check for alerts and store them in database"""
        alert_records = []
        current_time = datetime.now()
        
        # Find records below threshold
        query = {
            '$or': [
                {'sp500_return': {'$lt': threshold}},
                {'baa_bond_return': {'$lt': threshold}}
            ]
        }
        
        records_below_threshold = list(self.records.find(query))
        
        for record in records_below_threshold:
            # Check if we already have a recent alert for this record
            recent_alert = self.alerts.find_one({
                'year': record['year'],
                'alert_time': {'$gt': current_time - timedelta(hours=1)}
            })
            
            if not recent_alert:
                # Create alert document
                alert = {
                    'year': record['year'],
                    'sp500_return': record['sp500_return'],
                    'baa_bond_return': record['baa_bond_return'],
                    'us_treasury_return': record['us_treasury_return'],
                    'threshold': threshold,
                    'alert_time': current_time,
                    'alert_type': self._get_alert_type(record, threshold),
                    'resolved': False
                }
                
                self.alerts.insert_one(alert)
                alert_records.append(alert)
        
        return alert_records
    
    def _get_alert_type(self, record, threshold):
        """Determine what triggered the alert"""
        triggers = []
        if record['sp500_return'] < threshold:
            triggers.append("S&P 500")
        if record['baa_bond_return'] < threshold:
            triggers.append("BAA Bond")
        return ", ".join(triggers)
    
    def get_alert_summary(self):
        """Get summary of all alerts"""
        total_alerts = self.alerts.count_documents({})
        unresolved_alerts = self.alerts.count_documents({'resolved': False})
        recent_alerts = self.alerts.count_documents({
            'alert_time': {'$gt': datetime.now() - timedelta(days=7)}
        })
        
        return {
            'total_alerts': total_alerts,
            'unresolved_alerts': unresolved_alerts,
            'recent_alerts': recent_alerts,
            'alert_rate': recent_alerts / 7 if recent_alerts > 0 else 0
        }
    
    def get_historical_data(self, years=None):
        """Retrieve historical bond data"""
        query = {}
        if years:
            query['year'] = {'$in': years}
        
        return list(self.records.find(query).sort('year', 1))
    
    def get_correlation_analysis(self):
        """Calculate correlation between different returns"""
        pipeline = [
            {
                '$group': {
                    '_id': None,
                    'sp500_returns': {'$push': '$sp500_return'},
                    'baa_returns': {'$push': '$baa_bond_return'},
                    'treasury_returns': {'$push': '$us_treasury_return'}
                }
            }
        ]
        
        result = list(self.records.aggregate(pipeline))
        if result:
            data = result[0]
            df = pd.DataFrame({
                'S&P 500': data['sp500_returns'],
                'BAA Bond': data['baa_returns'],
                'US Treasury': data['treasury_returns']
            })
            return df.corr()
        
        return None
    
    def export_to_json(self, output_file):
        """Export all data to JSON file"""
        data = {
            'records': list(self.records.find()),
            'alerts': list(self.alerts.find()),
            'export_time': datetime.now().isoformat()
        }
        
        # Convert ObjectId to string for JSON serialization
        for record in data['records']:
            record['_id'] = str(record['_id'])
            if 'timestamp' in record:
                record['timestamp'] = record['timestamp'].isoformat()
        
        for alert in data['alerts']:
            alert['_id'] = str(alert['_id'])
            alert['alert_time'] = alert['alert_time'].isoformat()
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Data exported to {output_file}")
    
    def close(self):
        """Close database connection"""
        self.client.close()

# Demo usage
if __name__ == "__main__":
    print("="*60)
    print("MONGODB BOND ALERT SYSTEM")
    print("="*60)
    
    # Initialize system
    alert_system = MongoDBBondAlert()
    alert_system.setup_indexes()
    
    # Import data (replace with your actual file path)
    excel_file = "../Start Project/Lab Simple Test.xlsx"
    
    if os.path.exists(excel_file):
        print(f"\n📁 Importing data from {excel_file}...")
        alert_system.import_from_excel(excel_file)
    else:
        print(f"\n⚠️  Excel file not found: {excel_file}")
        print("Creating sample data instead...")
        
        # Create sample data
        sample_data = [
            {'year': 2020, 'sp500_return': 0.18, 'baa_bond_return': 0.08, 'us_treasury_return': 0.04},
            {'year': 2021, 'sp500_return': 0.28, 'baa_bond_return': 0.06, 'us_treasury_return': 0.03},
            {'year': 2022, 'sp500_return': -0.18, 'baa_bond_return': -0.08, 'us_treasury_return': 0.02},
            {'year': 2023, 'sp500_return': 0.26, 'baa_bond_return': 0.05, 'us_treasury_return': 0.04},
        ]
        
        for data in sample_data:
            alert_system.records.update_one(
                {'year': data['year']},
                {'$set': {**data, 'timestamp': datetime.now(), 'data_source': 'sample'}},
                upsert=True
            )
        
        print(f"✓ Created {len(sample_data)} sample records")
    
    # Check for alerts
    print("\n🔍 Checking for alerts...")
    alerts = alert_system.check_alerts(threshold=0.10)
    
    if alerts:
        print(f"🔴 Found {len(alerts)} new alerts:")
        for alert in alerts:
            print(f"   - Year {alert['year']}: {alert['alert_type']} below threshold")
    else:
        print("✓ No new alerts found")
    
    # Show summary
    print("\n📊 Alert Summary:")
    summary = alert_system.get_alert_summary()
    for key, value in summary.items():
        print(f"   - {key.replace('_', ' ').title()}: {value}")
    
    # Show correlation analysis
    print("\n📈 Correlation Analysis:")
    correlation = alert_system.get_correlation_analysis()
    if correlation is not None:
        print(correlation.round(4))
    
    # Export data
    alert_system.export_to_json("bond_data_export.json")
    
    # Close connection
    alert_system.close()
    print("\n✓ System shutdown complete")
