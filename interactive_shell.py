"""
Interactive MongoDB Query Shell
Type queries directly and see results instantly
"""

import pymongo
from mongodb_bond_alert import MongoDBBondAlert
import json
from datetime import datetime
import pandas as pd

class InteractiveMongoShell:
    """Interactive shell for MongoDB queries"""
    
    def __init__(self, connection_string):
        self.alert_system = MongoDBBondAlert(connection_string)
        self.records = self.alert_system.records
        self.alerts = self.alert_system.alerts
        
        # Available collections
        self.collections = {
            'records': self.records,
            'alerts': self.alerts
        }
    
    def display_help(self):
        """Show available commands and examples"""
        help_text = """
🔍 MONGODB INTERACTIVE SHELL - HELP

📋 COLLECTIONS:
  - records: Bond return data
  - alerts: Alert history

⚡ BASIC COMMANDS:
  find()                    - Show all documents (limited)
  find_one()               - Show single document
  count()                  - Count documents
  distinct(field)          - Get unique values

🔧 QUERY EXAMPLES:
  find({'year': 2022})                    - Specific year
  find({'sp500_return': {'$gt': 0.20}})   - S&P > 20%
  find({'$or': [{'sp500_return': {'$gt': 0.25}}, {'baa_bond_return': {'$gt': 0.10}}]}) - OR query
  
📊 AGGREGATION EXAMPLES:
  aggregate([{'$group': {'_id': None, 'avg_sp500': {'$avg': '$sp500_return'}}}])
  aggregate([{'$match': {'sp500_return': {'$gt': 0}}}, {'$count': 'positive_years'}])

🎯 SPECIAL COMMANDS:
  help                     - Show this help
  stats                    - Database statistics
  indexes                  - Show indexes
  exit/quit                - Exit shell

💡 TIPS:
  - Use collection_name.command() format
  - Add .limit(5) to limit results
  - Use {'field': 1, '_id': 0} for field projection
  - Chain commands: find().limit(3).sort('year', -1)
"""
        print(help_text)
    
    def show_stats(self):
        """Display database statistics"""
        print("\n📊 DATABASE STATISTICS")
        print("="*50)
        
        for name, collection in self.collections.items():
            count = collection.count_documents({})
            print(f"{name.upper()}: {count:,} documents")
        
        # Sample data
        print(f"\n📋 SAMPLE RECORD:")
        sample = self.records.find_one()
        if sample:
            print(json.dumps(sample, indent=2, default=str))
    
    def show_indexes(self):
        """Display collection indexes"""
        print("\n🔍 COLLECTION INDEXES")
        print("="*50)
        
        for name, collection in self.collections.items():
            print(f"\n{name.upper()}:")
            indexes = collection.list_indexes()
            for index in indexes:
                print(f"  - {index['name']}: {index['key']}")
    
    def execute_query(self, collection_name, query_string):
        """Execute a MongoDB query and display results"""
        try:
            collection = self.collections.get(collection_name)
            if not collection:
                return f"❌ Collection '{collection_name}' not found. Use: records or alerts"
            
            # Parse and execute the query
            if query_string == 'find()':
                result = list(collection.find().limit(10))
            elif query_string == 'find_one()':
                result = collection.find_one()
            elif query_string == 'count()':
                result = collection.count_documents({})
            elif query_string.startswith('find('):
                # Extract JSON query from find(...)
                query_part = query_string[5:-1]  # Remove 'find(' and ')'
                if query_part:
                    query = json.loads(query_part)
                    result = list(collection.find(query).limit(10))
                else:
                    result = list(collection.find().limit(10))
            elif query_string.startswith('find_one('):
                query_part = query_string[10:-1]
                if query_part:
                    query = json.loads(query_part)
                    result = collection.find_one(query)
                else:
                    result = collection.find_one()
            elif query_string.startswith('distinct('):
                field = query_string[9:-2]  # Remove 'distinct(' and ')'
                result = collection.distinct(field)
            elif query_string.startswith('aggregate('):
                pipeline_part = query_string[11:-1]  # Remove 'aggregate(' and ')'
                pipeline = json.loads(pipeline_part)
                result = list(collection.aggregate(pipeline))
            else:
                return f"❌ Unknown query format: {query_string}"
            
            # Format and display results
            return self.format_results(result)
            
        except json.JSONDecodeError as e:
            return f"❌ Invalid JSON in query: {e}"
        except Exception as e:
            return f"❌ Query error: {e}"
    
    def format_results(self, result):
        """Format query results for display"""
        if result is None:
            return "📄 No document found"
        
        if isinstance(result, int):
            return f"📊 Count: {result:,}"
        
        if isinstance(result, list):
            if not result:
                return "📄 No documents found"
            
            if len(result) == 1:
                return self.format_single_document(result[0])
            else:
                output = [f"📋 Found {len(result)} documents:"]
                for i, doc in enumerate(result[:5], 1):
                    if 'year' in doc:
                        output.append(f"  {i}. Year {doc['year']}: S&P {doc.get('sp500_return', 0):.2%}")
                    else:
                        output.append(f"  {i}. {str(doc)[:80]}...")
                
                if len(result) > 5:
                    output.append(f"  ... and {len(result) - 5} more")
                
                return "\n".join(output)
        
        return self.format_single_document(result)
    
    def format_single_document(self, doc):
        """Format a single document for display"""
        if 'year' in doc:
            output = f"📄 Year {doc['year']}:\n"
            output += f"  S&P 500: {doc.get('sp500_return', 0):.2%}\n"
            output += f"  BAA Bond: {doc.get('baa_bond_return', 0):.2%}\n"
            output += f"  US Treasury: {doc.get('us_treasury_return', 0):.2%}"
            
            if 'alert_time' in doc:
                output += f"\n  Alert Time: {doc['alert_time']}"
            if 'alert_type' in doc:
                output += f"\n  Alert Type: {doc['alert_type']}"
            
            return output
        else:
            return f"📄 Document:\n{json.dumps(doc, indent=2, default=str)}"
    
    def run_interactive_shell(self):
        """Run the interactive shell"""
        print("🚀 MONGODB INTERACTIVE QUERY SHELL")
        print("="*50)
        print("Type 'help' for commands, 'exit' to quit")
        print("Format: collection.query (e.g., records.find())")
        print("="*50)
        
        while True:
            try:
                command = input("\n🔍 mongo> ").strip()
                
                if command.lower() in ['exit', 'quit']:
                    print("👋 Goodbye!")
                    break
                
                if command.lower() == 'help':
                    self.display_help()
                    continue
                
                if command.lower() == 'stats':
                    self.show_stats()
                    continue
                
                if command.lower() == 'indexes':
                    self.show_indexes()
                    continue
                
                if not command:
                    continue
                
                # Parse collection and query
                if '.' in command:
                    collection_name, query_string = command.split('.', 1)
                    result = self.execute_query(collection_name, query_string)
                    print(f"\n{result}")
                else:
                    print("❌ Use format: collection.query (e.g., records.find())")
                    print("   Type 'help' for examples")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        self.alert_system.close()

if __name__ == "__main__":
    # Load configuration
    try:
        import config
        connection_string = config.MONGODB_CONNECTION_STRING
    except ImportError:
        print("⚠️  config.py not found. Using default connection string.")
        connection_string = "mongodb://localhost:27017/"
    
    # Run interactive shell
    shell = InteractiveMongoShell(connection_string)
    shell.run_interactive_shell()
