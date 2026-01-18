# Multi-Source Dashboard User Guide

Welcome to the Multi-Source Dashboard! This comprehensive guide will help you get started with content aggregation, curation, and automated publishing across multiple platforms.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [Data Sources Configuration](#data-sources-configuration)
4. [Creating Content Collection Runs](#creating-content-collection-runs)
5. [Content Review and Curation](#content-review-and-curation)
6. [Blog Platform Setup](#blog-platform-setup)
7. [Publishing Content](#publishing-content)
8. [Analytics and Monitoring](#analytics-and-monitoring)
9. [Settings and Preferences](#settings-and-preferences)
10. [Troubleshooting](#troubleshooting)

## Getting Started

### System Requirements

- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, or Edge 90+
- **Internet Connection**: Stable broadband connection
- **Screen Resolution**: 1024x768 minimum (1920x1080 recommended)

### Account Registration

1. **Visit the Application**:
   - Navigate to `https://yourdomain.com`
   - Click "Sign Up" in the top-right corner

2. **Complete Registration Form**:
   ```
   Email Address: your-email@example.com
   Username: your_username
   Full Name: John Doe
   Password: Use a strong password (8+ characters)
   Confirm Password: Re-enter your password
   ```

3. **Verify Your Account**:
   - Check your email for verification link
   - Click the verification link to activate your account

4. **First Login**:
   - Return to the application
   - Click "Sign In"
   - Enter your email and password
   - Click "Sign In" to access the dashboard

### Initial Setup Wizard

Upon first login, you'll be guided through a setup wizard:

1. **Welcome Screen**: Introduction to the platform
2. **Data Sources**: Select content sources to monitor
3. **Blog Platforms**: Connect your publishing platforms
4. **Preferences**: Set content filtering preferences
5. **Complete Setup**: Finish and access the dashboard

## Dashboard Overview

### Main Dashboard Layout

The dashboard is divided into several key sections:

#### 📊 **Statistics Cards** (Top Row)
- **Total Runs**: Number of content collection runs created
- **Active Runs**: Currently running collection processes
- **Content Collected**: Total pieces of content aggregated
- **Published Content**: Successfully published articles

#### 📈 **Quick Actions** (Center)
- **Create New Run**: Start a new content collection
- **Review Content**: Access pending content for review
- **View Analytics**: Check performance metrics
- **Settings**: Access configuration options

#### 📋 **Recent Activity** (Bottom)
- **Recent Runs**: Latest collection run activities
- **Recent Content**: Newly collected content items
- **Publishing Activity**: Recent publishing actions

### Navigation Menu

#### Left Sidebar Navigation:
- **🏠 Dashboard**: Main overview page
- **🔄 Runs**: Manage content collection runs
- **📝 Content**: Review and manage collected content
- **🔗 Sources**: Configure data sources
- **📤 Blog Configs**: Set up publishing platforms
- **👥 Demographics**: Target audience settings
- **📊 Analytics**: Performance and statistics
- **⚙️ Settings**: Account and app preferences

## Data Sources Configuration

### Available Data Sources

#### **Hacker News**
- **Content Type**: Technology news and discussions
- **Update Frequency**: Real-time
- **Authentication**: Not required
- **Rate Limits**: 60 requests/minute

**Configuration Options**:
```
Story Type: Top Stories, New Stories, Best Stories
Content Limit: 1-100 items per collection
Minimum Score: Filter by community score
Age Limit: Content age in hours
```

#### **Reddit**
- **Content Type**: Community discussions and links
- **Update Frequency**: Real-time
- **Authentication**: Required (OAuth2)
- **Rate Limits**: 60 requests/minute

**Configuration Options**:
```
Subreddits: Select specific communities
Sort Method: Hot, New, Top, Rising
Time Period: Hour, Day, Week, Month, Year
Minimum Score: Filter by upvotes
```

### Setting Up Data Sources

1. **Navigate to Sources**:
   - Click "Sources" in the left sidebar
   - View available data sources

2. **Configure Hacker News**:
   - Click "Configure" next to Hacker News
   - Select story type (Top Stories recommended)
   - Set content limit (30-50 for daily collections)
   - Set minimum score (25+ recommended)
   - Click "Save Configuration"

3. **Configure Reddit** (Requires API Access):
   - Click "Configure" next to Reddit
   - Click "Connect Reddit Account"
   - Authorize the application
   - Select subreddits to monitor:
     ```
     Recommended Subreddits for Tech Content:
     - r/programming
     - r/technology
     - r/MachineLearning
     - r/webdev
     - r/datascience
     ```
   - Set filtering preferences
   - Click "Save Configuration"

4. **Test Configuration**:
   - Click "Test Connection" for each source
   - Verify sample content is retrieved
   - Adjust settings if needed

## Creating Content Collection Runs

### What is a Content Collection Run?

A content collection run is an automated process that:
- Gathers content from configured data sources
- Applies your filtering criteria
- Processes and categorizes content
- Makes it available for review and publishing

### Creating Your First Run

1. **Start Run Creation**:
   - Click "Create New Run" on the dashboard
   - Or navigate to "Runs" → "Create New Run"

2. **Basic Information**:
   ```
   Run Name: Daily Tech News Collection
   Description: Automated collection of programming and technology content
   Collection Frequency: 
   - Daily (recommended for beginners)
   - 2x Daily
   - 3x Daily  
   - 4x Daily
   - Hourly (for high-volume needs)
   ```

3. **Source Selection**:
   - ✅ **Hacker News**: Enable for tech news
   - ✅ **Reddit**: Enable for community discussions
   - Configure source-specific settings

4. **Content Filtering**:
   ```
   Keywords (Include): python, javascript, react, ai, machine learning
   Keywords (Exclude): spam, clickbait, advertisement
   Minimum Score: 25 (filters low-quality content)
   Maximum Age: 24 hours (fresh content only)
   Content Types: Stories, Articles (exclude comments initially)
   ```

5. **Target Demographics** (Optional):
   ```
   Target Audience: Software Developers
   Experience Level: Intermediate
   Interests: Web Development, AI/ML, Programming
   ```

6. **Publishing Settings**:
   ```
   Auto-Publish: Disabled (recommended for manual review)
   Max Posts Per Day: 5 (prevents over-posting)
   Review Required: Enabled
   Publishing Platforms: (Configure later)
   ```

7. **Schedule and Activation**:
   - Set collection time (e.g., 9:00 AM daily)
   - Review all settings
   - Click "Create Run"
   - Set status to "Active" to start collection

### Managing Runs

#### **Run Status Types**:
- **Draft**: Run created but not activated
- **Active**: Currently collecting content
- **Paused**: Temporarily stopped
- **Completed**: Finished (for one-time runs)
- **Failed**: Error occurred during execution

#### **Run Actions**:
- **▶️ Start**: Begin content collection
- **⏸️ Pause**: Temporarily stop collection
- **✏️ Edit**: Modify run configuration
- **📊 View Stats**: See collection performance
- **🗑️ Delete**: Remove run permanently

### Advanced Run Configuration

#### **Content Filtering Rules**:
```
Advanced Filters:
- Word Count: 200-5000 words
- Reading Time: 2-15 minutes
- External Links: Maximum 5
- Image Requirements: At least 1 image
- Language: English only
- Duplicate Detection: Enabled
```

#### **Sentiment Analysis**:
```
Content Sentiment:
- Positive: Focus on solutions and opportunities
- Neutral: Balanced, informational content
- Negative: Exclude overly critical content
```

#### **Topic Categories**:
```
Preferred Topics:
- Web Development (React, Vue, Angular)
- Backend Development (Node.js, Python, Java)
- Mobile Development (React Native, Flutter)
- DevOps and Cloud (AWS, Docker, Kubernetes)
- Data Science and AI/ML
- Cybersecurity
```

## Content Review and Curation

### Content Review Workflow

1. **Access Content for Review**:
   - Navigate to "Content" in the sidebar
   - Filter by "Pending Review" status
   - Content is automatically organized by collection date

2. **Content Card Information**:
   ```
   Title: Article/Story Title
   Source: Hacker News, Reddit, etc.
   Score: Community engagement score
   Comments: Number of discussions
   Reading Time: Estimated reading duration
   Tags: Automatically generated tags
   Sentiment: Positive/Neutral/Negative
   Collection Date: When content was gathered
   ```

3. **Review Actions**:
   - **👀 View Full Content**: Read complete article
   - **✅ Approve**: Mark for publishing
   - **❌ Reject**: Exclude from publishing
   - **📝 Edit**: Modify title, tags, or description
   - **🔗 View Original**: Open source URL

### Content Filtering and Search

#### **Filter Options**:
```
Status Filter:
- All Content
- Pending Review
- Approved
- Rejected
- Published

Source Filter:
- All Sources
- Hacker News
- Reddit
- [Other configured sources]

Date Range:
- Today
- Yesterday  
- Last 7 days
- Last 30 days
- Custom range

Content Type:
- Articles
- Discussions
- News
- Tutorials
```

#### **Search Functionality**:
- **Keyword Search**: Search titles and content
- **Tag Search**: Find content by tags
- **Author Search**: Find content by specific authors
- **Advanced Search**: Combine multiple criteria

### Content Quality Guidelines

#### **✅ Approve Content When**:
- Content is relevant to your audience
- Information is accurate and well-sourced
- Writing quality is good
- Content provides value (educational, informative, entertaining)
- No copyright or ethical issues
- Fits your brand/blog tone

#### **❌ Reject Content When**:
- Content is spam or low-quality
- Information is outdated or incorrect
- Contains inappropriate material
- Duplicate of already published content
- Copyright concerns exist
- Doesn't match your audience interests

### Bulk Actions

For efficient content management:

1. **Select Multiple Items**:
   - Use checkboxes to select content
   - Or use "Select All" for current page

2. **Bulk Operations**:
   - **Approve Selected**: Approve multiple items
   - **Reject Selected**: Reject multiple items
   - **Add Tags**: Apply tags to multiple items
   - **Export**: Download content data

## Blog Platform Setup

### Supported Platforms

#### **WordPress**
- **Self-hosted WordPress**: Full control and customization
- **WordPress.com**: Hosted solution with limitations
- **Authentication**: Application passwords (recommended)

#### **Dev.to**
- **Community**: Large developer community
- **Audience**: Technical professionals
- **Authentication**: API key
- **Features**: Tags, series, canonical URLs

#### **Ghost**
- **Platform**: Modern publishing platform
- **Audience**: Professional writers and creators
- **Authentication**: Admin API key
- **Features**: Rich editor, membership, newsletters

### Setting Up WordPress

1. **Navigate to Blog Configs**:
   - Click "Blog Configs" in sidebar
   - Click "Add New Configuration"
   - Select "WordPress"

2. **WordPress Configuration**:
   ```
   Configuration Name: My WordPress Blog
   WordPress URL: https://yourblog.com
   Username: your_username
   Authentication Method: Application Password (recommended)
   ```

3. **Generate Application Password**:
   - Login to your WordPress admin
   - Go to Users → Profile
   - Scroll to "Application Passwords"
   - Enter name: "Multi-Source Dashboard"
   - Click "Add New Application Password"
   - Copy the generated password

4. **Complete Configuration**:
   ```
   Application Password: [paste generated password]
   Default Category: Technology
   Default Tags: tech, programming
   Auto-Publish: Disabled (recommended initially)
   ```

5. **Test Connection**:
   - Click "Test Connection"
   - Verify successful connection
   - Check that categories and tags are detected

### Setting Up Dev.to

1. **Create Dev.to Account**:
   - Sign up at dev.to if you don't have an account
   - Complete your profile

2. **Generate API Key**:
   - Go to Settings → Account
   - Scroll to "DEV Community API Keys"
   - Click "Generate API Key"
   - Copy the key

3. **Configure in Dashboard**:
   ```
   Configuration Name: My Dev.to Profile
   Platform: Dev.to
   API Key: [paste your API key]
   Default Tags: programming, webdev, tutorial
   Auto-Publish: Disabled
   Canonical URL: Enabled (if content is published elsewhere first)
   ```

### Setting Up Ghost

1. **Access Ghost Admin**:
   - Login to your Ghost admin panel
   - Navigate to Settings → Integrations
   - Click "Add custom integration"

2. **Create Integration**:
   ```
   Integration Name: Multi-Source Dashboard
   Description: Automated content publishing
   ```

3. **Copy API Details**:
   - Copy the Admin API Key
   - Copy the API URL

4. **Configure in Dashboard**:
   ```
   Configuration Name: My Ghost Blog
   Platform: Ghost
   Ghost URL: https://yourblog.ghost.io
   Admin API Key: [paste admin API key]
   Default Author: Your Name
   Default Tags: technology, programming
   ```

### Platform-Specific Settings

#### **WordPress Settings**:
```
Post Status: Draft (recommended for review)
Comment Status: Open/Closed
Ping Status: Open/Closed
Featured Image: Auto-generate from content
Excerpt: Auto-generate from content
```

#### **Dev.to Settings**:
```
Published: False (saves as draft)
Main Image: Auto-extract from content
Canonical URL: Link to original source
Series: Group related content
Organization: Your organization (if applicable)
```

#### **Ghost Settings**:
```
Status: Draft
Featured: No
Page: No (use for posts)
Meta Title: Auto-generate
Meta Description: Auto-generate
```

## Publishing Content

### Publishing Workflow

1. **Select Approved Content**:
   - Navigate to Content section
   - Filter by "Approved" status
   - Select content for publishing

2. **Choose Publishing Platforms**:
   - Select one or more configured platforms
   - Each platform can have different settings

3. **Customize for Each Platform**:
   ```
   Title: Customize for platform audience
   Tags: Platform-appropriate tags
   Category: Select relevant category
   Description: Platform-specific description
   Scheduling: Immediate or scheduled
   ```

4. **Review and Publish**:
   - Preview how content will appear
   - Make final adjustments
   - Click "Publish Now" or "Schedule"

### Content Formatting

#### **Automatic Formatting**:
- **Title Optimization**: Engaging titles for each platform
- **Content Formatting**: HTML/Markdown conversion
- **Image Processing**: Resize and optimize images
- **Link Handling**: Convert to appropriate format
- **Tag Mapping**: Platform-specific tag suggestions

#### **Manual Customization**:
```
Custom Title: Platform-specific titles
Custom Tags: Tailor tags for each platform
Custom Description: Platform-appropriate descriptions
Featured Image: Select or upload custom image
Publishing Schedule: Set specific publish times
```

### Scheduling and Automation

#### **Publishing Schedule Options**:
```
Immediate: Publish right away
Scheduled: Set specific date and time
Queue: Add to publishing queue
Recurring: Regular publishing schedule
```

#### **Queue Management**:
- **View Queue**: See upcoming publications
- **Reorder**: Change publishing order
- **Edit Scheduled**: Modify scheduled content
- **Cancel**: Remove from queue

#### **Auto-Publishing Rules** (Advanced):
```
Auto-Publish Criteria:
- Content score above threshold
- Specific tags present
- Content type matches rules
- Time-based rules (publish during peak hours)
- Platform-specific rules
```

### Multi-Platform Publishing

#### **Cross-Platform Strategy**:
1. **Primary Platform**: Publish original content first
2. **Secondary Platforms**: Publish with canonical links
3. **Social Platforms**: Share with summaries
4. **Timing**: Stagger publications for maximum reach

#### **Platform-Specific Optimization**:
```
WordPress:
- SEO optimization
- Category organization
- Comment engagement

Dev.to:
- Community tags
- Series organization
- Discussion encouragement

Ghost:
- Newsletter integration
- Member-only content
- Rich formatting
```

### Publishing Analytics

#### **Track Publishing Performance**:
- **Success Rate**: Percentage of successful publishes
- **Error Rate**: Failed publication attempts
- **Engagement**: Views, comments, shares per platform
- **Best Performing Content**: Top-performing posts
- **Platform Comparison**: Performance across platforms

## Analytics and Monitoring

### Dashboard Analytics

#### **Key Metrics Overview**:
```
Content Collection:
- Items collected per day/week/month
- Collection success rate
- Source performance comparison
- Average content quality score

Content Processing:
- Review completion rate
- Approval vs rejection rate
- Time from collection to review
- Most popular topics/tags

Publishing Performance:
- Posts published per platform
- Publishing success rate
- Average time from approval to publish
- Cross-platform engagement comparison
```

### Detailed Analytics

#### **Content Performance**:
- **Top Performing Content**: Most engaging posts
- **Content Categories**: Performance by topic
- **Source Analysis**: Which sources provide best content
- **Timing Analysis**: Best times for collection and publishing

#### **Platform Analytics**:
```
WordPress:
- Page views and unique visitors
- Comments and engagement
- SEO performance
- Popular categories

Dev.to:
- Article views and reactions
- Comments and discussions
- Follower growth
- Tag performance

Ghost:
- Subscriber growth
- Email open rates
- Member engagement
- Revenue (if applicable)
```

### Performance Monitoring

#### **System Health**:
- **Data Source Uptime**: Availability of external APIs
- **Collection Performance**: Speed and reliability
- **Processing Times**: Content analysis duration
- **Error Rates**: System reliability metrics

#### **Alerts and Notifications**:
```
Email Notifications:
- Daily/weekly summary reports
- Failed collection attempts
- Publishing errors
- High-performing content alerts

Dashboard Alerts:
- Source unavailability
- Queue backup warnings
- Review pending notifications
- System maintenance alerts
```

### Custom Reports

#### **Generate Custom Reports**:
1. **Select Report Type**: Content, Publishing, or Performance
2. **Choose Date Range**: Custom time periods
3. **Select Metrics**: Specific data points
4. **Filter Criteria**: Sources, platforms, content types
5. **Export Options**: PDF, CSV, or email delivery

## Settings and Preferences

### Account Settings

#### **Profile Information**:
```
Display Name: Your public name
Bio: Brief description
Avatar: Profile picture
Email: Account email (for notifications)
Password: Change account password
```

#### **Notification Preferences**:
```
Email Notifications:
☑️ Daily summary reports
☑️ Content ready for review
☑️ Publishing failures
☑️ Weekly analytics summary
☐ System maintenance notices

Dashboard Notifications:
☑️ New content alerts
☑️ Publishing queue updates
☑️ Source connection issues
☐ Performance achievements
```

### Application Preferences

#### **Content Collection Settings**:
```
Default Collection Time: 9:00 AM
Duplicate Detection: Enabled
Auto-tagging: Enabled
Sentiment Analysis: Enabled
Content Scoring: Enabled
Language Detection: English Only
```

#### **Review Workflow Settings**:
```
Default Review Status: Pending Review
Auto-approve High-scoring Content: Disabled
Bulk Actions: Enabled
Content Preview: Full content
Review Queue Size: 50 items
```

#### **Publishing Preferences**:
```
Default Publishing Status: Draft
Cross-posting Delay: 2 hours
Canonical URL Handling: Automatic
Image Processing: Enabled
Link Tracking: Enabled
```

### Data and Privacy

#### **Data Management**:
```
Data Retention:
- Rejected content: 30 days
- Published content: Permanent
- Draft content: 90 days
- Analytics data: 1 year

Export Options:
- Content export (JSON/CSV)
- Analytics export
- Configuration backup
- Account data download
```

#### **Privacy Settings**:
```
Analytics Sharing: Disabled
Usage Statistics: Anonymous only
Third-party Integrations: Configured platforms only
Data Processing: Necessary functions only
```

## Troubleshooting

### Common Issues

#### **Content Collection Problems**

**Issue**: No content being collected
```
Solutions:
1. Check data source configurations
2. Verify API credentials
3. Check internet connection
4. Review content filters (may be too restrictive)
5. Check run status (ensure it's "Active")
```

**Issue**: Duplicate content appearing
```
Solutions:
1. Enable duplicate detection in settings
2. Adjust content filters
3. Review source overlaps
4. Check time ranges for collection
```

**Issue**: Low-quality content being collected
```
Solutions:
1. Increase minimum score threshold
2. Add negative keywords to filters
3. Adjust source configurations
4. Enable sentiment analysis filtering
```

#### **Publishing Problems**

**Issue**: Publishing failures
```
Solutions:
1. Test platform connections in Blog Configs
2. Check API credentials and permissions
3. Verify content formatting
4. Check platform-specific requirements
5. Review error logs in publishing history
```

**Issue**: Content formatting issues
```
Solutions:
1. Check HTML/Markdown conversion settings
2. Review image processing configuration
3. Verify link handling settings
4. Test with sample content
5. Check platform-specific formatting rules
```

#### **Authentication Issues**

**Issue**: Login problems
```
Solutions:
1. Reset password using "Forgot Password"
2. Clear browser cache and cookies
3. Try different browser
4. Check email for account verification
5. Contact support if account is locked
```

**Issue**: API connection failures
```
Solutions:
1. Regenerate API keys
2. Check API rate limits
3. Verify permissions for API keys
4. Test connections outside the platform
5. Check platform service status
```

### Performance Issues

#### **Slow Content Loading**

```
Troubleshooting Steps:
1. Check internet connection speed
2. Clear browser cache
3. Reduce content filter complexity
4. Limit number of sources
5. Contact support for server status
```

#### **High Memory Usage**

```
Solutions:
1. Reduce concurrent collection runs
2. Lower content limits per collection
3. Clear old content regularly
4. Optimize browser settings
5. Close unnecessary browser tabs
```

### Getting Help

#### **Support Channels**:
- **Help Documentation**: Built-in help system
- **Email Support**: support@yourdomain.com
- **Community Forum**: community.yourdomain.com
- **Video Tutorials**: help.yourdomain.com/videos
- **Live Chat**: Available during business hours

#### **Before Contacting Support**:
1. Check this user guide
2. Search the knowledge base
3. Try basic troubleshooting steps
4. Gather error messages and screenshots
5. Note when the issue started occurring

#### **Information to Include in Support Requests**:
- Account username (not password)
- Browser and version
- Operating system
- Specific error messages
- Steps to reproduce the issue
- Screenshots of the problem

### Best Practices

#### **Content Collection**:
- Start with fewer sources and expand gradually
- Use specific, relevant keywords in filters
- Regularly review and adjust filter criteria
- Monitor source performance and reliability
- Keep collections focused on your niche

#### **Content Review**:
- Establish consistent review criteria
- Create a regular review schedule
- Use bulk actions for efficiency
- Maintain quality standards
- Document common rejection reasons

#### **Publishing Strategy**:
- Test all platform configurations thoroughly
- Start with manual publishing before automation
- Stagger publications across platforms
- Monitor engagement and adjust strategy
- Keep backup copies of published content

This user guide provides comprehensive information for using the Multi-Source Dashboard effectively. For additional help or advanced configuration questions, please refer to the support resources or contact our support team.