"""
MongoDB Query Examples for Bond Alert System
Demonstrates various query patterns and operations
"""

import pymongo
from mongodb_bond_alert import MongoDBBondAlert
from datetime import datetime, timedelta
import json

class BondQueryEngine:
    """Advanced query interface for MongoDB bond data"""
    
    def __init__(self, connection_string):
        self.alert_system = MongoDBBondAlert(connection_string)
        self.records = self.alert_system.records
        self.alerts = self.alert_system.alerts
    
    def basic_queries(self):
        """Basic query examples"""
        print("="*60)
        print("BASIC MONGODB QUERIES")
        print("="*60)
        
        # 1. Find all records
        print("\n1. 📋 All Bond Records:")
        all_records = list(self.records.find().limit(5))
        for record in all_records:
            print(f"   Year {record['year']}: S&P {record['sp500_return']:.2%}, BAA {record['baa_bond_return']:.2%}")
        
        # 2. Find specific year
        print("\n2. 🎯 Specific Year (2022):")
        year_2022 = self.records.find_one({'year': 2022})
        if year_2022:
            print(f"   Found: S&P {year_2022['sp500_return']:.2%}, BAA {year_2022['baa_bond_return']:.2%}")
        
        # 3. Count documents
        print(f"\n3. 📊 Total Records: {self.records.count_documents({})}")
        print(f"   Total Alerts: {self.alerts.count_documents({})}")
    
    def comparison_queries(self):
        """Comparison and range queries"""
        print("\n" + "="*60)
        print("COMPARISON & RANGE QUERIES")
        print("="*60)
        
        # 1. S&P 500 returns above 20%
        print("\n1. 📈 S&P 500 Returns > 20%:")
        high_returns = list(self.records.find({'sp500_return': {'$gt': 0.20}}))
        for record in high_returns:
            print(f"   Year {record['year']}: {record['sp500_return']:.2%}")
        
        # 2. Negative returns (loss years)
        print("\n2. 📉 Negative Return Years:")
        negative_years = list(self.records.find({'sp500_return': {'$lt': 0}}))
        for record in negative_years:
            print(f"   Year {record['year']}: S&P {record['sp500_return']:.2%}, BAA {record['baa_bond_return']:.2%}")
        
        # 3. Range query (returns between 5% and 15%)
        print("\n3. 🎯 Moderate Returns (5%-15%):")
        moderate_returns = list(self.records.find({
            'sp500_return': {'$gte': 0.05, '$lte': 0.15}
        }))
        for record in moderate_returns:
            print(f"   Year {record['year']}: {record['sp500_return']:.2%}")
    
    def logical_queries(self):
        """Logical operators (AND, OR, NOT)"""
        print("\n" + "="*60)
        print("LOGICAL OPERATORS")
        print("="*60)
        
        # 1. OR query - high S&P OR high BAA returns
        print("\n1. 🔀 High Returns (S&P > 25% OR BAA > 10%):")
        high_any = list(self.records.find({
            '$or': [
                {'sp500_return': {'$gt': 0.25}},
                {'baa_bond_return': {'$gt': 0.10}}
            ]
        }))
        for record in high_any:
            print(f"   Year {record['year']}: S&P {record['sp500_return']:.2%}, BAA {record['baa_bond_return']:.2%}")
        
        # 2. AND query - positive returns for both
        print("\n2. ✅ Positive Returns (Both > 0):")
        positive_both = list(self.records.find({
            '$and': [
                {'sp500_return': {'$gt': 0}},
                {'baa_bond_return': {'$gt': 0}}
            ]
        }))
        for record in positive_both:
            print(f"   Year {record['year']}: S&P {record['sp500_return']:.2%}, BAA {record['baa_bond_return']:.2%}")
        
        # 3. NOR query - neither S&P nor BAA above 15%
        print("\n3. 🚫 Low Returns (Neither > 15%):")
        low_returns = list(self.records.find({
            '$nor': [
                {'sp500_return': {'$gt': 0.15}},
                {'baa_bond_return': {'$gt': 0.15}}
            ]
        }))
        for record in low_returns:
            print(f"   Year {record['year']}: S&P {record['sp500_return']:.2%}, BAA {record['baa_bond_return']:.2%}")
    
    def text_search_queries(self):
        """Text search and pattern matching"""
        print("\n" + "="*60)
        print("TEXT SEARCH & PATTERNS")
        print("="*60)
        
        # 1. Search by data source
        print("\n1. 📁 Records by Data Source:")
        sources = self.records.distinct('data_source')
        for source in sources:
            count = self.records.count_documents({'data_source': source})
            print(f"   {source}: {count} records")
        
        # 2. Regex search on alert types
        print("\n2. 🔍 Alert Types containing 'Bond':")
        bond_alerts = list(self.alerts.find({
            'alert_type': {'$regex': 'Bond', '$options': 'i'}
        }))
        for alert in bond_alerts[:5]:
            print(f"   Year {alert['year']}: {alert['alert_type']}")
    
    def aggregation_queries(self):
        """Aggregation pipeline examples"""
        print("\n" + "="*60)
        print("AGGREGATION PIPELINES")
        print("="*60)
        
        # 1. Average returns by decade
        print("\n1. 📊 Average Returns by Decade:")
        decade_pipeline = [
            {
                '$addFields': {
                    'decade': {
                        '$subtract': [
                            {'$mod': ['$year', 10]},
                            '$year'
                        ]
                    }
                }
            },
            {
                '$group': {
                    '_id': '$decade',
                    'avg_sp500': {'$avg': '$sp500_return'},
                    'avg_baa': {'$avg': '$baa_bond_return'},
                    'avg_treasury': {'$avg': '$us_treasury_return'},
                    'count': {'$sum': 1}
                }
            },
            {'$sort': {'_id': 1}}
        ]
        
        decade_results = list(self.records.aggregate(decade_pipeline))
        for result in decade_results:
            print(f"   {result['_id']}s: S&P {result['avg_sp500']:.2%}, BAA {result['avg_baa']:.2%}, Count: {result['count']}")
        
        # 2. Best and worst years
        print("\n2. 🏆 Best & Worst Years:")
        best_worst_pipeline = [
            {
                '$group': {
                    '_id': None,
                    'best_year': {'$max': {'$mergeObjects': [
                        {'year': '$year', 'sp500': '$sp500_return'},
                        {'score': '$sp500_return'}
                    ]}},
                    'worst_year': {'$min': {'$mergeObjects': [
                        {'year': '$year', 'sp500': '$sp500_return'},
                        {'score': '$sp500_return'}
                    ]}}
                }
            }
        ]
        
        best_worst = list(self.records.aggregate(best_worst_pipeline))
        if best_worst:
            result = best_worst[0]
            print(f"   Best Year: {result['best_year']['year']} ({result['best_year']['sp500']:.2%})")
            print(f"   Worst Year: {result['worst_year']['year']} ({result['worst_year']['sp500']:.2%})")
        
        # 3. Alert frequency by year
        print("\n3. 🚨 Alert Frequency by Year:")
        alert_freq_pipeline = [
            {
                '$group': {
                    '_id': '$year',
                    'alert_count': {'$sum': 1},
                    'alert_types': {'$addToSet': '$alert_type'}
                }
            },
            {'$sort': {'alert_count': -1}},
            {'$limit': 5}
        ]
        
        alert_freq = list(self.alerts.aggregate(alert_freq_pipeline))
        for result in alert_freq:
            print(f"   Year {result['_id']}: {result['alert_count']} alerts")
    
    def advanced_queries(self):
        """Advanced query techniques"""
        print("\n" + "="*60)
        print("ADVANCED QUERIES")
        print("="*60)
        
        # 1. Subquery - years with alerts AND high volatility
        print("\n1. 🎯 Years with Alerts & High Volatility:")
        alert_years = [alert['year'] for alert in self.alerts.find({}, {'year': 1})]
        volatile_years = list(self.records.find({
            'year': {'$in': alert_years},
            '$or': [
                {'sp500_return': {'$gt': 0.30}},
                {'sp500_return': {'$lt': -0.20}}
            ]
        }))
        for record in volatile_years:
            print(f"   Year {record['year']}: {record['sp500_return']:.2%} (Alert Year)")
        
        # 2. Date range queries
        print("\n2. 📅 Recent Alerts (Last 30 days):")
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_alerts = list(self.alerts.find({
            'alert_time': {'$gte': thirty_days_ago}
        }))
        print(f"   Found {len(recent_alerts)} recent alerts")
        
        # 3. Array operations with $elemMatch
        print("\n3. 🔍 Complex Alert Patterns:")
        complex_alerts = list(self.alerts.find({
            '$and': [
                {'sp500_return': {'$lt': 0.05}},
                {'baa_bond_return': {'$lt': 0.05}}
            ]
        }))
        for alert in complex_alerts:
            print(f"   Year {alert['year']}: Both low - S&P {alert['sp500_return']:.2%}, BAA {alert['baa_bond_return']:.2%}")
    
    def performance_queries(self):
        """Performance-optimized queries"""
        print("\n" + "="*60)
        print("PERFORMANCE QUERIES")
        print("="*60)
        
        # 1. Indexed queries (fast)
        print("\n1. ⚡ Indexed Query (by year):")
        import time
        start_time = time.time()
        year_query = self.records.find({'year': 2022})
        result = list(year_query)
        end_time = time.time()
        print(f"   Found {len(result)} records in {(end_time - start_time)*1000:.2f}ms")
        
        # 2. Projection (select specific fields)
        print("\n2. 📋 Field Projection (Only S&P Returns):")
        projected = list(self.records.find(
            {'sp500_return': {'$gt': 0}},
            {'year': 1, 'sp500_return': 1, '_id': 0}
        ).limit(5))
        for record in projected:
            print(f"   Year {record['year']}: {record['sp500_return']:.2%}")
        
        # 3. Limit and skip for pagination
        print("\n3. 📄 Pagination (Page 2, 3 records per page):")
        page2 = list(self.records.find({}).skip(3).limit(3))
        for record in page2:
            print(f"   Year {record['year']}: S&P {record['sp500_return']:.2%}")
    
    def run_all_queries(self):
        """Execute all query examples"""
        try:
            self.basic_queries()
            self.comparison_queries()
            self.logical_queries()
            self.text_search_queries()
            self.aggregation_queries()
            self.advanced_queries()
            self.performance_queries()
            
            print("\n" + "="*60)
            print("✅ ALL QUERIES COMPLETED SUCCESSFULLY!")
            print("="*60)
            
        except Exception as e:
            print(f"❌ Query Error: {str(e)}")
        
        finally:
            self.alert_system.close()

if __name__ == "__main__":
    # Load configuration
    try:
        import config
        connection_string = config.MONGODB_CONNECTION_STRING
    except ImportError:
        print("⚠️  config.py not found. Using default connection string.")
        connection_string = "mongodb://localhost:27017/"
    
    # Run query examples
    query_engine = BondQueryEngine(connection_string)
    query_engine.run_all_queries()
