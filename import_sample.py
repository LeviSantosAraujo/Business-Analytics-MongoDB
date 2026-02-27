"""
Import Sample Dataset to MongoDB Atlas
Import a smaller sample that fits within the 512MB free tier limit
"""

import pandas as pd
from pymongo import MongoClient
import time

def import_sample_data():
    """Import sample data that fits within free tier limits"""
    
    try:
        # Connect to MongoDB Atlas
        client = MongoClient("mongodb+srv://leviaraujo_db_user:RAfa7170*@businesscluster0.p0k3wou.mongodb.net/?appName=BusinessCluster0")
        db = client['business_data']
        collection = db['company_metrics']
        
        print("🔗 Connected to MongoDB Atlas")
        
        # Clear existing data to free up space
        print("Clearing existing data...")
        result = collection.delete_many({})
        print(f"✓ Cleared {result.deleted_count:,} existing records")
        
        # Create indexes for performance
        print("Creating indexes...")
        collection.create_index("Year")
        collection.create_index("Total_Revenue")
        collection.create_index("Total_Sales")
        collection.create_index("Record_ID")
        
        # Import smaller sample (500K records should fit in 512MB)
        print("Importing sample dataset (500K records)...")
        start_time = time.time()
        
        batch_size = 25000  # Smaller batches for Atlas
        total_imported = 0
        target_records = 500000  # Target 500K records
        
        for chunk in pd.read_csv("Raw_data.csv", chunksize=batch_size):
            if total_imported >= target_records:
                break
                
            # Convert DataFrame to documents
            documents = chunk.to_dict('records')
            
            # Adjust batch size if we're near the target
            if total_imported + len(documents) > target_records:
                documents = documents[:target_records - total_imported]
            
            # Insert batch
            result = collection.insert_many(documents)
            total_imported += len(result.inserted_ids)
            
            # Progress
            progress = (total_imported / target_records) * 100
            elapsed = time.time() - start_time
            rate = total_imported / elapsed
            
            print(f"✓ Imported {total_imported:,} records ({progress:.1f}%) - {rate:,.0f} records/sec")
        
        end_time = time.time()
        
        print("\n" + "="*60)
        print("SAMPLE IMPORT COMPLETE!")
        print("="*60)
        print(f"📊 Total Records: {total_imported:,}")
        print(f"⏱️  Import Time: {end_time - start_time:.1f} seconds")
        print(f"🗄️  Database: business_data.company_metrics")
        
        # Verify import and show statistics
        doc_count = collection.count_documents({})
        print(f"✅ Verification: {doc_count:,} documents in database")
        
        # Show database statistics
        stats = db.command("collStats", "company_metrics")
        storage_size_mb = stats['storageSize'] / (1024 * 1024)
        print(f"💾 Storage Used: {storage_size_mb:.1f} MB")
        
        # Sample queries
        print(f"\n🔍 Sample Database Queries:")
        
        # Count by year
        year_stats = list(collection.aggregate([
            {"$group": {"_id": "$Year", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]))
        print(f"   Records by year: {year_stats[:5]}")
        
        # High revenue companies
        high_revenue = collection.count_documents({"Total_Revenue": {"$gt": 100000000}})
        print(f"   Companies with >$100M revenue: {high_revenue:,}")
        
        # Average metrics
        avg_metrics = list(collection.aggregate([
            {"$group": {
                "_id": None,
                "avg_revenue": {"$avg": "$Total_Revenue"},
                "avg_sales": {"$avg": "$Total_Sales"},
                "avg_profit_margin": {"$avg": "$Profit_Margin"}
            }}
        ]))
        
        if avg_metrics:
            metrics = avg_metrics[0]
            print(f"   Average Revenue: ${metrics['avg_revenue']:,.0f}")
            print(f"   Average Sales: ${metrics['avg_sales']:,.0f}")
            print(f"   Average Profit Margin: {metrics['avg_profit_margin']:.2%}")
        
        client.close()
        
        print(f"\n🎯 Ready for querying!")
        print(f"   Run: python3 interactive_shell.py")
        print(f"   Database: business_data.company_metrics")
        print(f"   Records: {total_imported:,}")
        
        return True
        
    except Exception as e:
        print(f"❌ Import Error: {e}")
        return False

if __name__ == "__main__":
    import_sample_data()
