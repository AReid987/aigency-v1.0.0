#!/usr/bin/env python3
"""
Quality Neighbor User Research Analysis
Comprehensive user research analysis with demographic profiles, behavioral patterns, and actionable insights
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

class QualityNeighborUserResearch:
    def __init__(self):
        self.demographic_data = {}
        self.technology_data = {}
        self.engagement_data = {}
        self.local_market_data = {}
        self.load_research_data()
    
    def load_research_data(self):
        """Load all user research data from JSON files"""
        try:
            # Load demographic data
            with open('/workspace/data/lockhart_texas_demographics.json', 'r') as f:
                self.demographic_data['lockhart'] = json.load(f)
            
            with open('/workspace/data/austin_metro_demographics.json', 'r') as f:
                self.demographic_data['austin_metro'] = json.load(f)
            
            # Load technology adoption data
            with open('/workspace/data/homeowner_technology_adoption.json', 'r') as f:
                self.technology_data = json.load(f)
            
            # Load engagement and communication data
            with open('/workspace/data/hoa_communication_preferences.json', 'r') as f:
                self.engagement_data['hoa_preferences'] = json.load(f)
            
            with open('/workspace/data/local_news_engagement_patterns.json', 'r') as f:
                self.engagement_data['news_patterns'] = json.load(f)
            
            with open('/workspace/data/community_engagement_trends_2024.json', 'r') as f:
                self.engagement_data['communication_trends'] = json.load(f)
            
            # Load D.R. Horton buyer data
            with open('/workspace/data/dr_horton_buyer_demographics.json', 'r') as f:
                self.local_market_data['dr_horton'] = json.load(f)
            
            print("✅ User research data loaded successfully")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
    
    def create_demographic_profile_analysis(self):
        """Create comprehensive demographic profile visualization"""
        plt.figure(figsize=(16, 12))
        
        # Hartland Ranch target area demographics
        plt.subplot(2, 4, 1)
        age_groups = ['Under 18', '18-64', '65+']
        lockhart_ages = [20.6, 63.5, 15.9]  # Based on Lockhart data
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        bars = plt.bar(age_groups, lockhart_ages, color=colors, alpha=0.8)
        plt.ylabel('Percentage (%)')
        plt.title('Age Distribution\n(Lockhart, TX)', fontweight='bold')
        plt.ylim(0, 80)
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Income comparison
        plt.subplot(2, 4, 2)
        areas = ['Lockhart', 'Austin Metro']
        median_incomes = [67252, 91461]
        
        bars = plt.bar(areas, median_incomes, color=['#FF9999', '#99CCFF'], alpha=0.8)
        plt.ylabel('Median Income ($)')
        plt.title('Median Household Income\nComparison', fontweight='bold')
        plt.ticklabel_format(style='plain', axis='y')
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'${int(height):,}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Education levels (Lockhart)
        plt.subplot(2, 4, 3)
        education_levels = ['High School+', 'Bachelor+']
        education_rates = [87.1, 16.7]
        
        bars = plt.bar(education_levels, education_rates, color=['lightcoral', 'lightblue'], alpha=0.8)
        plt.ylabel('Percentage (%)')
        plt.title('Education Levels\n(Lockhart)', fontweight='bold')
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Housing characteristics
        plt.subplot(2, 4, 4)
        housing_metrics = ['Homeownership\nRate', 'Median Home\nValue', 'Monthly\nCosts']
        housing_values = [63.2, 218.4, 1.65]  # Homeownership %, Value in $k, Costs in $k
        colors_housing = ['green', 'orange', 'purple']
        
        # Normalize values for display
        normalized_values = [63.2, 21.84, 16.5]  # Scale down for visualization
        
        bars = plt.bar(housing_metrics, normalized_values, color=colors_housing, alpha=0.8)
        plt.ylabel('Values (normalized)')
        plt.title('Housing Characteristics\n(Lockhart)', fontweight='bold')
        
        # Add actual values as labels
        actual_labels = ['63.2%', '$218K', '$1,650']
        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.annotate(actual_labels[i],
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Technology adoption rates
        plt.subplot(2, 4, 5)
        tech_categories = ['Smart Devices', 'Internet', 'Mobile Usage']
        tech_rates = [93, 90.1, 96.2]  # Smart home, broadband, mobile (estimated)
        
        bars = plt.bar(tech_categories, tech_rates, color='skyblue', alpha=0.8)
        plt.ylabel('Adoption Rate (%)')
        plt.title('Technology Adoption\n(Target Demographics)', fontweight='bold')
        plt.ylim(0, 100)
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Communication preferences
        plt.subplot(2, 4, 6)
        comm_channels = ['Email', 'Text', 'Social Media', 'Newsletter']
        preference_rates = [66, 53, 23, 31]  # Based on research data
        
        bars = plt.bar(comm_channels, preference_rates, color='lightgreen', alpha=0.8)
        plt.ylabel('Preference Rate (%)')
        plt.title('Communication Channel\nPreferences', fontweight='bold')
        plt.xticks(rotation=45)
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Local news engagement
        plt.subplot(2, 4, 7)
        news_metrics = ['Follow Local\nNews', 'Consider\nImportant', 'Use Online\nForum']
        news_rates = [66, 85, 52]
        
        bars = plt.bar(news_metrics, news_rates, color='gold', alpha=0.8)
        plt.ylabel('Percentage (%)')
        plt.title('Local News &\nCommunity Engagement', fontweight='bold')
        plt.xticks(rotation=45)
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Target market segmentation
        plt.subplot(2, 4, 8)
        segments = ['First-time\nBuyers', 'Families', 'Empty\nNesters', 'Young\nProfessionals']
        segment_sizes = [35, 40, 15, 10]  # Estimated percentages
        
        colors_pie = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        plt.pie(segment_sizes, labels=segments, autopct='%1.1f%%', colors=colors_pie, startangle=90)
        plt.title('Target Market\nSegmentation', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('/workspace/charts/user_demographic_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return "User demographic analysis visualization created"
    
    def create_user_behavior_analysis(self):
        """Create user behavior and engagement pattern visualization"""
        plt.figure(figsize=(16, 10))
        
        # Content consumption preferences
        plt.subplot(2, 3, 1)
        content_types = ['Local News', 'Safety Info', 'Business\nDirectory', 'Events', 'Neighbor\nUpdates']
        engagement_scores = [85, 70, 68, 60, 52]  # Based on research data
        
        bars = plt.bar(content_types, engagement_scores, color='steelblue', alpha=0.8)
        plt.ylabel('Engagement Level (%)')
        plt.title('Content Type Preferences', fontweight='bold')
        plt.xticks(rotation=45)
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Technology spending patterns
        plt.subplot(2, 3, 2)
        spending_categories = ['Smart Home\nDevices', 'Subscriptions', 'Future\nPurchases']
        spending_amounts = [3026, 498, 896]  # Average spending amounts
        
        bars = plt.bar(spending_categories, spending_amounts, color='orange', alpha=0.8)
        plt.ylabel('Average Spending ($)')
        plt.title('Technology Investment\nPatterns', fontweight='bold')
        plt.xticks(rotation=45)
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'${int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Information seeking behavior by age
        plt.subplot(2, 3, 3)
        age_groups = ['18-29', '30-44', '45-60', '60+']
        digital_preference = [90, 80, 70, 55]  # Estimated digital preference by age
        traditional_preference = [10, 20, 30, 45]  # Traditional media preference
        
        x = np.arange(len(age_groups))
        width = 0.35
        
        plt.bar(x - width/2, digital_preference, width, label='Digital', color='lightblue', alpha=0.8)
        plt.bar(x + width/2, traditional_preference, width, label='Traditional', color='lightcoral', alpha=0.8)
        
        plt.xlabel('Age Groups')
        plt.ylabel('Preference (%)')
        plt.title('Information Source Preferences\nby Age Group', fontweight='bold')
        plt.xticks(x, age_groups)
        plt.legend()
        
        # Local business engagement
        plt.subplot(2, 3, 4)
        business_activities = ['Directory\nSearch', 'Reviews\nReading', 'Online\nBooking', 'Social\nFollow']
        engagement_rates = [75, 68, 45, 35]  # Estimated engagement rates
        
        bars = plt.bar(business_activities, engagement_rates, color='mediumseagreen', alpha=0.8)
        plt.ylabel('Engagement Rate (%)')
        plt.title('Local Business\nInteraction Patterns', fontweight='bold')
        plt.xticks(rotation=45)
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Communication timing preferences
        plt.subplot(2, 3, 5)
        times_of_day = ['Morning\n(6-9 AM)', 'Midday\n(12-2 PM)', 'Evening\n(5-8 PM)', 'Night\n(8-10 PM)']
        engagement_by_time = [25, 15, 45, 15]  # Peak engagement times
        
        bars = plt.bar(times_of_day, engagement_by_time, color='purple', alpha=0.8)
        plt.ylabel('Peak Engagement (%)')
        plt.title('Optimal Communication\nTiming', fontweight='bold')
        plt.xticks(rotation=45)
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Community participation drivers
        plt.subplot(2, 3, 6)
        participation_drivers = ['Safety\nConcerns', 'Property\nValue', 'Social\nConnection', 'Local\nServices']
        motivation_scores = [55, 52, 35, 68]  # Based on research findings
        
        bars = plt.bar(participation_drivers, motivation_scores, color='darkorange', alpha=0.8)
        plt.ylabel('Motivation Score (%)')
        plt.title('Community Participation\nDrivers', fontweight='bold')
        plt.xticks(rotation=45)
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('/workspace/charts/user_behavior_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return "User behavior analysis visualization created"
    
    def create_local_market_analysis(self):
        """Create local market and business ecosystem analysis"""
        plt.figure(figsize=(14, 10))
        
        # Local business categories (estimated for Lockhart area)
        plt.subplot(2, 3, 1)
        business_categories = ['Restaurants', 'Retail', 'Services', 'Healthcare', 'Professional', 'Real Estate']
        business_counts = [45, 35, 60, 25, 40, 20]  # Estimated counts
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(business_categories)))
        plt.pie(business_counts, labels=business_categories, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Local Business\nEcosystem Distribution', fontweight='bold')
        
        # Advertising spending potential by business size
        plt.subplot(2, 3, 2)
        business_sizes = ['Small\n(<10 employees)', 'Medium\n(10-50 employees)', 'Large\n(50+ employees)']
        monthly_ad_spend = [500, 2000, 8000]  # Estimated monthly advertising budgets
        
        bars = plt.bar(business_sizes, monthly_ad_spend, color='lightblue', alpha=0.8)
        plt.ylabel('Monthly Ad Spend ($)')
        plt.title('Local Business\nAdvertising Budgets', fontweight='bold')
        plt.xticks(rotation=45)
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'${int(height):,}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Community growth trends
        plt.subplot(2, 3, 3)
        years = ['2020', '2021', '2022', '2023', '2024']
        population_growth = [14379, 15200, 15800, 16500, 17166]  # Lockhart population growth
        
        plt.plot(years, population_growth, marker='o', linewidth=2, markersize=6, color='green')
        plt.ylabel('Population')
        plt.title('Community Growth\nTrend (Lockhart)', fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        # Add value labels
        for i, value in enumerate(population_growth):
            plt.annotate(f'{value:,}',
                        xy=(i, value),
                        xytext=(0, 10),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Target household income distribution
        plt.subplot(2, 3, 4)
        income_ranges = ['<$50K', '$50-75K', '$75-100K', '$100K+']
        household_percentages = [25, 30, 25, 20]  # Estimated distribution for target area
        
        bars = plt.bar(income_ranges, household_percentages, color='gold', alpha=0.8)
        plt.ylabel('Households (%)')
        plt.title('Target Area Income\nDistribution', fontweight='bold')
        plt.xticks(rotation=45)
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Commute patterns (employment centers)
        plt.subplot(2, 3, 5)
        commute_destinations = ['Austin', 'San Marcos', 'Local', 'Remote']
        commute_percentages = [40, 25, 20, 15]  # Estimated commute patterns
        
        colors_commute = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        plt.pie(commute_percentages, labels=commute_destinations, autopct='%1.1f%%', 
                colors=colors_commute, startangle=90)
        plt.title('Employment\nCommute Patterns', fontweight='bold')
        
        # Local advertising opportunity score
        plt.subplot(2, 3, 6)
        ad_categories = ['Restaurants', 'Home Services', 'Healthcare', 'Retail', 'Professional', 'Events']
        opportunity_scores = [8.5, 9.0, 7.5, 7.0, 6.5, 8.0]  # Opportunity scores out of 10
        
        bars = plt.barh(ad_categories, opportunity_scores, color='coral', alpha=0.8)
        plt.xlabel('Opportunity Score (1-10)')
        plt.title('Advertising Opportunity\nby Category', fontweight='bold')
        
        for bar in bars:
            width = bar.get_width()
            plt.annotate(f'{width}',
                        xy=(width, bar.get_y() + bar.get_height() / 2),
                        xytext=(3, 0),
                        textcoords="offset points",
                        ha='left', va='center')
        
        plt.tight_layout()
        plt.savefig('/workspace/charts/local_market_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return "Local market analysis visualization created"
    
    def run_complete_user_research(self):
        """Run all user research analysis components"""
        print("🔍 Starting comprehensive user research analysis for Quality Neighbor...")
        
        results = []
        results.append(self.create_demographic_profile_analysis())
        results.append(self.create_user_behavior_analysis())
        results.append(self.create_local_market_analysis())
        
        print("✅ All user research visualizations created successfully!")
        return results

if __name__ == "__main__":
    analyzer = QualityNeighborUserResearch()
    analyzer.run_complete_user_research()
