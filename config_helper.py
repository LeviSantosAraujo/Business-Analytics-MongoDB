
"""
Config Helper - Update your MongoDB connection string
"""

def update_config():
    """Interactive config update"""
    
    print("🔧 MongoDB Atlas Configuration Updater")
    print("="*50)
    
    # Get connection string from user
    connection_string = input("\nEnter your MongoDB Atlas connection string: ").strip()
    
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
