"""
MongoDB Bond Alert System - Main Entry Point
A production-ready database-powered financial monitoring system
"""

import os
import sys
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mongodb_bond_alert import MongoDBBondAlert

def load_config():
    """Load configuration from config.py"""
    try:
        import config
        return config
    except ImportError:
        print("⚠️  config.py not found. Please copy config.py.example to config.py")
        print("   and fill in your MongoDB connection details.")
        return None

def main():
    """Main application entry point"""
    
    print("="*70)
    print("MONGODB BOND ALERT SYSTEM")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load configuration
    config = load_config()
    if not config:
        return
    
    try:
        # Initialize MongoDB connection
        print("\n🔗 Connecting to MongoDB...")
        alert_system = MongoDBBondAlert(config.MONGODB_CONNECTION_STRING)
        alert_system.setup_indexes()
        print("✅ Connected successfully!")
        
        # Import data if Excel file exists
        excel_files = [
            "../Start Project/Lab Simple Test.xlsx",
            "Lab Simple Test.xlsx"
        ]
        
        data_imported = False
        for excel_file in excel_files:
            if os.path.exists(excel_file):
                print(f"\n📁 Importing data from {excel_file}...")
                if alert_system.import_from_excel(excel_file):
                    data_imported = True
                    break
        
        if not data_imported:
            print("\n📊 Creating sample data for demonstration...")
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
            
            print(f"✅ Created {len(sample_data)} sample records")
        
        # Check for alerts
        print(f"\n🔍 Checking for alerts (threshold: {config.ALERT_THRESHOLD * 100}%)...")
        alerts = alert_system.check_alerts(threshold=config.ALERT_THRESHOLD)
        
        if alerts:
            print(f"🔴 Found {len(alerts)} new alerts:")
            for alert in alerts:
                print(f"   - Year {alert['year']}: {alert['alert_type']} below threshold")
        else:
            print("✅ No new alerts found")
        
        # Show summary
        print("\n📊 System Summary:")
        summary = alert_system.get_alert_summary()
        for key, value in summary.items():
            print(f"   - {key.replace('_', ' ').title()}: {value}")
        
        # Show correlation analysis
        print("\n📈 Correlation Analysis:")
        correlation = alert_system.get_correlation_analysis()
        if correlation is not None:
            print(correlation.round(4))
        else:
            print("   No data available for correlation analysis")
        
        # Export data
        export_file = "bond_data_export.json"
        alert_system.export_to_json(export_file)
        
        # Show database stats
        print(f"\n💾 Database Statistics:")
        print(f"   - Total records: {alert_system.records.count_documents({})}")
        print(f"   - Total alerts: {alert_system.alerts.count_documents({})}")
        print(f"   - Database: {config.DATABASE_NAME}")
        
        # Close connection
        alert_system.close()
        print(f"\n✅ System completed successfully!")
        print(f"📁 Data exported to: {export_file}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please check your MongoDB connection and configuration.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
