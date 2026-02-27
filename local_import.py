"""
Local MongoDB Import
Import data to local MongoDB instance for testing
"""

import pandas as pd
from pymongo import MongoClient
import time

def import_to_local_mongodb():
    """Import CSV to local MongoDB instance"""
    
    try:
        # Connect to local MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['business_data']
        collection = db['company_metrics']
        
        print("🔗 Connected to local MongoDB")
        
        # Create indexes for performance
        print("Creating indexes...")
        collection.create_index("Year")
        collection.create_index("Total_Revenue")
        collection.create_index("Total_Sales")
        collection.create_index("Record_ID")
        
        # Clear existing data
        collection.delete_many({})
        print("Cleared existing data")
        
        # Read and import data in smaller batches
        print("Starting import...")
        start_time = time.time()
        
        batch_size = 10000  # Smaller batches for local testing
        total_imported = 0
        
        for chunk in pd.read_csv("Raw_data.csv", chunksize=batch_size):
            # Convert DataFrame to documents
            documents = chunk.to_dict('records')
            
            # Insert batch
            result = collection.insert_many(documents)
            total_imported += len(result.inserted_ids)
            
            # Progress
            progress = (total_imported / 3000000) * 100
            elapsed = time.time() - start_time
            rate = total_imported / elapsed
            
            print(f"✓ Imported {total_imported:,} records ({progress:.1f}%) - {rate:,.0f} records/sec")
            
            # Stop after 100K for testing (remove this for full import)
            if total_imported >= 100000:
                print("📊 Stopping at 100K records for testing")
                break
        
        end_time = time.time()
        
        print("\n" + "="*60)
        print("IMPORT COMPLETE!")
        print("="*60)
        print(f"📊 Total Records: {total_imported:,}")
        print(f"⏱️  Import Time: {end_time - start_time:.1f} seconds")
        print(f"🗄️  Database: business_data.company_metrics")
        
        # Verify import
        doc_count = collection.count_documents({})
        print(f"✅ Verification: {doc_count:,} documents in database")
        
        # Show sample queries
        print(f"\n🔍 Sample Queries:")
        
        # Count by year
        year_stats = list(collection.aggregate([
            {"$group": {"_id": "$Year", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]))
        print(f"   Records by year: {year_stats[:5]}")
        
        # High revenue companies
        high_revenue = collection.count_documents({"Total_Revenue": {"$gt": 100000000}})
        print(f"   Companies with >$100M revenue: {high_revenue:,}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Import Error: {e}")
        print("\n💡 Solutions:")
        print("   1. Install MongoDB: brew install mongodb-community")
        print("   2. Start MongoDB: brew services start mongodb-community")
        print("   3. Use MongoDB Atlas (cloud) instead")
        return False

if __name__ == "__main__":
    import_to_local_mongodb()
