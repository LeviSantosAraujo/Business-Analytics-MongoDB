
"""
Import Large CSV Dataset into MongoDB
Efficiently import the 3M record dataset
"""

import pandas as pd
from pymongo import MongoClient
import sys
import time

def import_large_csv(csv_file, connection_string, batch_size=50000):
    """Import large CSV file into MongoDB in batches"""
    
    try:
        # Connect to MongoDB
        client = MongoClient(connection_string)
        db = client['business_data']
        collection = db['company_metrics']
        
        # Create indexes for performance
        print("Creating indexes...")
        collection.create_index("Year")
        collection.create_index("Total_Revenue")
        collection.create_index("Total_Sales")
        collection.create_index("Record_ID")
        
        # Read CSV in chunks and import
        print(f"Importing {csv_file} to MongoDB...")
        start_time = time.time()
        
        total_imported = 0
        for chunk in pd.read_csv(csv_file, chunksize=batch_size):
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
        
        client.close()
        
    except Exception as e:
        print(f"❌ Import Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    # Load configuration
    try:
        import config
        connection_string = config.MONGODB_CONNECTION_STRING
    except ImportError:
        print("⚠️  config.py not found. Using default connection string.")
        connection_string = "mongodb://localhost:27017/"
    
    # Import the dataset
    import_large_csv("Raw_data.csv", connection_string)
