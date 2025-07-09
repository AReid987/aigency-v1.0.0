#!/usr/bin/env python3
"""
Quality Neighbor Market Research Analysis
Comprehensive market analysis with competitive positioning and demographic insights
"""

import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Font configuration for better rendering
plt.rcParams['font.size'] = 10
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

class QualityNeighborMarketAnalysis:
    def __init__(self):
        self.market_data = {}
        self.competitors = {}
        self.demographics = {}
        self.load_research_data()
    
    def load_research_data(self):
        """Load all research data from JSON files"""
        try:
            # Load market data
            with open('/workspace/data/community_platform_market_analysis.json', 'r') as f:
                self.market_data = json.load(f)
            
            # Load competitor data
            with open('/workspace/data/nextdoor_competitors_analysis.json', 'r') as f:
                self.competitors = json.load(f)
            
            # Load demographics data
            with open('/workspace/data/neighborhood_apps_usage_demographics.json', 'r') as f:
                self.demographics = json.load(f)
                
            print("✅ Market research data loaded successfully")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
    
    def create_market_size_analysis(self):
        """Create market size and growth visualization"""
        plt.figure(figsize=(14, 10))
        
        # Market size data
        market_sizes = {
            'Community Engagement Platforms': [2.5, 4.7],  # 2024, projected 2030
            'Online Community Platforms': [1.2, 3.0],      # 2024, projected 2033
            'Community Engagement Software': [27.73, 62.49] # 2024, projected 2034
        }
        
        years = ['2024', 'Projected']
        x = np.arange(len(years))
        width = 0.25
        
        # Create subplot for market size comparison
        plt.subplot(2, 2, 1)
        colors = ['#2E86AB', '#A23B72', '#F18F01']
        
        for i, (category, values) in enumerate(market_sizes.items()):
            plt.bar(x + i*width, values, width, label=category, color=colors[i], alpha=0.8)
        
        plt.xlabel('Time Period')
        plt.ylabel('Market Size (USD Billions)')
        plt.title('Community Platform Market Size Growth', fontweight='bold')
        plt.xticks(x + width, years)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        
        # Newsletter growth trends
        plt.subplot(2, 2, 2)
        newsletter_data = {
            'beehiiv Newsletters': [26911, 52809],  # 2023, 2024
            'Emails Sent (Billions)': [4.5, 15.6]   # 2023, 2024
        }
        
        years_newsletter = ['2023', '2024']
        x_news = np.arange(len(years_newsletter))
        
        # Primary y-axis for newsletters
        ax1 = plt.gca()
        color = 'tab:blue'
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Number of Newsletters', color=color)
        bars1 = ax1.bar(x_news - 0.2, newsletter_data['beehiiv Newsletters'], 0.4, 
                       label='beehiiv Newsletters', color=color, alpha=0.7)
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.set_xticks(x_news)
        ax1.set_xticklabels(years_newsletter)
        
        # Secondary y-axis for emails sent
        ax2 = ax1.twinx()
        color = 'tab:orange'
        ax2.set_ylabel('Emails Sent (Billions)', color=color)
        bars2 = ax2.bar(x_news + 0.2, newsletter_data['Emails Sent (Billions)'], 0.4,
                       label='Emails Sent (Billions)', color=color, alpha=0.7)
        ax2.tick_params(axis='y', labelcolor=color)
        
        plt.title('Newsletter Platform Growth Trends', fontweight='bold')
        
        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            ax1.annotate(f'{int(height):,}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)
        
        for bar in bars2:
            height = bar.get_height()
            ax2.annotate(f'{height}B',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)
        
        # Regional market analysis
        plt.subplot(2, 2, 3)
        regions = ['North America', 'Europe', 'Asia Pacific']
        market_share = [35, 30, 35]  # Estimated based on research
        colors_pie = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        
        plt.pie(market_share, labels=regions, autopct='%1.1f%%', colors=colors_pie, startangle=90)
        plt.title('Regional Market Distribution\n(Community Platforms)', fontweight='bold')
        
        # CAGR comparison
        plt.subplot(2, 2, 4)
        platforms = ['Community\nEngagement', 'Online\nCommunity', 'Newsletter\nPlatforms']
        cagr_rates = [16.2, 10.5, 25.0]  # Estimated CAGR rates
        colors_bar = ['#FF9999', '#66B2FF', '#99FF99']
        
        bars = plt.bar(platforms, cagr_rates, color=colors_bar, alpha=0.8)
        plt.ylabel('CAGR (%)')
        plt.title('Market Growth Rates (CAGR)', fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('/workspace/charts/market_size_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return "Market size analysis visualization created"
    
    def create_competitive_landscape(self):
        """Create comprehensive competitive analysis visualization"""
        plt.figure(figsize=(16, 12))
        
        # Competitor categories and positioning
        competitors_data = {
            'Platform': ['NextDoor', 'Facebook Groups', 'Front Porch Forum', 'Patch', 'Ring Neighbors', 
                        'OneRoof', 'Citizen', 'HamletHub', 'Quality Neighbor'],
            'Category': ['Social Network', 'Social Network', 'Newsletter/Forum', 'News Platform', 'Safety App',
                        'Building Network', 'Safety Network', 'Community News', 'Community Newsletter'],
            'Target_Scope': ['Neighborhood', 'Local Groups', 'Neighborhood', 'Hyperlocal', 'Safety',
                           'Building', 'Safety', 'Local News', 'Community'],
            'Business_Model': ['Advertising', 'Advertising', 'Donation/Ads', 'Advertising', 'Hardware Sales',
                             'Freemium', 'Freemium', 'Advertising', 'TBD'],
            'User_Base_Size': [9, 8, 2, 6, 7, 3, 5, 4, 1],  # Relative scale 1-10
            'Feature_Richness': [8, 6, 3, 7, 4, 5, 6, 5, 7],  # Relative scale 1-10
            'Market_Position': ['Leader', 'Major Player', 'Niche', 'Declining', 'Growing', 
                              'Emerging', 'Growing', 'Niche', 'New Entrant']
        }
        
        df_competitors = pd.DataFrame(competitors_data)
        
        # Create positioning matrix
        plt.subplot(2, 3, 1)
        colors_map = {'Leader': '#FF6B6B', 'Major Player': '#4ECDC4', 'Growing': '#45B7D1',
                     'Declining': '#FFA07A', 'Niche': '#98D8C8', 'Emerging': '#F7DC6F',
                     'New Entrant': '#BB8FCE'}
        
        colors = [colors_map[pos] for pos in df_competitors['Market_Position']]
        
        scatter = plt.scatter(df_competitors['User_Base_Size'], df_competitors['Feature_Richness'], 
                            c=colors, s=200, alpha=0.7, edgecolors='black', linewidth=1)
        
        # Add labels for each point
        for i, platform in enumerate(df_competitors['Platform']):
            plt.annotate(platform, 
                        (df_competitors['User_Base_Size'][i], df_competitors['Feature_Richness'][i]),
                        xytext=(5, 5), textcoords='offset points', fontsize=9, fontweight='bold')
        
        plt.xlabel('User Base Size (Relative Scale)')
        plt.ylabel('Feature Richness (Relative Scale)')
        plt.title('Competitive Positioning Matrix', fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        # Create legend for market position
        handles = [plt.scatter([], [], c=color, s=100, alpha=0.7, edgecolors='black') 
                  for color in colors_map.values()]
        labels = list(colors_map.keys())
        plt.legend(handles, labels, title='Market Position', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Business model distribution
        plt.subplot(2, 3, 2)
        business_models = df_competitors['Business_Model'].value_counts()
        colors_pie = plt.cm.Set3(np.linspace(0, 1, len(business_models)))
        
        plt.pie(business_models.values, labels=business_models.index, autopct='%1.1f%%', 
                colors=colors_pie, startangle=90)
        plt.title('Business Model Distribution', fontweight='bold')
        
        # Target scope analysis
        plt.subplot(2, 3, 3)
        target_scopes = df_competitors['Target_Scope'].value_counts()
        bars = plt.bar(range(len(target_scopes)), target_scopes.values, 
                      color=plt.cm.viridis(np.linspace(0, 1, len(target_scopes))))
        plt.xticks(range(len(target_scopes)), target_scopes.index, rotation=45)
        plt.ylabel('Number of Platforms')
        plt.title('Target Scope Distribution', fontweight='bold')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Feature comparison matrix
        plt.subplot(2, 3, 4)
        features_matrix = {
            'Platform': ['NextDoor', 'Facebook Groups', 'Front Porch Forum', 'Quality Neighbor'],
            'Social_Features': [9, 8, 4, 6],
            'Local_News': [6, 5, 8, 9],
            'Safety_Features': [7, 4, 2, 5],
            'Business_Directory': [8, 6, 3, 7],
            'Events': [7, 9, 5, 6]
        }
        
        df_features = pd.DataFrame(features_matrix)
        df_features_plot = df_features.set_index('Platform').T
        
        sns.heatmap(df_features_plot, annot=True, cmap='RdYlGn', center=5, 
                   cbar_kws={'label': 'Feature Strength (1-10)'})
        plt.title('Feature Comparison Matrix', fontweight='bold')
        plt.ylabel('Features')
        
        # Demographics and usage patterns
        plt.subplot(2, 3, 5)
        age_groups = ['18-29', '30-44', '45-60', '60+']
        usage_patterns = [65, 75, 85, 55]  # Estimated usage percentages by age group
        
        bars = plt.bar(age_groups, usage_patterns, color='skyblue', alpha=0.8)
        plt.ylabel('Usage Percentage (%)')
        plt.xlabel('Age Groups')
        plt.title('Community App Usage by Age', fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{int(height)}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Revenue model potential
        plt.subplot(2, 3, 6)
        revenue_models = ['Local Advertising', 'Premium Features', 'Sponsored Content', 
                         'Local Business Directory', 'Event Promotion']
        potential_scores = [8.5, 6.0, 7.5, 7.0, 6.5]  # Potential revenue scores
        
        bars = plt.barh(revenue_models, potential_scores, color='lightcoral', alpha=0.8)
        plt.xlabel('Revenue Potential (1-10)')
        plt.title('Revenue Model Potential\nfor Community Newsletters', fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            plt.annotate(f'{width}',
                        xy=(width, bar.get_y() + bar.get_height() / 2),
                        xytext=(3, 0),
                        textcoords="offset points",
                        ha='left', va='center')
        
        plt.tight_layout()
        plt.savefig('/workspace/charts/competitive_landscape.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return "Competitive landscape analysis created"
    
    def create_demographic_analysis(self):
        """Create demographic and usage pattern analysis"""
        plt.figure(figsize=(14, 10))
        
        # Neighborhood app usage statistics from research
        plt.subplot(2, 3, 1)
        usage_categories = ['Daily Users', 'Active Users', 'Rare/Never Users']
        usage_percentages = [41, 80, 20]
        colors = ['#FF6B6B', '#4ECDC4', '#FFD93D']
        
        bars = plt.bar(usage_categories, usage_percentages, color=colors, alpha=0.8)
        plt.ylabel('Percentage (%)')
        plt.title('Neighborhood App Usage Patterns', fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{int(height)}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontweight='bold')
        
        # Platform preferences by age
        plt.subplot(2, 3, 2)
        age_groups = ['18-29', '30-44', '45-60', '60+']
        facebook_usage = [50, 45, 40, 35]
        nextdoor_usage = [20, 25, 35, 47]
        
        x = np.arange(len(age_groups))
        width = 0.35
        
        plt.bar(x - width/2, facebook_usage, width, label='Facebook Groups', color='#4267B2', alpha=0.8)
        plt.bar(x + width/2, nextdoor_usage, width, label='NextDoor', color='#00D86A', alpha=0.8)
        
        plt.xlabel('Age Groups')
        plt.ylabel('Usage Preference (%)')
        plt.title('Platform Preference by Age Group', fontweight='bold')
        plt.xticks(x, age_groups)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Safety concerns driving usage
        plt.subplot(2, 3, 3)
        safety_concerns = ['Suspicious\nActivity', 'Package\nTheft', 'Crime\nReports', 'Other\nSafety']
        concern_percentages = [50, 37, 70, 25]
        
        bars = plt.bar(safety_concerns, concern_percentages, color='orangered', alpha=0.8)
        plt.ylabel('Percentage Reporting (%)')
        plt.title('Safety Concerns Discussed\nin Community Apps', fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{int(height)}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Actions taken based on app information
        plt.subplot(2, 3, 4)
        actions = ['Installed\nCameras', 'Increased\nLighting', 'Changed\nLocks', 'Upgraded\nFencing']
        action_percentages = [38, 34, 32, 30]
        
        bars = plt.bar(actions, action_percentages, color='steelblue', alpha=0.8)
        plt.ylabel('Percentage Taking Action (%)')
        plt.title('Security Actions Taken\nBased on App Information', fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{int(height)}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Decision-making influence
        plt.subplot(2, 3, 5)
        decisions = ['Moving\nDecisions', 'Security\nMeasures', 'Local\nBusiness\nChoices', 'Community\nParticipation']
        influence_percentages = [52, 55, 35, 60]
        
        bars = plt.bar(decisions, influence_percentages, color='mediumseagreen', alpha=0.8)
        plt.ylabel('Percentage Influenced (%)')
        plt.title('Community App Influence\non Resident Decisions', fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{int(height)}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Newsletter engagement trends
        plt.subplot(2, 3, 6)
        engagement_metrics = ['Open Rate', 'Click Rate', 'Daily Send', 'Weekly Send']
        metric_values = [37.67, 4.59, 15.82, 65.62]
        colors_metrics = ['gold', 'lightcoral', 'lightblue', 'lightgreen']
        
        bars = plt.bar(engagement_metrics, metric_values, color=colors_metrics, alpha=0.8)
        plt.ylabel('Percentage (%)')
        plt.title('Newsletter Engagement\nBenchmarks (2024)', fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('/workspace/charts/demographic_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return "Demographic analysis visualization created"
    
    def run_complete_analysis(self):
        """Run all analysis components"""
        print("🔍 Starting comprehensive market analysis for Quality Neighbor...")
        
        results = []
        results.append(self.create_market_size_analysis())
        results.append(self.create_competitive_landscape())
        results.append(self.create_demographic_analysis())
        
        print("✅ All visualizations created successfully!")
        return results

if __name__ == "__main__":
    analyzer = QualityNeighborMarketAnalysis()
    analyzer.run_complete_analysis()
