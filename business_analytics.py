"""
Comprehensive Business Analytics Suite
All analytics types for your 1.1M business records
"""

import pandas as pd
from pymongo import MongoClient
import json
from datetime import datetime
import time

class BusinessAnalyticsSuite:
    """Complete analytics suite for business data"""
    
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client['business_data']
        self.collection = self.db['company_metrics']
        
    def financial_performance_analysis(self):
        """Analyze financial performance metrics"""
        print("\n" + "="*60)
        print("📊 FINANCIAL PERFORMANCE ANALYSIS")
        print("="*60)
        
        analytics = {}
        
        # 1. Revenue trends by year
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
        
        analytics['revenue_trends'] = revenue_trends
        
        # 2. Profit margin analysis
        print("\n2. 💰 Profit Margin Analysis:")
        profit_analysis = list(self.collection.aggregate([
            {"$group": {
                "_id": None,
                "avg_profit_margin": {"$avg": "$Profit_Margin"},
                "min_profit_margin": {"$min": "$Profit_Margin"},
                "max_profit_margin": {"$max": "$Profit_Margin"},
                "high_profit_companies": {"$sum": {"$cond": [{"$gt": ["$Profit_Margin", 0.8]}, 1, 0]}}
            }},
            {"$project": {
                "avg_profit_margin": {"$round": ["$avg_profit_margin", 4]},
                "min_profit_margin": {"$round": ["$min_profit_margin", 4]},
                "max_profit_margin": {"$round": ["$max_profit_margin", 4]},
                "high_profit_companies": 1
            }}
        ]))
        
        if profit_analysis:
            pa = profit_analysis[0]
            print(f"   Average Profit Margin: {pa['avg_profit_margin']:.2%}")
            print(f"   Profit Margin Range: {pa['min_profit_margin']:.2%} - {pa['max_profit_margin']:.2%}")
            print(f"   High Profit Companies (>80%): {pa['high_profit_companies']:,}")
        
        analytics['profit_analysis'] = profit_analysis
        
        # 3. Sales vs Revenue correlation
        print("\n3. 🔄 Sales vs Revenue Analysis:")
        sales_revenue = list(self.collection.aggregate([
            {"$group": {
                "_id": None,
                "total_sales": {"$sum": "$Total_Sales"},
                "total_revenue": {"$sum": "$Total_Revenue"},
                "avg_sales_ratio": {"$avg": {"$divide": ["$Total_Sales", "$Total_Revenue"]}}
            }},
            {"$project": {
                "sales_to_revenue_ratio": {"$round": [{"$divide": ["$total_sales", "$total_revenue"]}, 4]},
                "avg_individual_ratio": {"$round": ["$avg_sales_ratio", 4]}
            }}
        ]))
        
        if sales_revenue:
            sr = sales_revenue[0]
            print(f"   Overall Sales/Revenue Ratio: {sr['sales_to_revenue_ratio']:.2%}")
            print(f"   Average Company Sales/Revenue Ratio: {sr['avg_individual_ratio']:.2%}")
        
        analytics['sales_revenue'] = sales_revenue
        
        return analytics
    
    def growth_analytics(self):
        """Analyze growth patterns and trends"""
        print("\n" + "="*60)
        print("📈 GROWTH ANALYTICS")
        print("="*60)
        
        analytics = {}
        
        # 1. Year-over-year growth rates
        print("\n1. 📊 Year-over-Year Growth Rates:")
        growth_rates = list(self.collection.aggregate([
            {"$group": {
                "_id": "$Year",
                "avg_growth": {"$avg": "$Revenue_Growth"},
                "positive_growth": {"$sum": {"$cond": [{"$gt": ["$Revenue_Growth", 0]}, 1, 0]}},
                "negative_growth": {"$sum": {"$cond": [{"$lt": ["$Revenue_Growth", 0]}, 1, 0]}},
                "total_companies": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}},
            {"$project": {
                "year": "$_id",
                "avg_growth": {"$round": ["$avg_growth", 4]},
                "positive_growth": 1,
                "negative_growth": 1,
                "positive_growth_pct": {"$round": [{"$divide": ["$positive_growth", "$total_companies"]}, 4]},
                "negative_growth_pct": {"$round": [{"$divide": ["$negative_growth", "$total_companies"]}, 4]}
            }}
        ]))
        
        for growth in growth_rates:
            print(f"   {growth['year']}: Avg Growth {growth['avg_growth']:.2%}, "
                  f"Positive {growth['positive_growth_pct']:.1%}, Negative {growth['negative_growth_pct']:.1%}")
        
        analytics['growth_rates'] = growth_rates
        
        # 2. High-growth companies
        print("\n2. 🚀 High-Growth Companies Analysis:")
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
        
        analytics['high_growth'] = high_growth
        
        # 3. Growth distribution
        print("\n3. 📊 Growth Distribution:")
        growth_dist = list(self.collection.aggregate([
            {"$group": {
                "_id": {
                    "$switch": {
                        "branches": [
                            {"case": {"$lt": ["$Revenue_Growth", -0.2]}, "then": "Declining (>20% decline)"},
                            {"case": {"$lt": ["$Revenue_Growth", 0]}, "then": "Declining"},
                            {"case": {"$lt": ["$Revenue_Growth", 0.10]}, "then": "Slow Growth"},
                            {"case": {"$lt": ["$Revenue_Growth", 0.20]}, "then": "Moderate Growth"},
                            {"case": {"$lt": ["$Revenue_Growth", 0.30]}, "then": "Fast Growth"}
                        ],
                        "default": "Hyper Growth"
                    }
                },
                "count": {"$sum": 1},
                "avg_growth": {"$avg": "$Revenue_Growth"}
            }},
            {"$sort": {"count": -1}}
        ]))
        
        for dist in growth_dist:
            percentage = (dist['count'] / 1100000) * 100  # Approximate total
            print(f"   {dist['_id']}: {dist['count']:,} companies ({percentage:.1f}%), "
                  f"Avg Growth {dist['avg_growth']:.2%}")
        
        analytics['growth_distribution'] = growth_dist
        
        return analytics
    
    def market_segmentation(self):
        """Segment companies by size and performance"""
        print("\n" + "="*60)
        print("🎯 MARKET SEGMENTATION")
        print("="*60)
        
        analytics = {}
        
        # 1. Company size segmentation
        print("\n1. 🏢 Company Size Segmentation:")
        size_segments = list(self.collection.aggregate([
            {"$group": {
                "_id": {"$switch": {
                    "branches": [
                        {"case": {"$lt": ["$Total_Revenue", 10000000]}, "then": "Small (<$10M)"},
                        {"case": {"$lt": ["$Total_Revenue", 100000000]}, "then": "Medium ($10M-$100M)"},
                        {"case": {"$lt": ["$Total_Revenue", 1000000000]}, "then": "Large ($100M-$1B)"},
                        {"default": "Enterprise (>$1B)"}
                    ]
                }},
                "count": {"$sum": 1},
                "avg_revenue": {"$avg": "$Total_Revenue"},
                "avg_profit_margin": {"$avg": "$Profit_Margin"},
                "total_market_cap": {"$sum": "$Market_Cap"}
            }},
            {"$sort": {"avg_revenue": 1}}
        ]))
        
        for segment in size_segments:
            percentage = (segment['count'] / 1100000) * 100
            print(f"   {segment['_id']}:")
            print(f"     Count: {segment['count']:,} ({percentage:.1f}%)")
            print(f"     Avg Revenue: ${segment['avg_revenue']:,.0f}")
            print(f"     Avg Profit Margin: {segment['avg_profit_margin']:.2%}")
            print(f"     Total Market Cap: ${segment['total_market_cap']:,.0f}")
        
        analytics['size_segments'] = size_segments
        
        # 2. Performance-based segmentation
        print("\n2. ⭐ Performance-Based Segmentation:")
        perf_segments = list(self.collection.aggregate([
            {"$group": {
                "_id": {
                    "$switch": {
                        "branches": [
                            {"case": {"$and": [
                                {"$gt": ["$Profit_Margin", 0.8]},
                                {"$gt": ["$Revenue_Growth", 0.15]}
                            ]}, "then": "Star Performers"},
                            {"case": {"$gt": ["$Profit_Margin", 0.8]}, "then": "High Profit"},
                            {"case": {"$gt": ["$Revenue_Growth", 0.15]}, "then": "Fast Growers"},
                            {"case": {"$and": [
                                {"$gt": ["$Profit_Margin", 0.5]},
                                {"$gt": ["$Revenue_Growth", 0]}
                            ]}, "then": "Steady Performers"}
                        ],
                        "default": "Needs Improvement"
                    }
                },
                "count": {"$sum": 1},
                "avg_revenue": {"$avg": "$Total_Revenue"},
                "avg_profit_margin": {"$avg": "$Profit_Margin"},
                "avg_growth": {"$avg": "$Revenue_Growth"}
            }},
            {"$sort": {"count": -1}}
        ]))
        
        for segment in perf_segments:
            percentage = (segment['count'] / 1100000) * 100
            print(f"   {segment['_id']}: {segment['count']:,} ({percentage:.1f}%)")
            print(f"     Avg Revenue: ${segment['avg_revenue']:,.0f}")
            print(f"     Avg Profit Margin: {segment['avg_profit_margin']:.2%}")
            print(f"     Avg Growth: {segment['avg_growth']:.2%}")
        
        analytics['performance_segments'] = perf_segments
        
        return analytics
    
    def performance_benchmarks(self):
        """Identify top and bottom performers"""
        print("\n" + "="*60)
        print("🏆 PERFORMANCE BENCHMARKS")
        print("="*60)
        
        analytics = {}
        
        # 1. Top performers by market cap
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
        
        analytics['top_market_cap'] = top_market_cap
        
        # 2. Most profitable companies
        print("\n2. 💎 Top 10 Most Profitable Companies:")
        most_profitable = list(self.collection.find(
            {"Profit_Margin": {"$gt": 0}},
            {"Year": 1, "Total_Revenue": 1, "Profit_Margin": 1, "Revenue_Growth": 1}
        ).sort("Profit_Margin", -1).limit(10))
        
        for i, company in enumerate(most_profitable, 1):
            print(f"   {i}. Year {company['Year']}: Profit Margin {company['Profit_Margin']:.2%}")
            print(f"      Revenue: ${company['Total_Revenue']:,.0f}, Growth: {company['Revenue_Growth']:.2%}")
        
        analytics['most_profitable'] = most_profitable
        
        # 3. Fastest growing companies
        print("\n3. 🚀 Top 10 Fastest Growing Companies:")
        fastest_growing = list(self.collection.find(
            {"Revenue_Growth": {"$gt": 0}},
            {"Year": 1, "Total_Revenue": 1, "Revenue_Growth": 1, "Profit_Margin": 1}
        ).sort("Revenue_Growth", -1).limit(10))
        
        for i, company in enumerate(fastest_growing, 1):
            print(f"   {i}. Year {company['Year']}: Growth {company['Revenue_Growth']:.2%}")
            print(f"      Revenue: ${company['Total_Revenue']:,.0f}, "
                  f"Profit Margin: {company['Profit_Margin']:.2%}")
        
        analytics['fastest_growing'] = fastest_growing
        
        # 4. Bottom performers (for analysis)
        print("\n4. ⚠️  Bottom 10 Performers (Low Growth & Profit):")
        bottom_performers = list(self.collection.find({
            "$and": [
                {"Revenue_Growth": {"$lt": -0.1}},
                {"Profit_Margin": {"$lt": 0.3}}
            ]
        }, {"Year": 1, "Total_Revenue": 1, "Revenue_Growth": 1, "Profit_Margin": 1}).sort("Revenue_Growth", 1).limit(10))
        
        for i, company in enumerate(bottom_performers, 1):
            print(f"   {i}. Year {company['Year']}: Growth {company['Revenue_Growth']:.2%}")
            print(f"      Revenue: ${company['Total_Revenue']:,.0f}, "
                  f"Profit Margin: {company['Profit_Margin']:.2%}")
        
        analytics['bottom_performers'] = bottom_performers
        
        return analytics
    
    def statistical_analysis(self):
        """Comprehensive statistical analysis"""
        print("\n" + "="*60)
        print("📊 STATISTICAL ANALYSIS")
        print("="*60)
        
        analytics = {}
        
        # 1. Revenue distribution statistics
        print("\n1. 💰 Revenue Distribution Statistics:")
        revenue_stats = list(self.collection.aggregate([
            {"$group": {
                "_id": None,
                "min_revenue": {"$min": "$Total_Revenue"},
                "max_revenue": {"$max": "$Total_Revenue"},
                "avg_revenue": {"$avg": "$Total_Revenue"},
                "median_revenue": {"$median": "$Total_Revenue"},
                "std_dev_revenue": {"$stdDevPop": "$Total_Revenue"},
                "total_companies": {"$sum": 1}
            }}
        ]))
        
        if revenue_stats:
            rs = revenue_stats[0]
            print(f"   Companies: {rs['total_companies']:,}")
            print(f"   Revenue Range: ${rs['min_revenue']:,.0f} - ${rs['max_revenue']:,.0f}")
            print(f"   Average Revenue: ${rs['avg_revenue']:,.0f}")
            print(f"   Median Revenue: ${rs['median_revenue']:,.0f}")
            print(f"   Standard Deviation: ${rs['std_dev_revenue']:,.0f}")
        
        analytics['revenue_stats'] = revenue_stats
        
        # 2. Correlation analysis
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
        
        analytics['correlations'] = correlations
        
        # 3. Percentile analysis
        print("\n3. 📈 Percentile Analysis:")
        percentiles = list(self.collection.aggregate([
            {"$group": {
                "_id": None,
                "p10_revenue": {"$percentile": {"input": "$Total_Revenue", "p": [0.1], "method": "approximate"}},
                "p25_revenue": {"$percentile": {"input": "$Total_Revenue", "p": [0.25], "method": "approximate"}},
                "p50_revenue": {"$percentile": {"input": "$Total_Revenue", "p": [0.5], "method": "approximate"}},
                "p75_revenue": {"$percentile": {"input": "$Total_Revenue", "p": [0.75], "method": "approximate"}},
                "p90_revenue": {"$percentile": {"input": "$Total_Revenue", "p": [0.9], "method": "approximate"}},
                "p10_profit": {"$percentile": {"input": "$Profit_Margin", "p": [0.1], "method": "approximate"}},
                "p90_profit": {"$percentile": {"input": "$Profit_Margin", "p": [0.9], "method": "approximate"}}
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
            print(f"   Profit Margin Percentiles:")
            print(f"     10th: {p['p10_profit'][0]:.2%}")
            print(f"     90th: {p['p90_profit'][0]:.2%}")
        
        analytics['percentiles'] = percentiles
        
        return analytics
    
    def generate_executive_summary(self):
        """Generate executive summary of all analytics"""
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
    
    def run_complete_analytics(self):
        """Run all analytics types"""
        start_time = time.time()
        
        print("🚀 STARTING COMPREHENSIVE BUSINESS ANALYTICS")
        print("="*80)
        
        try:
            # Run all analytics
            financial = self.financial_performance_analysis()
            growth = self.growth_analytics()
            segmentation = self.market_segmentation()
            benchmarks = self.performance_benchmarks()
            statistics = self.statistical_analysis()
            
            # Generate summary
            self.generate_executive_summary()
            
            # Combine all results
            all_analytics = {
                'financial_performance': financial,
                'growth_analytics': growth,
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
        print("⚠️  config.py not found")
        connection_string = "mongodb+srv://leviaraujo_db_user:RAfa7170*@businesscluster0.p0k3wou.mongodb.net/?appName=BusinessCluster0"
    
    # Run complete analytics
    analytics_suite = BusinessAnalyticsSuite(connection_string)
    results = analytics_suite.run_complete_analytics()
