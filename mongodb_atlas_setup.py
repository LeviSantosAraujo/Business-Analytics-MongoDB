"""
MongoDB Atlas Setup Guide
Step-by-step setup for free cloud MongoDB
"""

import webbrowser
from datetime import datetime

def print_setup_guide():
    """Print detailed setup instructions"""
    
    print("="*80)
    print("MONGODB ATLAS SETUP - FREE CLOUD DATABASE")
    print("="*80)
    
    print("\n🚀 STEP 1: Create MongoDB Atlas Account")
    print("1. Go to: https://www.mongodb.com/cloud/atlas")
    print("2. Click 'Try Free' (no credit card required)")
    print("3. Sign up with Google/GitHub or email")
    
    print("\n🏗️  STEP 2: Create Your Free Cluster")
    print("1. Choose 'Shared Cluster' (FREE)")
    print("2. Select a cloud provider (AWS, GCP, or Azure)")
    print("3. Choose a region (pick one closest to you)")
    print("4. Cluster name: 'BondMonitoring' (or any name)")
    print("5. Click 'Create Cluster'")
    
    print("\n🔐 STEP 3: Create Database User")
    print("1. Go to 'Database Access' in left menu")
    print("2. Click 'Add New Database User'")
    print("3. Username: bonduser")
    print("4. Password: Create a strong password (save it!)")
    print("5. Permissions: 'Read and write to any database'")
    print("6. Click 'Add User'")
    
    print("\n🌐 STEP 4: Whitelist Your IP Address")
    print("1. Go to 'Network Access' in left menu")
    print("2. Click 'Add IP Address'")
    print("3. Select 'Allow Access from Anywhere' (0.0.0.0/0)")
    print("4. Click 'Confirm'")
    
    print("\n🔗 STEP 5: Get Your Connection String")
    print("1. Go to 'Database' in left menu")
    print("2. Click 'Connect' for your cluster")
    print("3. Select 'Connect your application'")
    print("4. Choose 'Python' and version 3.9 or later")
    print("5. Copy the connection string")
    print("6. Replace <password> with your actual password")
    
    print("\n⚙️  STEP 6: Update Your Code")
    print("Replace this line in mongodb_bond_alert.py:")
    print("  alert_system = MongoDBBondAlert()")
    print("With:")
    print("  alert_system = MongoDBBondAlert('your_connection_string_here')")
    
    print("\n✅ STEP 7: Test Your Connection")
    print("Run: python3 mongodb_bond_alert.py")
    
    print("\n" + "="*80)
    print("🎯 YOUR FREE ATLAS BENEFITS:")
    print("• 512MB storage (plenty for learning)")
    print("• Unlimited collections and documents")
    print("• Full MongoDB features")
    print("• 24/7 monitoring and backups")
    print("• Global CDN for fast access")
    print("="*80)

def create_connection_template():
    """Create a template for connection string"""
    
    template = '''
# MongoDB Atlas Connection Template
# Replace YOUR_PASSWORD with your actual password

CONNECTION_STRING = "mongodb+srv://bonduser:YOUR_PASSWORD@bondmonitoring.xxxxx.mongodb.net/?retryWrites=true&w=majority"

# Example usage:
# alert_system = MongoDBBondAlert(CONNECTION_STRING)
'''
    
    with open('connection_template.py', 'w') as f:
        f.write(template)
    
    print("✅ Created 'connection_template.py' with connection string format")

if __name__ == "__main__":
    print_setup_guide()
    create_connection_template()
    
    print(f"\n📅 Setup completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n💡 Pro Tip: Save your connection string in a separate file!")
    print("   Never commit passwords to Git repositories.")
