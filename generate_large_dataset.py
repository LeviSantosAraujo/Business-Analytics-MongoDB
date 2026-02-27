"""
Generate Large Business Dataset
Creates 3 million records for MongoDB testing and performance analysis
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime
import time
import os

class LargeDatasetGenerator:
    """Generate large business dataset for MongoDB testing"""
    
    def __init__(self, num_records=3_000_000):
        self.num_records = num_records
        self.years = list(range(2015, 2026))  # 2015 to 2025
        self.output_file = "Raw_data.csv"
        
        # Business parameters for realistic data generation
        self.revenue_params = {
            'min': 1_000_000,      # $1M minimum revenue
            'max': 500_000_000,    # $500M maximum revenue
            'growth_rate': 0.08    # 8% average annual growth
        }
        
        self.sales_params = {
            'min_ratio': 0.6,       # Sales are 60-90% of revenue
            'max_ratio': 0.9
        }
    
    def generate_batch(self, batch_size=100_000, start_idx=0):
        """Generate a batch of records to manage memory usage"""
        
        print(f"Generating batch {start_idx//batch_size + 1} ({batch_size:,} records)...")
        
        # Generate years with some distribution (more recent years have more data)
        year_weights = np.array([0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15])
        year_weights = year_weights / year_weights.sum()  # Normalize to sum to 1
        years = np.random.choice(self.years, size=batch_size, p=year_weights)
        
        # Generate revenue with year-based growth
        revenues = []
        for year in years:
            year_factor = (year - 2014) * self.revenue_params['growth_rate']
            base_revenue = np.random.uniform(
                self.revenue_params['min'] * (1 + year_factor),
                self.revenue_params['max'] * (1 + year_factor)
            )
            revenues.append(base_revenue)
        
        # Generate sales as percentage of revenue
        sales_ratios = np.random.uniform(
            self.sales_params['min_ratio'],
            self.sales_params['max_ratio'],
            size=batch_size
        )
        sales = [rev * ratio for rev, ratio in zip(revenues, sales_ratios)]
        
        # Add some business variability
        # Some companies have seasonal patterns
        seasonal_factor = np.random.uniform(0.8, 1.2, size=batch_size)
        revenues = [rev * factor for rev, factor in zip(revenues, seasonal_factor)]
        sales = [sale * factor for sale, factor in zip(sales, seasonal_factor)]
        
        # Create DataFrame
        batch_data = pd.DataFrame({
            'Total_Revenue': revenues,
            'Total_Sales': sales,
            'Year': years,
            'Record_ID': range(start_idx, start_idx + batch_size)
        })
        
        # Add some business metrics for additional analysis
        batch_data['Profit_Margin'] = batch_data['Total_Sales'] / batch_data['Total_Revenue']
        batch_data['Revenue_Growth'] = np.random.uniform(-0.2, 0.3, size=batch_size)  # -20% to +30% growth
        batch_data['Market_Cap'] = batch_data['Total_Revenue'] * np.random.uniform(2, 8, size=batch_size)  # 2-8x revenue
        
        return batch_data
    
    def generate_full_dataset(self):
        """Generate the complete 3 million record dataset"""
        
        print("="*60)
        print("GENERATING LARGE BUSINESS DATASET")
        print("="*60)
        print(f"Target Records: {self.num_records:,}")
        print(f"Output File: {self.output_file}")
        print(f"Years: {min(self.years)} - {max(self.years)}")
        print("="*60)
        
        start_time = time.time()
        batch_size = 100_000  # Process in batches to manage memory
        total_batches = self.num_records // batch_size
        
        # Initialize CSV file with header
        first_batch = self.generate_batch(batch_size, 0)
        first_batch.to_csv(self.output_file, index=False)
        print(f"✓ Initial batch written to {self.output_file}")
        
        # Generate remaining batches
        for batch_num in range(1, total_batches):
            start_idx = batch_num * batch_size
            
            # Generate batch
            batch = self.generate_batch(batch_size, start_idx)
            
            # Append to CSV (without header)
            batch.to_csv(self.output_file, mode='a', header=False, index=False)
            
            # Progress update
            progress = (batch_num + 1) / total_batches * 100
            elapsed = time.time() - start_time
            records_per_sec = (batch_num + 1) * batch_size / elapsed
            eta = (total_batches - batch_num - 1) * batch_size / records_per_sec
            
            print(f"✓ Batch {batch_num + 1}/{total_batches} complete ({progress:.1f}%)")
            print(f"  Speed: {records_per_sec:,.0f} records/sec")
            print(f"  ETA: {eta/60:.1f} minutes")
        
        # Handle remaining records if not divisible by batch_size
        remaining = self.num_records % batch_size
        if remaining > 0:
            start_idx = total_batches * batch_size
            final_batch = self.generate_batch(remaining, start_idx)
            final_batch.to_csv(self.output_file, mode='a', header=False, index=False)
            print(f"✓ Final batch ({remaining:,} records) written")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # File statistics
        file_size = os.path.getsize(self.output_file) / (1024 * 1024 * 1024)  # GB
        
        print("="*60)
        print("DATASET GENERATION COMPLETE!")
        print("="*60)
        print(f"📊 Total Records: {self.num_records:,}")
        print(f"📁 File Size: {file_size:.2f} GB")
        print(f"⏱️  Generation Time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
        print(f"🚀 Average Speed: {self.num_records/total_time:,.0f} records/sec")
        print(f"💾 Output File: {self.output_file}")
        
        # Show sample statistics
        self.show_dataset_statistics()
        
        return self.output_file
    
    def show_dataset_statistics(self):
        """Display statistics about the generated dataset"""
        
        print("\n📈 DATASET STATISTICS:")
        print("-" * 40)
        
        # Read a sample to calculate statistics
        sample_size = min(100_000, self.num_records)
        sample_df = pd.read_csv(self.output_file, nrows=sample_size)
        
        print(f"Sample Size: {sample_size:,} records")
        print(f"Year Range: {sample_df['Year'].min()} - {sample_df['Year'].max()}")
        print(f"Revenue Range: ${sample_df['Total_Revenue'].min():,.0f} - ${sample_df['Total_Revenue'].max():,.0f}")
        print(f"Sales Range: ${sample_df['Total_Sales'].min():,.0f} - ${sample_df['Total_Sales'].max():,.0f}")
        print(f"Average Revenue: ${sample_df['Total_Revenue'].mean():,.0f}")
        print(f"Average Sales: ${sample_df['Total_Sales'].mean():,.0f}")
        
        # Year distribution
        year_dist = sample_df['Year'].value_counts().sort_index()
        print(f"\nYear Distribution:")
        for year, count in year_dist.items():
            percentage = count / sample_size * 100
            print(f"  {year}: {count:,} records ({percentage:.1f}%)")
    
    def create_mongodb_import_script(self):
        """Create a script to import the CSV into MongoDB"""
        
        script_content = '''
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
        
        print("\\n" + "="*60)
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
'''
        
        with open('import_to_mongodb.py', 'w') as f:
            f.write(script_content)
        
        print("✅ Created 'import_to_mongodb.py' for database import")

if __name__ == "__main__":
    # Create dataset generator
    generator = LargeDatasetGenerator(3_000_000)
    
    # Generate the dataset
    output_file = generator.generate_full_dataset()
    
    # Create MongoDB import script
    generator.create_mongodb_import_script()
    
    print(f"\n🎯 Next Steps:")
    print(f"1. Review the generated CSV: {output_file}")
    print(f"2. Import to MongoDB: python3 import_to_mongodb.py")
    print(f"3. Test queries with the large dataset")
