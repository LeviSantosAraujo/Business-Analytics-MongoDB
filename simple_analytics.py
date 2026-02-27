"""
Simple Business Analytics Suite
Working analytics for your MongoDB business data
"""

import pandas as pd
from pymongo import MongoClient
import json
from datetime import datetime
import time

class SimpleBusinessAnalytics:
    """Simple but comprehensive analytics suite"""
    
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client['business_data']
        self.collection = self.db['company_metrics']
    
    def financial_performance(self):
        """Financial performance analysis"""
        print("\n" + "="*60)
        print("📊 FINANCIAL PERFORMANCE ANALYSIS")
        print("="*60)
        
        # Revenue trends by year
        print("\n1. 📈 Revenue Trends by Year:")
        revenue_trends = list(self.collection.aggregate([
            {"$group": {
                "_id": "$Year", 
                "avg_revenue": {"$avg": "$Total_Revenue"},
                "total_revenue": {"$sum": "$Total_Revenue"},
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}}
        ]))
        
        for trend in revenue_trends:
            print(f"   {trend['_id']}: Avg ${trend['avg_revenue']:,.0f}, Total ${trend['total_revenue']:,.0f} ({trend['count']:,} companies)")
        
        # Profit margin analysis
        print("\n2. 💰 Profit Margin Analysis:")
        profit_analysis = list(self.collection.aggregate([
            {"$group": {
                "_id": None,
                "avg_profit_margin": {"$avg": "$Profit_Margin"},
                "min_profit_margin": {"$min": "$Profit_Margin"},
                "max_profit_margin": {"$max": "$Profit_Margin"},
                "high_profit_companies": {"$sum": {"$cond": [{"$gt": ["$Profit_Margin", 0.8]}, 1, 0]}}
            }}
        ]))
        
        if profit_analysis:
            pa = profit_analysis[0]
            print(f"   Average Profit Margin: {pa['avg_profit_margin']:.2%}")
            print(f"   Profit Margin Range: {pa['min_profit_margin']:.2%} - {pa['max_profit_margin']:.2%}")
            print(f"   High Profit Companies (>80%): {pa['high_profit_companies']:,}")
        
        # Sales vs Revenue ratio
        print("\n3. 🔄 Sales vs Revenue Analysis:")
        sales_revenue = list(self.collection.aggregate([
            {"$group": {
                "_id": None,
                "total_sales": {"$sum": "$Total_Sales"},
                "total_revenue": {"$sum": "$Total_Revenue"},
                "avg_sales_ratio": {"$avg": {"$divide": ["$Total_Sales", "$Total_Revenue"]}}
            }}
        ]))
        
        if sales_revenue:
            sr = sales_revenue[0]
            overall_ratio = sr['total_sales'] / sr['total_revenue']
            print(f"   Overall Sales/Revenue Ratio: {overall_ratio:.2%}")
            print(f"   Average Company Sales/Revenue Ratio: {sr['avg_sales_ratio']:.2%}")
        
        return {
            'revenue_trends': revenue_trends,
            'profit_analysis': profit_analysis,
            'sales_revenue': sales_revenue
        }
    
    def growth_analysis(self):
        """Growth patterns analysis"""
        print("\n" + "="*60)
        print("📈 GROWTH ANALYTICS")
        print("="*60)
        
        # Year-over-year growth rates
        print("\n1. 📊 Year-over-Year Growth Rates:")
        growth_rates = list(self.collection.aggregate([
            {"$group": {
                "_id": "$Year",
                "avg_growth": {"$avg": "$Revenue_Growth"},
                "positive_growth": {"$sum": {"$cond": [{"$gt": ["$Revenue_Growth", 0]}, 1, 0]}},
                "negative_growth": {"$sum": {"$cond": [{"$lt": ["$Revenue_Growth", 0]}, 1, 0]}},
                "total_companies": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}}
        ]))
        
        for growth in growth_rates:
            positive_pct = growth['positive_growth'] / growth['total_companies'] * 100
            negative_pct = growth['negative_growth'] / growth['total_companies'] * 100
            print(f"   {growth['_id']}: Avg Growth {growth['avg_growth']:.2%}, "
                  f"Positive {positive_pct:.1f}%, Negative {negative_pct:.1f}%")
        
        # High-growth companies
        print("\n2. 🚀 High-Growth Companies (>20% growth):")
        high_growth = list(self.collection.aggregate([
            {"$match": {"Revenue_Growth": {"$gt": 0.20}}},
            {"$group": {
                "_id": "$Year",
                "high_growth_count": {"$sum": 1},
                "avg_high_growth": {"$avg": "$Revenue_Growth"},
                "avg_revenue_high_growth": {"$avg": "$Total_Revenue"}
            }},
            {"$sort": {"_id": 1}}
        ]))
        
        for hg in high_growth:
            print(f"   {hg['_id']}: {hg['high_growth_count']:,} companies, "
                  f"Avg Growth {hg['avg_high_growth']:.2%}, "
                  f"Avg Revenue ${hg['avg_revenue_high_growth']:,.0f}")
        
        # Growth distribution (simplified)
        print("\n3. 📊 Growth Distribution:")
        growth_categories = [
            {"name": "Strong Decline (<-20%)", "condition": {"$lt": ["$Revenue_Growth", -0.2]}},
            {"name": "Decline (<0%)", "condition": {"$lt": ["$Revenue_Growth", 0]}},
            {"name": "Slow Growth (0-10%)", "condition": {"$lt": ["$Revenue_Growth", 0.10]}},
            {"name": "Moderate Growth (10-20%)", "condition": {"$lt": ["$Revenue_Growth", 0.20]}},
            {"name": "Fast Growth (>20%)", "condition": {"$gte": ["$Revenue_Growth", 0.20]}}
        ]
        
        for category in growth_categories:
            count = self.collection.count_documents({"Revenue_Growth": category["condition"]})
            percentage = (count / 1100000) * 100
            print(f"   {category['name']}: {count:,} companies ({percentage:.1f}%)")
        
        return {
            'growth_rates': growth_rates,
            'high_growth': high_growth,
            'growth_distribution': growth_categories
        }
    
    def market_segmentation(self):
        """Market segmentation analysis"""
        print("\n" + "="*60)
        print("🎯 MARKET SEGMENTATION")
        print("="*60)
        
        # Company size segmentation
        print("\n1. 🏢 Company Size Segmentation:")
        
        size_segments = [
            {"name": "Small (<$10M)", "condition": {"$lt": ["$Total_Revenue", 10000000]}},
            {"name": "Medium ($10M-$100M)", "condition": {"$and": [
                {"$gte": ["$Total_Revenue", 10000000]},
                {"$lt": ["$Total_Revenue", 100000000]}
            ]}},
            {"name": "Large ($100M-$1B)", "condition": {"$and": [
                {"$gte": ["$Total_Revenue", 100000000]},
                {"$lt": ["$Total_Revenue", 1000000000]}
            ]}},
            {"name": "Enterprise (>$1B)", "condition": {"$gte": ["$Total_Revenue", 1000000000]}}
        ]
        
        for segment in size_segments:
            companies = list(self.collection.aggregate([
                {"$match": {"Total_Revenue": segment["condition"]}},
                {"$group": {
                    "_id": None,
                    "count": {"$sum": 1},
                    "avg_revenue": {"$avg": "$Total_Revenue"},
                    "avg_profit_margin": {"$avg": "$Profit_Margin"},
                    "total_market_cap": {"$sum": "$Market_Cap"}
                }}
            ]))
            
            if companies:
                comp = companies[0]
                percentage = (comp['count'] / 1100000) * 100
                print(f"   {segment['name']}: {comp['count']:,} ({percentage:.1f}%)")
                print(f"     Avg Revenue: ${comp['avg_revenue']:,.0f}")
                print(f"     Avg Profit Margin: {comp['avg_profit_margin']:.2%}")
                print(f"     Total Market Cap: ${comp['total_market_cap']:,.0f}")
        
        # Performance segmentation
        print("\n2. ⭐ Performance-Based Segmentation:")
        
        perf_segments = [
            {"name": "Star Performers", "condition": {"$and": [
                {"$gt": ["$Profit_Margin", 0.8]},
                {"$gt": ["$Revenue_Growth", 0.15]}
            ]}},
            {"name": "High Profit", "condition": {"$gt": ["$Profit_Margin", 0.8]}},
            {"name": "Fast Growers", "condition": {"$gt": ["$Revenue_Growth", 0.15]}},
            {"name": "Steady Performers", "condition": {"$and": [
                {"$gt": ["$Profit_Margin", 0.5]},
                {"$gt": ["$Revenue_Growth", 0]}
            ]}},
            {"name": "Needs Improvement", "condition": {"$and": [
                {"$lte": ["$Profit_Margin", 0.5]},
                {"$lte": ["$Revenue_Growth", 0]}
            ]}}
        ]
        
        for segment in perf_segments:
            companies = list(self.collection.aggregate([
                {"$match": segment["condition"]},
                {"$group": {
                    "_id": None,
                    "count": {"$sum": 1},
                    "avg_revenue": {"$avg": "$Total_Revenue"},
                    "avg_profit_margin": {"$avg": "$Profit_Margin"},
                    "avg_growth": {"$avg": "$Revenue_Growth"}
                }}
            ]))
            
            if companies:
                comp = companies[0]
                percentage = (comp['count'] / 1100000) * 100
                print(f"   {segment['name']}: {comp['count']:,} ({percentage:.1f}%)")
                print(f"     Avg Revenue: ${comp['avg_revenue']:,.0f}")
                print(f"     Avg Profit Margin: {comp['avg_profit_margin']:.2%}")
                print(f"     Avg Growth: {comp['avg_growth']:.2%}")
        
        return {
            'size_segments': size_segments,
            'performance_segments': perf_segments
        }
    
    def performance_benchmarks(self):
        """Top and bottom performers"""
        print("\n" + "="*60)
        print("🏆 PERFORMANCE BENCHMARKS")
        print("="*60)
        
        # Top performers by market cap
        print("\n1. 💰 Top 10 Companies by Market Cap:")
        top_market_cap = list(self.collection.find(
            {}, 
            {"Year": 1, "Total_Revenue": 1, "Total_Sales": 1, "Market_Cap": 1, "Profit_Margin": 1, "Revenue_Growth": 1}
        ).sort("Market_Cap", -1).limit(10))
        
        for i, company in enumerate(top_market_cap, 1):
            print(f"   {i}. Year {company['Year']}: Market Cap ${company['Market_Cap']:,.0f}")
            print(f"      Revenue: ${company['Total_Revenue']:,.0f}, "
                  f"Profit Margin: {company['Profit_Margin']:.2%}, "
                  f"Growth: {company['Revenue_Growth']:.2%}")
        
        # Most profitable companies
        print("\n2. 💎 Top 10 Most Profitable Companies:")
        most_profitable = list(self.collection.find(
            {"Profit_Margin": {"$gt": 0}},
            {"Year": 1, "Total_Revenue": 1, "Profit_Margin": 1, "Revenue_Growth": 1}
        ).sort("Profit_Margin", -1).limit(10))
        
        for i, company in enumerate(most_profitable, 1):
            print(f"   {i}. Year {company['Year']}: Profit Margin {company['Profit_Margin']:.2%}")
            print(f"      Revenue: ${company['Total_Revenue']:,.0f}, Growth: {company['Revenue_Growth']:.2%}")
        
        # Fastest growing companies
        print("\n3. 🚀 Top 10 Fastest Growing Companies:")
        fastest_growing = list(self.collection.find(
            {"Revenue_Growth": {"$gt": 0}},
            {"Year": 1, "Total_Revenue": 1, "Revenue_Growth": 1, "Profit_Margin": 1}
        ).sort("Revenue_Growth", -1).limit(10))
        
        for i, company in enumerate(fastest_growing, 1):
            print(f"   {i}. Year {company['Year']}: Growth {company['Revenue_Growth']:.2%}")
            print(f"      Revenue: ${company['Total_Revenue']:,.0f}, "
                  f"Profit Margin: {company['Profit_Margin']:.2%}")
        
        return {
            'top_market_cap': top_market_cap,
            'most_profitable': most_profitable,
            'fastest_growing': fastest_growing
        }
    
    def statistical_analysis(self):
        """Statistical analysis"""
        print("\n" + "="*60)
        print("📊 STATISTICAL ANALYSIS")
        print("="*60)
        
        # Revenue distribution statistics
        print("\n1. 💰 Revenue Distribution Statistics:")
        revenue_stats = list(self.collection.aggregate([
            {"$group": {
                "_id": None,
                "min_revenue": {"$min": "$Total_Revenue"},
                "max_revenue": {"$max": "$Total_Revenue"},
                "avg_revenue": {"$avg": "$Total_Revenue"},
                "total_companies": {"$sum": 1}
            }}
        ]))
        
        if revenue_stats:
            rs = revenue_stats[0]
            print(f"   Companies: {rs['total_companies']:,}")
            print(f"   Revenue Range: ${rs['min_revenue']:,.0f} - ${rs['max_revenue']:,.0f}")
            print(f"   Average Revenue: ${rs['avg_revenue']:,.0f}")
        
        # Correlation analysis
        print("\n2. 🔗 Correlation Analysis:")
        correlations = list(self.collection.aggregate([
            {"$group": {
                "_id": None,
                "revenue_sales_corr": {"$corr": ["$Total_Revenue", "$Total_Sales"]},
                "revenue_profit_corr": {"$corr": ["$Total_Revenue", "$Profit_Margin"]},
                "growth_profit_corr": {"$corr": ["$Revenue_Growth", "$Profit_Margin"]},
                "market_cap_revenue_corr": {"$corr": ["$Market_Cap", "$Total_Revenue"]}
            }}
        ]))
        
        if correlations:
            corr = correlations[0]
            print(f"   Revenue ↔ Sales: {corr['revenue_sales_corr']:.4f}")
            print(f"   Revenue ↔ Profit Margin: {corr['revenue_profit_corr']:.4f}")
            print(f"   Growth ↔ Profit Margin: {corr['growth_profit_corr']:.4f}")
            print(f"   Market Cap ↔ Revenue: {corr['market_cap_revenue_corr']:.4f}")
        
        # Percentile analysis
        print("\n3. 📈 Percentile Analysis:")
        percentiles = list(self.collection.aggregate([
            {"$group": {
                "_id": None,
                "p10_revenue": {"$percentile": {"input": "$Total_Revenue", "p": [0.1], "method": "approximate"}},
                "p25_revenue": {"$percentile": {"input": "$Total_Revenue", "p": [0.25], "method": "approximate"}},
                "p50_revenue": {"$percentile": {"input": "$Total_Revenue", "p": [0.5], "method": "approximate"}},
                "p75_revenue": {"$percentile": {"input": "$Total_Revenue", "p": [0.75], "method": "approximate"}},
                "p90_revenue": {"$percentile": {"input": "$Total_Revenue", "p": [0.9], "method": "approximate"}}
            }}
        ]))
        
        if percentiles:
            p = percentiles[0]
            print(f"   Revenue Percentiles:")
            print(f"     10th: ${p['p10_revenue'][0]:,.0f}")
            print(f"     25th: ${p['p25_revenue'][0]:,.0f}")
            print(f"     50th: ${p['p50_revenue'][0]:,.0f}")
            print(f"     75th: ${p['p75_revenue'][0]:,.0f}")
            print(f"     90th: ${p['p90_revenue'][0]:,.0f}")
        
        return {
            'revenue_stats': revenue_stats,
            'correlations': correlations,
            'percentiles': percentiles
        }
    
    def executive_summary(self):
        """Generate executive summary"""
        print("\n" + "="*80)
        print("📋 EXECUTIVE SUMMARY - BUSINESS ANALYTICS REPORT")
        print("="*80)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Dataset: 1.1M business records (2015-2025)")
        
        # Quick stats
        total_companies = self.collection.count_documents({})
        total_revenue = list(self.collection.aggregate([{"$group": {"_id": None, "total": {"$sum": "$Total_Revenue"}}}]))
        total_market_cap = list(self.collection.aggregate([{"$group": {"_id": None, "total": {"$sum": "$Market_Cap"}}}]))
        
        print(f"\n📊 KEY METRICS:")
        print(f"   Total Companies: {total_companies:,}")
        print(f"   Total Revenue: ${total_revenue[0]['total']:,.0f}")
        print(f"   Total Market Cap: ${total_market_cap[0]['total']:,.0f}")
        
        # Year with most data
        year_counts = list(self.collection.aggregate([
            {"$group": {"_id": "$Year", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ]))
        
        if year_counts:
            print(f"   Most Recent Year: {year_counts[0]['_id']} ({year_counts[0]['count']:,} records)")
        
        print(f"\n🎯 KEY INSIGHTS:")
        print(f"   • Dataset spans 11 years of business performance")
        print(f"   • Comprehensive financial metrics available for analysis")
        print(f"   • Ready for advanced business intelligence and ML applications")
        
        print("="*80)
    
    def run_all_analytics(self):
        """Run all analytics types"""
        start_time = time.time()
        
        print("🚀 STARTING COMPREHENSIVE BUSINESS ANALYTICS")
        print("="*80)
        
        try:
            # Run all analytics
            financial = self.financial_performance()
            growth = self.growth_analysis()
            segmentation = self.market_segmentation()
            benchmarks = self.performance_benchmarks()
            statistics = self.statistical_analysis()
            
            # Generate summary
            self.executive_summary()
            
            # Combine all results
            all_analytics = {
                'financial_performance': financial,
                'growth_analysis': growth,
                'market_segmentation': segmentation,
                'performance_benchmarks': benchmarks,
                'statistical_analysis': statistics,
                'generated_at': datetime.now().isoformat()
            }
            
            # Save results to file
            with open('business_analytics_results.json', 'w') as f:
                json.dump(all_analytics, f, indent=2, default=str)
            
            end_time = time.time()
            
            print(f"\n✅ ANALYTICS COMPLETE!")
            print(f"⏱️  Total Time: {end_time - start_time:.1f} seconds")
            print(f"📁 Results saved to: business_analytics_results.json")
            print(f"🔍 Ready for business insights and decision-making!")
            
            return all_analytics
            
        except Exception as e:
            print(f"❌ Analytics Error: {e}")
            return None
        
        finally:
            self.client.close()

if __name__ == "__main__":
    # Load configuration
    try:
        import config
        connection_string = config.MONGODB_CONNECTION_STRING
    except ImportError:
        connection_string = "mongodb+srv://leviaraujo_db_user:RAfa7170*@businesscluster0.p0k3wou.mongodb.net/?appName=BusinessCluster0"
    
    # Run complete analytics
    analytics_suite = SimpleBusinessAnalytics(connection_string)
    results = analytics_suite.run_all_analytics()
