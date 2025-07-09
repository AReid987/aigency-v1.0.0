#!/usr/bin/env python3
"""
Quality Neighbor User Persona Template Generator
Creates visual persona templates for the three primary user personas
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set up colors and styles
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'sans-serif'

# Define custom colors
colors = {
    'family_primary': '#4E79A7',
    'family_secondary': '#A0CBE8',
    'elder_primary': '#F28E2B',
    'elder_secondary': '#FFBE7D',
    'leader_primary': '#59A14F',
    'leader_secondary': '#8CD17D',
    'background': '#F7F7F7',
    'text': '#333333',
    'section_bg': '#E9ECEF',
    'highlight': '#E15759',
    'positive': '#4CAF50',
    'neutral': '#FF9800',
    'negative': '#F44336'
}

def create_growing_family_persona():
    """Create persona template for Growing Family"""
    
    # Create figure and set up grid
    fig = plt.figure(figsize=(12, 15), facecolor=colors['background'])
    
    # Define grid
    grid = plt.GridSpec(10, 6, figure=fig)
    
    # Header section with name and photo
    header_ax = fig.add_subplot(grid[0:2, 0:6])
    header_ax.set_facecolor(colors['family_primary'])
    header_ax.set_xticks([])
    header_ax.set_yticks([])
    
    # Add persona name and archetype
    header_ax.text(0.03, 0.6, 'Sarah & Mike Chen', fontsize=24, fontweight='bold', color='white')
    header_ax.text(0.03, 0.2, 'YOUNG GROWING FAMILY', fontsize=16, color='white')
    
    # Add quote
    quote_ax = fig.add_subplot(grid[2, 0:6])
    quote_ax.set_facecolor(colors['family_secondary'])
    quote_ax.set_xticks([])
    quote_ax.set_yticks([])
    quote_ax.text(0.5, 0.5, '"We need a reliable, single source for local information that doesn\'t waste our time with social media drama."', 
                 fontsize=14, fontstyle='italic', ha='center', va='center', color=colors['text'])
    
    # Demographics section
    demo_ax = fig.add_subplot(grid[3:5, 0:2])
    demo_ax.set_facecolor(colors['section_bg'])
    demo_ax.set_xticks([])
    demo_ax.set_yticks([])
    
    demo_ax.text(0.5, 0.9, 'DEMOGRAPHICS', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['family_primary'])
    demo_content = [
        'Age: 32-38 years old',
        'Household: Married with 2 children (5, 8)',
        'Income: $85,000-$110,000',
        'Education: College-educated',
        'Employment: Marketing & IT',
        'Location: First-time homebuyers in Hartland Ranch'
    ]
    
    for i, item in enumerate(demo_content):
        demo_ax.text(0.1, 0.75 - i*0.12, item, fontsize=11, color=colors['text'])
    
    # Technology section
    tech_ax = fig.add_subplot(grid[3:5, 2:4])
    tech_ax.set_facecolor(colors['section_bg'])
    tech_ax.set_xticks([])
    tech_ax.set_yticks([])
    
    tech_ax.text(0.5, 0.9, 'TECHNOLOGY PROFILE', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['family_primary'])
    tech_content = [
        'Devices: Smartphones, laptops, smart TV, tablet',
        'Smart Home: Moderate adopter (doorbell, thermostat)',
        'Internet Usage: High (remote work)',
        'Social Media: Facebook, Instagram, occasional NextDoor',
        'Tech Spending: $2,500-3,500 annually'
    ]
    
    for i, item in enumerate(tech_content):
        tech_ax.text(0.1, 0.75 - i*0.12, item, fontsize=11, color=colors['text'])
    
    # Communication section
    comm_ax = fig.add_subplot(grid[3:5, 4:6])
    comm_ax.set_facecolor(colors['section_bg'])
    comm_ax.set_xticks([])
    comm_ax.set_yticks([])
    
    comm_ax.text(0.5, 0.9, 'COMMUNICATION PREFERENCES', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['family_primary'])
    comm_content = [
        'Primary Channels: Email, text messages',
        'Newsletter Receptivity: High',
        'Optimal Timing: Evenings (6-8 PM), weekends',
        'Content Format: Concise text with images',
        'Frequency: Weekly newsletters, daily for urgent'
    ]
    
    for i, item in enumerate(comm_content):
        comm_ax.text(0.1, 0.75 - i*0.12, item, fontsize=11, color=colors['text'])
    
    # Goals and motivations
    goals_ax = fig.add_subplot(grid[5, 0:3])
    goals_ax.set_facecolor(colors['section_bg'])
    goals_ax.set_xticks([])
    goals_ax.set_yticks([])
    
    goals_ax.text(0.5, 0.85, 'GOALS & MOTIVATIONS', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['family_primary'])
    goals_content = [
        '• Find safe, family-friendly activities',
        '• Stay informed about school events',
        '• Discover reliable local service providers',
        '• Build connections with other families',
        '• Maintain home value'
    ]
    
    for i, item in enumerate(goals_content):
        goals_ax.text(0.1, 0.65 - i*0.12, item, fontsize=11, color=colors['text'])
    
    # Pain points
    pain_ax = fig.add_subplot(grid[5, 3:6])
    pain_ax.set_facecolor(colors['section_bg'])
    pain_ax.set_xticks([])
    pain_ax.set_yticks([])
    
    pain_ax.text(0.5, 0.85, 'PAIN POINTS & FRUSTRATIONS', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['family_primary'])
    pain_content = [
        '• Information scattered across multiple platforms',
        '• Social media groups full of drama and noise',
        '• Difficulty finding trustworthy recommendations',
        '• Limited time to search through content',
        '• Too many communication apps to manage'
    ]
    
    for i, item in enumerate(pain_content):
        pain_ax.text(0.1, 0.65 - i*0.12, item, fontsize=11, color=colors['text'])
    
    # Behavioral patterns
    behavior_ax = fig.add_subplot(grid[6:8, 0:3])
    behavior_ax.set_facecolor(colors['section_bg'])
    behavior_ax.set_xticks([])
    behavior_ax.set_yticks([])
    
    behavior_ax.text(0.5, 0.9, 'BEHAVIORAL PATTERNS', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['family_primary'])
    behavior_content = [
        'Usage Frequency: Daily quick checks, weekly review',
        'Prime Time: Evenings (6-8 PM), weekend mornings',
        'Content Priorities: School updates, activities, safety',
        'Information Seeking: Facebook groups, Google',
        'Decision Making: Reviews-driven, recommendations',
        'Content Creation: Limited due to time constraints'
    ]
    
    for i, item in enumerate(behavior_content):
        behavior_ax.text(0.1, 0.8 - i*0.1, item, fontsize=11, color=colors['text'])
    
    # Quality Neighbor fit
    fit_ax = fig.add_subplot(grid[6:8, 3:6])
    fit_ax.set_facecolor(colors['section_bg'])
    fit_ax.set_xticks([])
    fit_ax.set_yticks([])
    
    fit_ax.text(0.5, 0.9, 'QUALITY NEIGHBOR FIT', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['family_primary'])
    fit_content = [
        'Value Proposition: One trusted source for family information',
        'Critical Features: Mobile weekly digest, verified directory',
        'Engagement Triggers: School calendar, family events',
        'Adoption Barriers: Time investment, email overload',
        'Success Metrics: Open rate (50%), local business engagement',
        'Engagement Likelihood: HIGH'
    ]
    
    for i, item in enumerate(fit_content):
        fit_ax.text(0.1, 0.8 - i*0.1, item, fontsize=11, color=colors['text'])
    
    # Key quotes
    quotes_ax = fig.add_subplot(grid[8:10, 0:6])
    quotes_ax.set_facecolor(colors['family_secondary'])
    quotes_ax.set_xticks([])
    quotes_ax.set_yticks([])
    
    quotes_ax.text(0.5, 0.9, 'KEY INSIGHTS', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['family_primary'])
    quotes_content = [
        '"Between work and the kids, we don\'t have time to scroll through endless social media feeds."',
        '"We need reliable information about local family activities and safe places for our kids."',
        '"I want updates from my kids\' school, neighborhood safety alerts, and local business info all in one place."',
        '"We\'d pay for a service that saves us time and connects us with trustworthy local resources."'
    ]
    
    for i, item in enumerate(quotes_content):
        quotes_ax.text(0.5, 0.75 - i*0.15, item, fontsize=11, fontstyle='italic', ha='center', va='center', color=colors['text'])
    
    # Save the figure
    plt.subplots_adjust(hspace=0.3, wspace=0.3)
    plt.savefig('/workspace/charts/growing_family_persona.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return "Growing Family persona template created"

def create_community_elder_persona():
    """Create persona template for Community Elder"""
    
    # Create figure and set up grid
    fig = plt.figure(figsize=(12, 15), facecolor=colors['background'])
    
    # Define grid
    grid = plt.GridSpec(10, 6, figure=fig)
    
    # Header section with name and photo
    header_ax = fig.add_subplot(grid[0:2, 0:6])
    header_ax.set_facecolor(colors['elder_primary'])
    header_ax.set_xticks([])
    header_ax.set_yticks([])
    
    # Add persona name and archetype
    header_ax.text(0.03, 0.6, 'Robert & Linda Martinez', fontsize=24, fontweight='bold', color='white')
    header_ax.text(0.03, 0.2, 'COMMUNITY ELDER', fontsize=16, color='white')
    
    # Add quote
    quote_ax = fig.add_subplot(grid[2, 0:6])
    quote_ax.set_facecolor(colors['elder_secondary'])
    quote_ax.set_xticks([])
    quote_ax.set_yticks([])
    quote_ax.text(0.5, 0.5, '"We value being connected to our community through reliable, traditional channels. We prefer quality information over quantity."', 
                 fontsize=14, fontstyle='italic', ha='center', va='center', color=colors['text'])
    
    # Demographics section
    demo_ax = fig.add_subplot(grid[3:5, 0:2])
    demo_ax.set_facecolor(colors['section_bg'])
    demo_ax.set_xticks([])
    demo_ax.set_yticks([])
    
    demo_ax.text(0.5, 0.9, 'DEMOGRAPHICS', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['elder_primary'])
    demo_content = [
        'Age: 55-62 years old',
        'Household: Married, adult children moved out',
        'Income: $90,000-$130,000',
        'Education: High school + some college/trade',
        'Employment: Small business owner, Healthcare admin',
        'Location: Downsizing to Hartland Ranch'
    ]
    
    for i, item in enumerate(demo_content):
        demo_ax.text(0.1, 0.75 - i*0.12, item, fontsize=11, color=colors['text'])
    
    # Technology section
    tech_ax = fig.add_subplot(grid[3:5, 2:4])
    tech_ax.set_facecolor(colors['section_bg'])
    tech_ax.set_xticks([])
    tech_ax.set_yticks([])
    
    tech_ax.text(0.5, 0.9, 'TECHNOLOGY PROFILE', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['elder_primary'])
    tech_content = [
        'Devices: Smartphones, desktop computer, smart TV',
        'Smart Home: Basic adoption (security, thermostat)',
        'Internet Usage: Moderate',
        'Social Media: Facebook primary, some NextDoor',
        'Tech Spending: $1,500-2,000 annually'
    ]
    
    for i, item in enumerate(tech_content):
        tech_ax.text(0.1, 0.75 - i*0.12, item, fontsize=11, color=colors['text'])
    
    # Communication section
    comm_ax = fig.add_subplot(grid[3:5, 4:6])
    comm_ax.set_facecolor(colors['section_bg'])
    comm_ax.set_xticks([])
    comm_ax.set_yticks([])
    
    comm_ax.text(0.5, 0.9, 'COMMUNICATION PREFERENCES', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['elder_primary'])
    comm_content = [
        'Primary Channels: Email, traditional mail',
        'Newsletter Receptivity: Very high',
        'Optimal Timing: Mornings (7-9 AM), afternoons',
        'Content Format: Detailed text, traditional layout',
        'Frequency: Weekly newsletters, monthly details'
    ]
    
    for i, item in enumerate(comm_content):
        comm_ax.text(0.1, 0.75 - i*0.12, item, fontsize=11, color=colors['text'])
    
    # Goals and motivations
    goals_ax = fig.add_subplot(grid[5, 0:3])
    goals_ax.set_facecolor(colors['section_bg'])
    goals_ax.set_xticks([])
    goals_ax.set_yticks([])
    
    goals_ax.text(0.5, 0.85, 'GOALS & MOTIVATIONS', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['elder_primary'])
    goals_content = [
        '• Stay informed about community governance',
        '• Discover and support local businesses',
        '• Build social connections in new neighborhood',
        '• Access reliable health and home services',
        '• Participate in community events'
    ]
    
    for i, item in enumerate(goals_content):
        goals_ax.text(0.1, 0.65 - i*0.12, item, fontsize=11, color=colors['text'])
    
    # Pain points
    pain_ax = fig.add_subplot(grid[5, 3:6])
    pain_ax.set_facecolor(colors['section_bg'])
    pain_ax.set_xticks([])
    pain_ax.set_yticks([])
    
    pain_ax.text(0.5, 0.85, 'PAIN POINTS & FRUSTRATIONS', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['elder_primary'])
    pain_content = [
        '• Modern platforms too complex and changing',
        '• Information overload and too much noise',
        '• Difficulty distinguishing facts from opinions',
        '• Too many different communication methods',
        '• Privacy concerns with social platforms'
    ]
    
    for i, item in enumerate(pain_content):
        pain_ax.text(0.1, 0.65 - i*0.12, item, fontsize=11, color=colors['text'])
    
    # Behavioral patterns
    behavior_ax = fig.add_subplot(grid[6:8, 0:3])
    behavior_ax.set_facecolor(colors['section_bg'])
    behavior_ax.set_xticks([])
    behavior_ax.set_yticks([])
    
    behavior_ax.text(0.5, 0.9, 'BEHAVIORAL PATTERNS', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['elder_primary'])
    behavior_content = [
        'Usage Frequency: Daily morning checks, afternoon reading',
        'Prime Time: Mornings (7-9 AM), afternoons (2-4 PM)',
        'Content Priorities: Governance, events, business news',
        'Information Seeking: Traditional sources, word of mouth',
        'Decision Making: Relationship-driven, values reputation',
        'Content Creation: Willing to share community knowledge'
    ]
    
    for i, item in enumerate(behavior_content):
        behavior_ax.text(0.1, 0.8 - i*0.1, item, fontsize=11, color=colors['text'])
    
    # Quality Neighbor fit
    fit_ax = fig.add_subplot(grid[6:8, 3:6])
    fit_ax.set_facecolor(colors['section_bg'])
    fit_ax.set_xticks([])
    fit_ax.set_yticks([])
    
    fit_ax.text(0.5, 0.9, 'QUALITY NEIGHBOR FIT', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['elder_primary'])
    fit_content = [
        'Value Proposition: Reliable information in familiar format',
        'Critical Features: Traditional layout, print-friendly version',
        'Engagement Triggers: Local business spotlights, history',
        'Adoption Barriers: Learning new platform, cost concerns',
        'Success Metrics: Content contribution, business referrals',
        'Engagement Likelihood: VERY HIGH'
    ]
    
    for i, item in enumerate(fit_content):
        fit_ax.text(0.1, 0.8 - i*0.1, item, fontsize=11, color=colors['text'])
    
    # Key quotes
    quotes_ax = fig.add_subplot(grid[8:10, 0:6])
    quotes_ax.set_facecolor(colors['elder_secondary'])
    quotes_ax.set_xticks([])
    quotes_ax.set_yticks([])
    
    quotes_ax.text(0.5, 0.9, 'KEY INSIGHTS', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['elder_primary'])
    quotes_content = [
        '"Modern social media platforms are too complicated and constantly changing."',
        '"We want to support local businesses but need a reliable way to discover them."',
        '"I prefer something I can print out and read at my leisure with my morning coffee."',
        '"We have valuable knowledge about our previous community that we\'d love to share."'
    ]
    
    for i, item in enumerate(quotes_content):
        quotes_ax.text(0.5, 0.75 - i*0.15, item, fontsize=11, fontstyle='italic', ha='center', va='center', color=colors['text'])
    
    # Save the figure
    plt.subplots_adjust(hspace=0.3, wspace=0.3)
    plt.savefig('/workspace/charts/community_elder_persona.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return "Community Elder persona template created"

def create_community_leader_persona():
    """Create persona template for Community Leader"""
    
    # Create figure and set up grid
    fig = plt.figure(figsize=(12, 15), facecolor=colors['background'])
    
    # Define grid
    grid = plt.GridSpec(10, 6, figure=fig)
    
    # Header section with name and photo
    header_ax = fig.add_subplot(grid[0:2, 0:6])
    header_ax.set_facecolor(colors['leader_primary'])
    header_ax.set_xticks([])
    header_ax.set_yticks([])
    
    # Add persona name and archetype
    header_ax.text(0.03, 0.6, 'David Kim', fontsize=24, fontweight='bold', color='white')
    header_ax.text(0.03, 0.2, 'COMMUNITY LEADER', fontsize=16, color='white')
    
    # Add quote
    quote_ax = fig.add_subplot(grid[2, 0:6])
    quote_ax.set_facecolor(colors['leader_secondary'])
    quote_ax.set_xticks([])
    quote_ax.set_yticks([])
    quote_ax.text(0.5, 0.5, '"As someone deeply involved in our community\'s development, I need comprehensive tools to stay informed and connect neighbors with resources."', 
                 fontsize=14, fontstyle='italic', ha='center', va='center', color=colors['text'])
    
    # Demographics section
    demo_ax = fig.add_subplot(grid[3:5, 0:2])
    demo_ax.set_facecolor(colors['section_bg'])
    demo_ax.set_xticks([])
    demo_ax.set_yticks([])
    
    demo_ax.text(0.5, 0.9, 'DEMOGRAPHICS', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['leader_primary'])
    demo_content = [
        'Age: 42-48 years old',
        'Household: Married with 1 teenage child',
        'Income: $120,000-$150,000',
        'Education: Advanced degree (MBA)',
        'Employment: Senior Manager at tech company',
        'Location: Move-up buyer in Hartland Ranch'
    ]
    
    for i, item in enumerate(demo_content):
        demo_ax.text(0.1, 0.75 - i*0.12, item, fontsize=11, color=colors['text'])
    
    # Technology section
    tech_ax = fig.add_subplot(grid[3:5, 2:4])
    tech_ax.set_facecolor(colors['section_bg'])
    tech_ax.set_xticks([])
    tech_ax.set_yticks([])
    
    tech_ax.text(0.5, 0.9, 'TECHNOLOGY PROFILE', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['leader_primary'])
    tech_content = [
        'Devices: Multiple smartphones, laptops, smart home',
        'Smart Home: Very high adopter, early technology adopter',
        'Internet Usage: Expert level, multiple platforms',
        'Social Media: LinkedIn, Twitter, Facebook, NextDoor',
        'Tech Spending: $5,000+ annually'
    ]
    
    for i, item in enumerate(tech_content):
        tech_ax.text(0.1, 0.75 - i*0.12, item, fontsize=11, color=colors['text'])
    
    # Communication section
    comm_ax = fig.add_subplot(grid[3:5, 4:6])
    comm_ax.set_facecolor(colors['section_bg'])
    comm_ax.set_xticks([])
    comm_ax.set_yticks([])
    
    comm_ax.text(0.5, 0.9, 'COMMUNICATION PREFERENCES', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['leader_primary'])
    comm_content = [
        'Primary Channels: Multiple (email, text, apps)',
        'Newsletter Receptivity: Very high, comprehensive',
        'Optimal Timing: Early mornings (6-7 AM), commute',
        'Content Format: Data-rich with detailed links',
        'Frequency: Daily for breaking news, weekly details'
    ]
    
    for i, item in enumerate(comm_content):
        comm_ax.text(0.1, 0.75 - i*0.12, item, fontsize=11, color=colors['text'])
    
    # Goals and motivations
    goals_ax = fig.add_subplot(grid[5, 0:3])
    goals_ax.set_facecolor(colors['section_bg'])
    goals_ax.set_xticks([])
    goals_ax.set_yticks([])
    
    goals_ax.text(0.5, 0.85, 'GOALS & MOTIVATIONS', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['leader_primary'])
    goals_content = [
        '• Drive community development and improvements',
        '• Establish efficient communication channels',
        '• Connect neighbors with reliable resources',
        '• Enhance property values through initiatives',
        '• Implement technology solutions for challenges'
    ]
    
    for i, item in enumerate(goals_content):
        goals_ax.text(0.1, 0.65 - i*0.12, item, fontsize=11, color=colors['text'])
    
    # Pain points
    pain_ax = fig.add_subplot(grid[5, 3:6])
    pain_ax.set_facecolor(colors['section_bg'])
    pain_ax.set_xticks([])
    pain_ax.set_yticks([])
    
    pain_ax.text(0.5, 0.85, 'PAIN POINTS & FRUSTRATIONS', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['leader_primary'])
    pain_content = [
        '• Critical information lost across multiple platforms',
        '• Time-consuming to track community resources',
        '• Community leadership requires significant time',
        '• Existing tools lack analytics and management',
        '• Difficulty driving consistent communication'
    ]
    
    for i, item in enumerate(pain_content):
        pain_ax.text(0.1, 0.65 - i*0.12, item, fontsize=11, color=colors['text'])
    
    # Behavioral patterns
    behavior_ax = fig.add_subplot(grid[6:8, 0:3])
    behavior_ax.set_facecolor(colors['section_bg'])
    behavior_ax.set_xticks([])
    behavior_ax.set_yticks([])
    
    behavior_ax.text(0.5, 0.9, 'BEHAVIORAL PATTERNS', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['leader_primary'])
    behavior_content = [
        'Usage Frequency: Multiple daily checks, weekly analysis',
        'Prime Time: Early mornings (6-7 AM), commute',
        'Content Priorities: Governance, property, development',
        'Information Seeking: Comprehensive research, data-driven',
        'Decision Making: ROI-focused, values quality and innovation',
        'Content Creation: Active content creator and moderator'
    ]
    
    for i, item in enumerate(behavior_content):
        behavior_ax.text(0.1, 0.8 - i*0.1, item, fontsize=11, color=colors['text'])
    
    # Quality Neighbor fit
    fit_ax = fig.add_subplot(grid[6:8, 3:6])
    fit_ax.set_facecolor(colors['section_bg'])
    fit_ax.set_xticks([])
    fit_ax.set_yticks([])
    
    fit_ax.text(0.5, 0.9, 'QUALITY NEIGHBOR FIT', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['leader_primary'])
    fit_content = [
        'Value Proposition: Comprehensive management platform',
        'Critical Features: Analytics dashboard, governance tools',
        'Engagement Triggers: Data visualization, efficiency tools',
        'Adoption Barriers: Community-wide adoption concerns',
        'Success Metrics: Platform advocacy, feature utilization',
        'Engagement Likelihood: VERY HIGH'
    ]
    
    for i, item in enumerate(fit_content):
        fit_ax.text(0.1, 0.8 - i*0.1, item, fontsize=11, color=colors['text'])
    
    # Key quotes
    quotes_ax = fig.add_subplot(grid[8:10, 0:6])
    quotes_ax.set_facecolor(colors['leader_secondary'])
    quotes_ax.set_xticks([])
    quotes_ax.set_yticks([])
    
    quotes_ax.text(0.5, 0.9, 'KEY INSIGHTS', fontsize=14, fontweight='bold', ha='center', va='center', color=colors['leader_primary'])
    quotes_content = [
        '"I need a centralized platform where I can track and manage community issues efficiently."',
        '"Data-driven insights would help us make better decisions about community investments."',
        '"The challenge is getting consistent community adoption of any new communication system."',
        '"I want advanced features for governance, but with an easy interface for all residents."'
    ]
    
    for i, item in enumerate(quotes_content):
        quotes_ax.text(0.5, 0.75 - i*0.15, item, fontsize=11, fontstyle='italic', ha='center', va='center', color=colors['text'])
    
    # Save the figure
    plt.subplots_adjust(hspace=0.3, wspace=0.3)
    plt.savefig('/workspace/charts/community_leader_persona.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return "Community Leader persona template created"

# Create all persona templates
def create_all_personas():
    print("Creating persona templates...")
    create_growing_family_persona()
    create_community_elder_persona()
    create_community_leader_persona()
    print("All persona templates created successfully!")

if __name__ == "__main__":
    create_all_personas()