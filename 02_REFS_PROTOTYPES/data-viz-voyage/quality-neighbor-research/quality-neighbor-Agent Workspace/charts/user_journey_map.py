#!/usr/bin/env python3
"""
Quality Neighbor User Journey Map Generator
Creates visual journey maps for the three primary user personas
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

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
    'highlight': '#E15759',
    'positive': '#4CAF50',
    'neutral': '#FF9800',
    'negative': '#F44336'
}

# Create journey maps for each persona
def create_growing_family_journey():
    """Create journey map for Growing Family persona"""
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(colors['background'])
    ax.set_facecolor(colors['background'])
    
    # Set up the journey stages
    stages = ['Awareness', 'Consideration', 'Onboarding', 'Regular Usage', 'Advocacy']
    y_categories = ['Touchpoints', 'Actions', 'Emotions', 'Pain Points', 'Opportunities']
    
    # Create a grid
    ax.set_xlim(0, len(stages))
    ax.set_ylim(0, len(y_categories))
    
    # Add stage headers
    for i, stage in enumerate(stages):
        ax.text(i + 0.5, len(y_categories) + 0.1, stage, 
                ha='center', va='bottom', fontsize=14, fontweight='bold', color=colors['family_primary'])
        # Add vertical separator lines
        if i > 0:
            ax.axvline(x=i, color='gray', linestyle='-', alpha=0.3)
    
    # Add row headers
    for i, category in enumerate(y_categories):
        ax.text(-0.1, len(y_categories) - i - 0.5, category, 
                ha='right', va='center', fontsize=12, fontweight='bold', color=colors['text'])
        # Add horizontal separator lines
        if i > 0:
            ax.axhline(y=len(y_categories) - i, color='gray', linestyle='-', alpha=0.3)
    
    # Define content for each cell in the journey map
    journey_content = {
        # Awareness stage
        (0, 0): {  # Touchpoints
            'content': 'School communications\nFacebook group posts\nHOA welcome package\nLocal business promotions',
            'color': colors['family_secondary']
        },
        (0, 1): {  # Actions
            'content': 'Notices multiple mentions\nBriefly investigates website\nAsks neighbors about experience\nConsiders benefits vs. time',
            'color': colors['family_secondary']
        },
        (0, 2): {  # Emotions
            'content': 'Curious but cautious\nMildly interested\nSlightly overwhelmed\nHopeful about solution',
            'color': colors['neutral']
        },
        (0, 3): {  # Pain Points
            'content': 'Too many platforms already\nUncertainty about value\nTime constraints\nEmail overload concerns',
            'color': colors['negative']
        },
        (0, 4): {  # Opportunities
            'content': 'Highlight time-saving benefits\nShowcase family-focused features\nProvide quick-start guide\nDemonstrate consolidation value',
            'color': colors['positive']
        },
        
        # Consideration stage
        (1, 0): {  # Touchpoints
            'content': 'Platform website comparison\nTestimonials from families\nDemo newsletter\nReferral from trusted neighbor',
            'color': colors['family_secondary']
        },
        (1, 1): {  # Actions
            'content': 'Reviews family benefits\nCompares with current sources\nEvaluates time commitment\nDiscusses with spouse',
            'color': colors['family_secondary']
        },
        (1, 2): {  # Emotions
            'content': 'Increasingly interested\nCalculating value vs. effort\nHopeful about reducing fatigue\nPractical about decision',
            'color': colors['neutral']
        },
        (1, 3): {  # Pain Points
            'content': 'Concerns about another account\nUncertainty about relevance\nQuestions about data usage\nUnclear integrations',
            'color': colors['negative']
        },
        (1, 4): {  # Opportunities
            'content': 'Offer similar family testimonials\nProvide one-click signup\nEmphasize time-saving content\nHighlight school integration',
            'color': colors['positive']
        },
        
        # Onboarding stage
        (2, 0): {  # Touchpoints
            'content': 'Welcome email guide\nProfile setup process\nContent preference selection\nMobile app download',
            'color': colors['family_secondary']
        },
        (2, 1): {  # Actions
            'content': 'Creates family account\nSelects content categories\nSets notification preferences\nConnects school calendar',
            'color': colors['family_secondary']
        },
        (2, 2): {  # Emotions
            'content': 'Hopeful but impatient\nDetermined to complete quickly\nInterested in immediate value\nTentatively committed',
            'color': colors['neutral']
        },
        (2, 3): {  # Pain Points
            'content': 'Limited time for setup\nPreference settings too detailed\nUnclear immediate benefits\nTechnical issues with mobile',
            'color': colors['negative']
        },
        (2, 4): {  # Opportunities
            'content': 'Implement progressive profiling\nProvide "quick setup" option\nDeliver immediate value\nOffer calendar integration help',
            'color': colors['positive']
        },
        
        # Regular Usage stage
        (3, 0): {  # Touchpoints
            'content': 'Weekly newsletter (primary)\nEmergency/safety alerts\nLocal business recommendations\nEvent reminders and updates',
            'color': colors['family_secondary']
        },
        (3, 1): {  # Actions
            'content': 'Reads during evening downtime\nSaves events to family calendar\nClicks through to local businesses\nShares useful information',
            'color': colors['family_secondary']
        },
        (3, 2): {  # Emotions
            'content': 'Satisfied with format\nRelieved to have consolidation\nAppreciative of curation\nGradually more engaged',
            'color': colors['positive']
        },
        (3, 3): {  # Pain Points
            'content': 'Occasional irrelevant content\nInconsistent delivery timing\nForgotten password issues\nFeature discovery challenges',
            'color': colors['negative']
        },
        (3, 4): {  # Opportunities
            'content': 'Implement personalization\nCreate consistent schedule\nOffer passwordless login\nHighlight features progressively',
            'color': colors['positive']
        },
        
        # Advocacy stage
        (4, 0): {  # Touchpoints
            'content': 'Referral program notification\nContribution opportunities\nFeedback requests\nSocial sharing options',
            'color': colors['family_secondary']
        },
        (4, 1): {  # Actions
            'content': 'Recommends to school parents\nShares business recommendations\nSubmits family event information\nProvides feedback when asked',
            'color': colors['family_secondary']
        },
        (4, 2): {  # Emotions
            'content': 'Confident in platform value\nProud to share useful resource\nInvested in improvement\nLoyal to trusted source',
            'color': colors['positive']
        },
        (4, 3): {  # Pain Points
            'content': 'Hesitant to actively promote\nLimited time for contribution\nUnsure how to maximize benefits\nConcerned about over-sharing',
            'color': colors['negative']
        },
        (4, 4): {  # Opportunities
            'content': 'Create frictionless referrals\nImplement micro-contributions\nProvide recognition for sharing\nDevelop super-user program',
            'color': colors['positive']
        },
    }
    
    # Add content to each cell
    for (x, y), data in journey_content.items():
        content = data['content']
        color = data['color']
        
        rect = patches.Rectangle((x, len(y_categories) - y - 1), 1, 1, 
                               linewidth=1, edgecolor='gray', facecolor=color, alpha=0.3)
        ax.add_patch(rect)
        
        ax.text(x + 0.5, len(y_categories) - y - 0.5, content, 
                ha='center', va='center', fontsize=9, color=colors['text'],
                linespacing=1.3)
    
    # Add user journey line
    # Define emotion scores for each stage (1-5 scale, 5 being most positive)
    emotion_scores = [3.0, 3.5, 3.2, 4.0, 4.5]
    emotion_y_positions = [len(y_categories) - 2.5 - (score-1)/4 for score in emotion_scores]
    
    # Plot the emotion line
    for i in range(len(stages)-1):
        ax.plot([i+0.5, i+1.5], [emotion_y_positions[i], emotion_y_positions[i+1]], 
                color=colors['family_primary'], linewidth=3, marker='o', markersize=8)
    
    # Add persona information
    persona_info = "JOURNEY MAP: GROWING FAMILY\nSarah & Mike Chen (32-38 years old)\n\"We need a reliable source for local information that doesn't waste our time.\""
    fig.text(0.02, 0.02, persona_info, fontsize=12, fontweight='bold', color=colors['family_primary'])
    
    # Remove ticks and spines
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Add title
    plt.suptitle('User Journey Map: Growing Family', fontsize=16, fontweight='bold', color=colors['family_primary'], y=0.98)
    
    # Save the figure
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('/workspace/charts/growing_family_journey_map.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return "Growing Family journey map created"

def create_community_elder_journey():
    """Create journey map for Community Elder persona"""
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(colors['background'])
    ax.set_facecolor(colors['background'])
    
    # Set up the journey stages
    stages = ['Awareness', 'Consideration', 'Onboarding', 'Regular Usage', 'Advocacy']
    y_categories = ['Touchpoints', 'Actions', 'Emotions', 'Pain Points', 'Opportunities']
    
    # Create a grid
    ax.set_xlim(0, len(stages))
    ax.set_ylim(0, len(y_categories))
    
    # Add stage headers
    for i, stage in enumerate(stages):
        ax.text(i + 0.5, len(y_categories) + 0.1, stage, 
                ha='center', va='bottom', fontsize=14, fontweight='bold', color=colors['elder_primary'])
        # Add vertical separator lines
        if i > 0:
            ax.axvline(x=i, color='gray', linestyle='-', alpha=0.3)
    
    # Add row headers
    for i, category in enumerate(y_categories):
        ax.text(-0.1, len(y_categories) - i - 0.5, category, 
                ha='right', va='center', fontsize=12, fontweight='bold', color=colors['text'])
        # Add horizontal separator lines
        if i > 0:
            ax.axhline(y=len(y_categories) - i, color='gray', linestyle='-', alpha=0.3)
    
    # Define content for each cell in the journey map
    journey_content = {
        # Awareness stage
        (0, 0): {  # Touchpoints
            'content': 'Community bulletin boards\nHOA newsletter mentions\nLocal business recommendations\nNeighbor in-person interactions',
            'color': colors['elder_secondary']
        },
        (0, 1): {  # Actions
            'content': 'Notes mentions from trusted sources\nDiscusses with spouse and neighbors\nResearches platform background\nConsiders benefits for new community',
            'color': colors['elder_secondary']
        },
        (0, 2): {  # Emotions
            'content': 'Initially skeptical but interested\nCautious about new technology\nHopeful about community connections\nDeliberate in decision-making',
            'color': colors['neutral']
        },
        (0, 3): {  # Pain Points
            'content': 'Wariness of new digital platforms\nConcerns about technical complexity\nPrivacy and security hesitations\nPreference for traditional methods',
            'color': colors['negative']
        },
        (0, 4): {  # Opportunities
            'content': 'Emphasize traditional format\nHighlight print-friendly capabilities\nShowcase privacy-first approach\nProvide comparison to familiar methods',
            'color': colors['positive']
        },
        
        # Consideration stage
        (1, 0): {  # Touchpoints
            'content': 'Printed platform overview\nDemonstration at community center\nConversations with current users\nSample newsletter (print and digital)',
            'color': colors['elder_secondary']
        },
        (1, 1): {  # Actions
            'content': 'Attends in-person demonstration\nReviews print materials thoroughly\nAsks detailed questions\nConsults with tech-savvy friends',
            'color': colors['elder_secondary']
        },
        (1, 2): {  # Emotions
            'content': 'Warming to potential benefits\nAppreciative of familiar options\nConcerned about learning curve\nDeliberate in evaluation',
            'color': colors['neutral']
        },
        (1, 3): {  # Pain Points
            'content': 'Technical vocabulary barriers\nUncertainty about ongoing costs\nConcerns about required tech skills\nQuestions about content reliability',
            'color': colors['negative']
        },
        (1, 4): {  # Opportunities
            'content': 'Offer in-person signup assistance\nProvide clear, jargon-free explanations\nEmphasize free resident access\nDemonstrate simple interface options',
            'color': colors['positive']
        },
        
        # Onboarding stage
        (2, 0): {  # Touchpoints
            'content': 'Welcome packet (print and digital)\nGuided setup process\nHelp documentation in multiple formats\nSupport contact information',
            'color': colors['elder_secondary']
        },
        (2, 1): {  # Actions
            'content': 'Creates account with assistance\nCompletes comprehensive profile\nSets content and delivery preferences\nExplores features methodically',
            'color': colors['elder_secondary']
        },
        (2, 2): {  # Emotions
            'content': 'Determined to master new system\nProud of embracing technology\nConcerned about "doing it right"\nSatisfied with completion',
            'color': colors['neutral']
        },
        (2, 3): {  # Pain Points
            'content': 'Technical terminology confusion\nMulti-step processes challenging\nPassword management difficulties\nFont size and readability issues',
            'color': colors['negative']
        },
        (2, 4): {  # Opportunities
            'content': 'Provide large-text interfaces\nImplement simplified setup process\nOffer phone/in-person assistance\nCreate printed quick reference guide',
            'color': colors['positive']
        },
        
        # Regular Usage stage
        (3, 0): {  # Touchpoints
            'content': 'Regular newsletter (print/digital)\nCommunity event notifications\nLocal business directory\nGovernance and HOA updates',
            'color': colors['elder_secondary']
        },
        (3, 1): {  # Actions
            'content': 'Reads entire newsletter thoroughly\nRegularly consults business directory\nAttends community events\nMaintains predictable usage pattern',
            'color': colors['elder_secondary']
        },
        (3, 2): {  # Emotions
            'content': 'Comfortable with routine\nAppreciative of information\nLoyal to reliable source\nIncreasingly confident with technology',
            'color': colors['positive']
        },
        (3, 3): {  # Pain Points
            'content': 'Frustration with platform changes\nDifficulty with advanced features\nOccasional technical glitches\nPrint vs. digital inconsistencies',
            'color': colors['negative']
        },
        (3, 4): {  # Opportunities
            'content': 'Maintain consistent interface\nProvide advance notice of changes\nEnsure print-digital content parity\nOffer progressive feature introduction',
            'color': colors['positive']
        },
        
        # Advocacy stage
        (4, 0): {  # Touchpoints
            'content': 'Community meetings and events\nTestimonial opportunities\nContent contribution invitations\nVolunteer engagement options',
            'color': colors['elder_secondary']
        },
        (4, 1): {  # Actions
            'content': 'Promotes to friends and neighbors\nContributes community knowledge\nAttends and supports related events\nProvides detailed feedback',
            'color': colors['elder_secondary']
        },
        (4, 2): {  # Emotions
            'content': 'Proud of technology adoption\nInvested in community success\nProtective of platform quality\nEnthusiastic ambassador',
            'color': colors['positive']
        },
        (4, 3): {  # Pain Points
            'content': 'Concern about usability changes\nFrustration with unaddressed feedback\nDifficulty explaining to peers\nLimitations in contribution options',
            'color': colors['negative']
        },
        (4, 4): {  # Opportunities
            'content': 'Create recognition for long-term users\nImplement dedicated feedback channels\nDevelop "community historian" role\nProvide ambassador tools',
            'color': colors['positive']
        },
    }
    
    # Add content to each cell
    for (x, y), data in journey_content.items():
        content = data['content']
        color = data['color']
        
        rect = patches.Rectangle((x, len(y_categories) - y - 1), 1, 1, 
                               linewidth=1, edgecolor='gray', facecolor=color, alpha=0.3)
        ax.add_patch(rect)
        
        ax.text(x + 0.5, len(y_categories) - y - 0.5, content, 
                ha='center', va='center', fontsize=9, color=colors['text'],
                linespacing=1.3)
    
    # Add user journey line
    # Define emotion scores for each stage (1-5 scale, 5 being most positive)
    emotion_scores = [2.5, 3.0, 3.5, 4.0, 4.8]
    emotion_y_positions = [len(y_categories) - 2.5 - (score-1)/4 for score in emotion_scores]
    
    # Plot the emotion line
    for i in range(len(stages)-1):
        ax.plot([i+0.5, i+1.5], [emotion_y_positions[i], emotion_y_positions[i+1]], 
                color=colors['elder_primary'], linewidth=3, marker='o', markersize=8)
    
    # Add persona information
    persona_info = "JOURNEY MAP: COMMUNITY ELDER\nRobert & Linda Martinez (55-62 years old)\n\"We value reliable, traditional channels for connecting with our community.\""
    fig.text(0.02, 0.02, persona_info, fontsize=12, fontweight='bold', color=colors['elder_primary'])
    
    # Remove ticks and spines
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Add title
    plt.suptitle('User Journey Map: Community Elder', fontsize=16, fontweight='bold', color=colors['elder_primary'], y=0.98)
    
    # Save the figure
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('/workspace/charts/community_elder_journey_map.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return "Community Elder journey map created"

def create_community_leader_journey():
    """Create journey map for Community Leader persona"""
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(colors['background'])
    ax.set_facecolor(colors['background'])
    
    # Set up the journey stages
    stages = ['Awareness', 'Consideration', 'Onboarding', 'Regular Usage', 'Advocacy']
    y_categories = ['Touchpoints', 'Actions', 'Emotions', 'Pain Points', 'Opportunities']
    
    # Create a grid
    ax.set_xlim(0, len(stages))
    ax.set_ylim(0, len(y_categories))
    
    # Add stage headers
    for i, stage in enumerate(stages):
        ax.text(i + 0.5, len(y_categories) + 0.1, stage, 
                ha='center', va='bottom', fontsize=14, fontweight='bold', color=colors['leader_primary'])
        # Add vertical separator lines
        if i > 0:
            ax.axvline(x=i, color='gray', linestyle='-', alpha=0.3)
    
    # Add row headers
    for i, category in enumerate(y_categories):
        ax.text(-0.1, len(y_categories) - i - 0.5, category, 
                ha='right', va='center', fontsize=12, fontweight='bold', color=colors['text'])
        # Add horizontal separator lines
        if i > 0:
            ax.axhline(y=len(y_categories) - i, color='gray', linestyle='-', alpha=0.3)
    
    # Define content for each cell in the journey map
    journey_content = {
        # Awareness stage
        (0, 0): {  # Touchpoints
            'content': 'HOA board discussions\nProfessional network connections\nCommunity management resources\nReal estate development communications',
            'color': colors['leader_secondary']
        },
        (0, 1): {  # Actions
            'content': 'Proactively researches solutions\nEvaluates against community needs\nAnalyzes competitive platforms\nConsiders implementation strategy',
            'color': colors['leader_secondary']
        },
        (0, 2): {  # Emotions
            'content': 'Analytically interested\nStrategically focused\nConcerned about adoption\nExcited about improvements',
            'color': colors['neutral']
        },
        (0, 3): {  # Pain Points
            'content': 'Current platform fragmentation\nData-driven decision challenges\nCommunity adoption barriers\nTime investment concerns',
            'color': colors['negative']
        },
        (0, 4): {  # Opportunities
            'content': 'Provide platform comparison\nHighlight analytics capabilities\nDemonstrate governance tools\nEmphasize adoption strategies',
            'color': colors['positive']
        },
        
        # Consideration stage
        (1, 0): {  # Touchpoints
            'content': 'Detailed capabilities documentation\nCase studies from similar communities\nDemo of analytics and management tools\nDirect platform team communication',
            'color': colors['leader_secondary']
        },
        (1, 1): {  # Actions
            'content': 'Conducts feature analysis\nExplores analytics capabilities\nEvaluates adoption potential\nDevelops implementation strategy',
            'color': colors['leader_secondary']
        },
        (1, 2): {  # Emotions
            'content': 'Critically evaluative\nPragmatically optimistic\nResponsible for success\nFocused on measurable outcomes',
            'color': colors['neutral']
        },
        (1, 3): {  # Pain Points
            'content': 'Concerns about feature limitations\nQuestions about data security\nIntegration with existing systems\nCommunity resistance management',
            'color': colors['negative']
        },
        (1, 4): {  # Opportunities
            'content': 'Provide technical documentation\nOffer customization options\nDemonstrate security measures\nShare adoption strategy templates',
            'color': colors['positive']
        },
        
        # Onboarding stage
        (2, 0): {  # Touchpoints
            'content': 'Comprehensive setup documentation\nAdministrative dashboard\nCommunity importing tools\nImplementation strategy support',
            'color': colors['leader_secondary']
        },
        (2, 1): {  # Actions
            'content': 'Configures administrative settings\nImports community database\nEstablishes governance structure\nCreates community onboarding plan',
            'color': colors['leader_secondary']
        },
        (2, 2): {  # Emotions
            'content': 'Methodically engaged\nDetail-oriented\nResponsible for success\nConfident in capabilities',
            'color': colors['neutral']
        },
        (2, 3): {  # Pain Points
            'content': 'Advanced configuration complexity\nData migration challenges\nTime requirements for setup\nFeature utilization concerns',
            'color': colors['negative']
        },
        (2, 4): {  # Opportunities
            'content': 'Provide admin onboarding assistance\nOffer data migration support\nCreate implementation templates\nDevelop feature rollout guidance',
            'color': colors['positive']
        },
        
        # Regular Usage stage
        (3, 0): {  # Touchpoints
            'content': 'Administrative dashboard\nAnalytics reports and insights\nContent management system\nCommunity engagement metrics',
            'color': colors['leader_secondary']
        },
        (3, 1): {  # Actions
            'content': 'Monitors engagement analytics\nCreates community content\nManages governance communications\nUses data for decision-making',
            'color': colors['leader_secondary']
        },
        (3, 2): {  # Emotions
            'content': 'Data-driven satisfaction\nProfessional pride in system\nStrategic about utilization\nInvested in improvement',
            'color': colors['positive']
        },
        (3, 3): {  # Pain Points
            'content': 'Feature limitations for advanced needs\nAnalytics customization depth\nIntegration with other systems\nAdmin time management',
            'color': colors['negative']
        },
        (3, 4): {  # Opportunities
            'content': 'Provide advanced analytics training\nDevelop admin efficiency tools\nCreate automation capabilities\nOffer integration APIs',
            'color': colors['positive']
        },
        
        # Advocacy stage
        (4, 0): {  # Touchpoints
            'content': 'Community leadership forums\nProfessional network sharing\nPlatform development feedback\nCase study participation',
            'color': colors['leader_secondary']
        },
        (4, 1): {  # Actions
            'content': 'Actively promotes to other leaders\nProvides detailed platform feedback\nParticipates in feature discussions\nShowcases success metrics',
            'color': colors['leader_secondary']
        },
        (4, 2): {  # Emotions
            'content': 'Professionally invested\nCollaborative with platform team\nProud of innovation adoption\nStrategic about evolution',
            'color': colors['positive']
        },
        (4, 3): {  # Pain Points
            'content': 'Feature request implementation time\nLimited influence on roadmap\nBalancing feedback with needs\nMaintaining consistent advocacy',
            'color': colors['negative']
        },
        (4, 4): {  # Opportunities
            'content': 'Create leader advisory board\nImplement feature request system\nDevelop community showcases\nProvide exclusive beta access',
            'color': colors['positive']
        },
    }
    
    # Add content to each cell
    for (x, y), data in journey_content.items():
        content = data['content']
        color = data['color']
        
        rect = patches.Rectangle((x, len(y_categories) - y - 1), 1, 1, 
                               linewidth=1, edgecolor='gray', facecolor=color, alpha=0.3)
        ax.add_patch(rect)
        
        ax.text(x + 0.5, len(y_categories) - y - 0.5, content, 
                ha='center', va='center', fontsize=9, color=colors['text'],
                linespacing=1.3)
    
    # Add user journey line
    # Define emotion scores for each stage (1-5 scale, 5 being most positive)
    emotion_scores = [3.2, 3.5, 3.8, 4.2, 4.5]
    emotion_y_positions = [len(y_categories) - 2.5 - (score-1)/4 for score in emotion_scores]
    
    # Plot the emotion line
    for i in range(len(stages)-1):
        ax.plot([i+0.5, i+1.5], [emotion_y_positions[i], emotion_y_positions[i+1]], 
                color=colors['leader_primary'], linewidth=3, marker='o', markersize=8)
    
    # Add persona information
    persona_info = "JOURNEY MAP: COMMUNITY LEADER\nDavid Kim (42-48 years old)\n\"I need comprehensive tools to stay informed, share updates, and connect neighbors with resources.\""
    fig.text(0.02, 0.02, persona_info, fontsize=12, fontweight='bold', color=colors['leader_primary'])
    
    # Remove ticks and spines
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Add title
    plt.suptitle('User Journey Map: Community Leader', fontsize=16, fontweight='bold', color=colors['leader_primary'], y=0.98)
    
    # Save the figure
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('/workspace/charts/community_leader_journey_map.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return "Community Leader journey map created"

def create_ideal_customer_profile():
    """Create visualization for Ideal Customer Profile"""
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor(colors['background'])
    ax.set_facecolor(colors['background'])
    
    # Define the categories and characteristics
    categories = ['Community Characteristics', 'Technology Profile', 'Communication Preferences', 
                 'Engagement Patterns', 'High-Value Indicators']
    
    characteristics = {
        'Community Characteristics': [
            'Planned residential development (50-500 homes)',
            'Suburban location near mid-sized city',
            'Middle to upper-middle income ($75K-$150K)',
            'Active HOA or community association',
            'Mixed generations with 25%+ families',
            '60%+ homeownership rate',
            'Located in 10%+ population growth area',
            'Community age: New to 5 years'
        ],
        'Technology Profile': [
            '90%+ broadband internet penetration',
            '70%+ smart home device adoption',
            '80%+ email usage',
            '60%+ smartphone ownership',
            'Moderate to high social media usage',
            '$2,000+ annual technology spending',
            'Multiple device households',
            'Evidence of platform fatigue'
        ],
        'Communication Preferences': [
            'Email as primary channel (66% preference)',
            'Text messaging for urgent info (53%)',
            'Professional content curation valued',
            'Mobile-first content consumption (65%)',
            'Weekly communication frequency preference',
            'Evening peak engagement (5-8 PM)',
            'Preference for concise, scannable content',
            'Privacy and data control concerns'
        ],
        'Engagement Patterns': [
            'Active information seeking behavior',
            '40%+ community activity participation',
            'Strong local business support preference',
            '30%+ event attendance',
            '15%+ volunteer for community initiatives',
            'Multiple platform usage for communication',
            'Community-oriented decision making',
            'Interest in neighborhood connections'
        ],
        'High-Value Indicators': [
            'Active HOA with communication challenges',
            'Growing local business ecosystem nearby',
            'Recent or planned community improvements',
            'Expressed dissatisfaction with current channels',
            'Community leadership receptive to new tools',
            'Demonstrated interest in technology solutions',
            'Existing newsletter with limited functionality',
            'Evidence of resident information-seeking'
        ]
    }
    
    # Create a visual ICP profile
    num_categories = len(categories)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    
    # Add title
    plt.suptitle('Quality Neighbor: Ideal Customer Profile (ICP)', 
                fontsize=18, fontweight='bold', y=0.98)
    
    # Add subtitle
    plt.figtext(0.5, 0.92, 'Target Communities: Planned Residential Developments with Active Communication Needs',
               ha='center', fontsize=14, fontstyle='italic')
    
    # Add each category and its characteristics
    height_per_category = 2.2
    
    for i, category in enumerate(categories):
        # Add category header
        y_position = 10 - i * height_per_category
        rect = patches.Rectangle((0.5, y_position), 9, 0.6, 
                               linewidth=0, facecolor='#6c757d', alpha=0.2)
        ax.add_patch(rect)
        ax.text(5, y_position + 0.3, category, 
                ha='center', va='center', fontsize=14, fontweight='bold', color=colors['text'])
        
        # Add characteristics
        chars = characteristics[category]
        chars_per_row = 4
        rows = len(chars) // chars_per_row + (1 if len(chars) % chars_per_row > 0 else 0)
        
        for j, char in enumerate(chars):
            row = j // chars_per_row
            col = j % chars_per_row
            
            x = 0.8 + col * 2.3
            y = y_position - 0.3 - row * 0.4
            
            # Add bullet point with characteristic
            ax.text(x, y, f'• {char}', fontsize=10, va='center', color=colors['text'])
    
    # Add decision maker information
    decision_makers_title = "Key Decision Makers:"
    ax.text(1, 1.5, decision_makers_title, fontsize=12, fontweight='bold', color=colors['text'])
    
    decision_makers = [
        "HOA Board Members: Focus on governance and communication efficiency",
        "Community Managers: Professional management seeking resident satisfaction",
        "Resident Committee Leaders: Volunteer leaders needing organization tools",
        "Local Business Associations: Seeking community connection channels"
    ]
    
    for i, dm in enumerate(decision_makers):
        ax.text(1.2, 1.1 - i * 0.3, dm, fontsize=10, color=colors['text'])
    
    # Add acquisition strategy
    acquisition_title = "Acquisition Strategy:"
    ax.text(6, 1.5, acquisition_title, fontsize=12, fontweight='bold', color=colors['text'])
    
    acquisition_strategies = [
        "Target new developments (1-3 years) with active HOAs",
        "Partner with real estate developers for new community launches",
        "Connect through HOA management companies (enterprise solutions)",
        "Engage at community leadership conferences and local business networks"
    ]
    
    for i, strategy in enumerate(acquisition_strategies):
        ax.text(6.2, 1.1 - i * 0.3, strategy, fontsize=10, color=colors['text'])
    
    # Remove ticks and spines
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Save the figure
    plt.tight_layout(rect=[0, 0, 1, 0.9])
    plt.savefig('/workspace/charts/ideal_customer_profile.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return "Ideal Customer Profile visualization created"

# Run all journey map creations
def create_all_visualizations():
    print("Creating user journey maps and persona visualizations...")
    create_growing_family_journey()
    create_community_elder_journey()
    create_community_leader_journey()
    create_ideal_customer_profile()
    print("All journey maps and visualizations created successfully!")

if __name__ == "__main__":
    create_all_visualizations()