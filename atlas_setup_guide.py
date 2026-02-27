"""
MongoDB Atlas Quick Setup Guide
Get your free cloud database running in 5 minutes
"""

import webbrowser
from datetime import datetime

def print_atlas_setup():
    """Print step-by-step Atlas setup instructions"""
    
    print("="*80)
    print("MONGODB ATLAS SETUP - 5 MINUTES TO FREE DATABASE")
    print("="*80)
    
    print("\n🚀 STEP 1: Create Free Account (2 minutes)")
    print("1. Go to: https://www.mongodb.com/cloud/atlas")
    print("2. Click 'Try Free' (no credit card required)")
    print("3. Sign up with Google/GitHub or email")
    print("4. Verify your email")
    
    print("\n🏗️  STEP 2: Create Free Cluster (1 minute)")
    print("1. Click 'Create Cluster'")
    print("2. Select 'Shared Cluster' (FREE - 512MB)")
    print("3. Cloud Provider: AWS")
    print("4. Region: Choose closest to you (e.g., us-east-1)")
    print("5. Cluster Name: BusinessData")
    print("6. Click 'Create Cluster'")
    print("7. Wait 2-3 minutes for cluster to be ready")
    
    print("\n🔐 STEP 3: Create Database User (30 seconds)")
    print("1. Go to 'Database Access' (left menu)")
    print("2. Click 'Add New Database User'")
    print("3. Username: businessuser")
    print("4. Password: Create strong password (save it!)")
    print("5. Permissions: 'Read and write to any database'")
    print("6. Click 'Add User'")
    
    print("\n🌐 STEP 4: Allow Connections (30 seconds)")
    print("1. Go to 'Network Access' (left menu)")
    print("2. Click 'Add IP Address'")
    print("3. Select 'Allow Access from Anywhere' (0.0.0.0/0)")
    print("4. Click 'Confirm'")
    
    print("\n🔗 STEP 5: Get Connection String (30 seconds)")
    print("1. Go to 'Database' (left menu)")
    print("2. Click 'Connect' on your cluster")
    print("3. Select 'Connect your application'")
    print("4. Driver: Python")
    print("5. Version: 3.9 or later")
    print("6. Copy the connection string")
    print("7. Replace <password> with your actual password")
    
    print("\n⚙️  STEP 6: Update Configuration")
    print("1. Edit config.py")
    print("2. Replace MONGODB_CONNECTION_STRING with your connection string")
    print("3. Save the file")
    
    print("\n🚀 STEP 7: Import Your Data")
    print("Run: python3 import_to_mongodb.py")
    
    print("\n" + "="*80)
    print("🎯 YOUR FREE ATLAS BENEFITS:")
    print("• 512MB storage (your 300MB dataset fits perfectly!)")
    print("• Unlimited collections and documents")
    print("• Full MongoDB features and indexes")
    print("• 24/7 monitoring and automatic backups")
    print("• Global CDN for fast access from anywhere")
    print("• No server management required")
    print("="*80)
    
    print("\n💡 CONNECTION STRING FORMAT:")
    print("mongodb+srv://businessuser:YOUR_PASSWORD@businessdata.xxxxx.mongodb.net/?retryWrites=true&w=majority")
    
    print("\n🔥 READY TO START?")
    print("1. Open: https://www.mongodb.com/cloud/atlas")
    print("2. Follow the steps above")
    print("3. Come back when you have your connection string")

def create_config_updater():
    """Create a script to help update config"""
    
    config_helper = '''
"""
Config Helper - Update your MongoDB connection string
"""

def update_config():
    """Interactive config update"""
    
    print("🔧 MongoDB Atlas Configuration Updater")
    print("="*50)
    
    # Get connection string from user
    connection_string = input("\\nEnter your MongoDB Atlas connection string: ").strip()
    
    if not connection_string:
        print("❌ No connection string provided")
        return False
    
    # Validate connection string format
    if not connection_string.startswith("mongodb+srv://"):
        print("⚠️  Warning: Connection string should start with 'mongodb+srv://'")
    
    # Update config file
    try:
        with open('config.py', 'r') as f:
            content = f.read()
        
        # Replace the connection string
        new_content = content.replace(
            'MONGODB_CONNECTION_STRING = "mongodb+srv://bonduser:YOUR_PASSWORD@cluster.mongodb.net/?retryWrites=true&w=majority"',
            f'MONGODB_CONNECTION_STRING = "{connection_string}"'
        )
        
        with open('config.py', 'w') as f:
            f.write(new_content)
        
        print("✅ Config updated successfully!")
        print("📁 File: config.py")
        print("🚀 Ready to import: python3 import_to_mongodb.py")
        return True
        
    except Exception as e:
        print(f"❌ Error updating config: {e}")
        return False

if __name__ == "__main__":
    update_config()
'''
    
    with open('config_helper.py', 'w') as f:
        f.write(config_helper)
    
    print("✅ Created 'config_helper.py' to easily update your configuration")

if __name__ == "__main__":
    print_atlas_setup()
    create_config_updater()
    
    print(f"\n📅 Setup guide created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n🎯 Next Steps:")
    print("1. Follow the setup guide above")
    print("2. Run: python3 config_helper.py (to update config)")
    print("3. Run: python3 import_to_mongodb.py (to import data)")
