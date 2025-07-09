import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts'
import { TrendingUp, Users, Target, DollarSign, Brain, Trophy, Shield, Zap, BarChart3, PieChart as PieChartIcon, LineChart as LineChartIcon, Globe, Star, AlertTriangle, CheckCircle } from 'lucide-react'
import './App.css'

// Sample data for charts
const marketSizeData = [
  { year: '2023', value: 148.8 },
  { year: '2024', value: 162.5 },
  { year: '2025', value: 177.8 },
  { year: '2026', value: 194.5 },
  { year: '2027', value: 212.8 },
  { year: '2028', value: 232.9 },
  { year: '2029', value: 255.1 },
  { year: '2030', value: 279.6 },
]

const demographicsData = [
  { name: '25-40 years', value: 45, color: 'var(--primary)' },
  { name: 'Under 25', value: 25, color: 'var(--secondary)' },
  { name: '41-55 years', value: 20, color: 'var(--accent)' },
  { name: '55+ years', value: 10, color: 'var(--muted-foreground)' },
]

const competitorData = [
  { name: 'DraftKings', marketShare: 35, strength: 'Large user base' },
  { name: 'FanDuel', marketShare: 30, strength: 'Brand recognition' },
  { name: 'PrizePicks', marketShare: 15, strength: 'Skill-based focus' },
  { name: 'Others', marketShare: 20, strength: 'Niche markets' },
]

const kpiData = [
  { metric: 'User Acquisition Cost', target: '$25', current: '$30', progress: 83 },
  { metric: 'Monthly Active Users', target: '10K', current: '7.5K', progress: 75 },
  { metric: 'User Retention (30-day)', target: '60%', current: '45%', progress: 75 },
  { metric: 'Average Revenue Per User', target: '$15', current: '$12', progress: 80 },
]

function App() {
  const [activeTab, setActiveTab] = useState('overview')

  return (
    <div className="min-h-screen bg-background text-foreground dark">
      <div className="container mx-auto p-6">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-primary mb-2">
            Sportsclub Market Research & Strategy Dashboard
          </h1>
          <p className="text-lg text-secondary-foreground">
            Comprehensive analysis for skill-based sports prediction platform
          </p>
          <Badge variant="outline" className="mt-2 border-primary text-primary">
            Play Smart. Win Big.
          </Badge>
        </div>

        {/* Navigation Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-7 mb-6 bg-card">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="market">Market</TabsTrigger>
            <TabsTrigger value="personas">Personas</TabsTrigger>
            <TabsTrigger value="competitors">Competitors</TabsTrigger>
            <TabsTrigger value="swot">SWOT</TabsTrigger>
            <TabsTrigger value="gtm">GTM Strategy</TabsTrigger>
            <TabsTrigger value="legal">Legal</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card className="border-border bg-card text-card-foreground">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Market Size (2024)</CardTitle>
                  <TrendingUp className="h-4 w-4 text-primary" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-primary">$162.5B</div>
                  <p className="text-xs text-muted-foreground">
                    +9.2% from previous year
                  </p>
                </CardContent>
              </Card>

              <Card className="border-border bg-card text-card-foreground">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Target Users</CardTitle>
                  <Users className="h-4 w-4 text-primary" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-primary">25-40</div>
                  <p className="text-xs text-muted-foreground">
                    Primary age demographic
                  </p>
                </CardContent>
              </Card>

              <Card className="border-border bg-card text-card-foreground">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Skill-Based Focus</CardTitle>
                  <Brain className="h-4 w-4 text-primary" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-primary">100%</div>
                  <p className="text-xs text-muted-foreground">
                    No gambling, pure skill
                  </p>
                </CardContent>
              </Card>

              <Card className="border-border bg-card text-card-foreground">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Legal Compliance</CardTitle>
                  <Shield className="h-4 w-4 text-primary" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-green-500">Compliant</div>
                  <p className="text-xs text-muted-foreground">
                    Florida statute aligned
                  </p>
                </CardContent>
              </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="border-border bg-card text-card-foreground">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BarChart3 className="h-5 w-5 text-primary" />
                    Market Growth Projection
                  </CardTitle>
                  <CardDescription>Sports betting market size (USD Billions)</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={marketSizeData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                      <XAxis dataKey="year" stroke="var(--foreground)" />
                      <YAxis stroke="var(--foreground)" />
                      <Tooltip contentStyle={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)', color: 'var(--foreground)' }} />
                      <Line type="monotone" dataKey="value" stroke="var(--primary)" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card className="border-border bg-card text-card-foreground">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <PieChartIcon className="h-5 w-5 text-primary" />
                    Target Demographics
                  </CardTitle>
                  <CardDescription>Age distribution of target users</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={demographicsData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        outerRadius={80}
                        dataKey="value"
                      >
                        {demographicsData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip contentStyle={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)', color: 'var(--foreground)' }} />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Market Tab */}
          <TabsContent value="market" className="space-y-6">
            <Card className="border-border bg-card text-card-foreground">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Globe className="h-5 w-5 text-primary" />
                  Market Analysis
                </CardTitle>
                <CardDescription>Comprehensive market research findings</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-semibold text-primary mb-2">Market Size & Growth</h4>
                    <ul className="space-y-1 text-sm text-muted-foreground">
                      <li>• Global sports betting market: $148.8B (2024)</li>
                      <li>• Projected to reach $329.96B by 2033</li>
                      <li>• CAGR of 9.26% (2024-2033)</li>
                      <li>• Skill gaming segment growing at 15% annually</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold text-primary mb-2">Key Trends</h4>
                    <ul className="space-y-1 text-sm text-muted-foreground">
                      <li>• Rising popularity of prediction markets</li>
                      <li>• Increased demand for skill-based platforms</li>
                      <li>• AI and data analytics integration</li>
                      <li>• Community-driven engagement</li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-border bg-card text-card-foreground">
              <CardHeader>
                <CardTitle>Market Opportunity</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={marketSizeData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                    <XAxis dataKey="year" stroke="var(--foreground)" />
                    <YAxis stroke="var(--foreground)" />
                    <Tooltip contentStyle={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)', color: 'var(--foreground)' }} />
                    <Bar dataKey="value" fill="var(--primary)" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Personas Tab */}
          <TabsContent value="personas" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card className="border-border bg-card text-card-foreground">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Users className="h-5 w-5 text-primary" />
                    Casual Sports Enthusiast
                  </CardTitle>
                  <CardDescription>David - The Social Fan</CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div>
                    <h4 className="font-semibold text-sm">Demographics</h4>
                    <p className="text-sm text-muted-foreground">25-55 years, moderate income</p>
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm">Goals</h4>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      <li>• Fun, low-pressure engagement</li>
                      <li>• Social interaction with friends</li>
                      <li>• Test basic sports intuition</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm">Pain Points</h4>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      <li>• Complex platforms</li>
                      <li>• Risk of losing real money</li>
                      <li>• Lack of social features</li>
                    </ul>
                  </div>
                </CardContent>
              </Card>

              <Card className="border-border bg-card text-card-foreground">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Brain className="h-5 w-5 text-primary" />
                    Data-Driven Learner
                  </CardTitle>
                  <CardDescription>Emily - The Analytical Fan</CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div>
                    <h4 className="font-semibold text-sm">Demographics</h4>
                    <p className="text-sm text-muted-foreground">25-40 years, higher education</p>
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm">Goals</h4>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      <li>• Improve predictive skills</li>
                      <li>• Leverage data and AI tools</li>
                      <li>• Learn data science principles</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm">Pain Points</h4>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      <li>• Lack of reliable data</li>
                      <li>• No analytical tools</li>
                      <li>• Generic AI assistance</li>
                    </ul>
                  </div>
                </CardContent>
              </Card>

              <Card className="border-border bg-card text-card-foreground">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Trophy className="h-5 w-5 text-primary" />
                    Competitive Player
                  </CardTitle>
                  <CardDescription>Kevin - The Driven Competitor</CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div>
                    <h4 className="font-semibold text-sm">Demographics</h4>
                    <p className="text-sm text-muted-foreground">25-40 years, competitive mindset</p>
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm">Goals</h4>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      <li>• Win cash prizes</li>
                      <li>• Achieve top rankings</li>
                      <li>• Outperform skilled players</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm">Pain Points</h4>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      <li>• Unclear prize structures</li>
                      <li>• Lack of genuine competition</li>
                      <li>• Security concerns</li>
                    </ul>
                  </div>
                </CardContent>
              </Card>
            </div>

            <Card className="border-border bg-card text-card-foreground">
              <CardHeader>
                <CardTitle>Ideal Customer Profile (ICP)</CardTitle>
                <CardDescription>Composite of most valuable user attributes</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-semibold text-primary mb-3">Demographics</h4>
                    <ul className="space-y-2 text-sm text-muted-foreground">
                      <li>• <strong>Age:</strong> 25-40 years old</li>
                      <li>• <strong>Gender:</strong> Primarily male, significant female engagement</li>
                      <li>• <strong>Location:</strong> Regions with clear skill-gaming laws</li>
                      <li>• <strong>Income:</strong> Moderate to high disposable income</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold text-primary mb-3">Psychographics</h4>
                    <ul className="space-y-2 text-sm text-muted-foreground">
                      <li>• <strong>Interests:</strong> Passionate sports fans</li>
                      <li>• <strong>Mindset:</strong> Intellectually curious, competitive</li>
                      <li>• <strong>Behavior:</strong> Tech-savvy, data consumers</li>
                      <li>• <strong>Values:</strong> Skill over chance, community-minded</li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Competitors Tab */}
          <TabsContent value="competitors" className="space-y-6">
            <Card className="border-border bg-card text-card-foreground">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Target className="h-5 w-5 text-primary" />
                  Competitive Landscape
                </CardTitle>
                <CardDescription>Analysis of key competitors and market positioning</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-semibold text-primary mb-3">Market Share</h4>
                    <ResponsiveContainer width="100%" height={200}>
                      <PieChart>
                        <Pie
                          data={competitorData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={({ name, value }) => `${name} ${value}%`}
                          outerRadius={80}
                          dataKey="marketShare"
                        >
                          {competitorData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={demographicsData[index]?.color || 'var(--primary)'} />
                          ))}
                        </Pie>
                        <Tooltip contentStyle={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)', color: 'var(--foreground)' }} />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                  <div>
                    <h4 className="font-semibold text-primary mb-3">Competitor Strengths</h4>
                    <div className="space-y-3">
                      {competitorData.map((competitor, index) => (
                        <div key={index} className="flex justify-between items-center">
                          <span className="font-medium">{competitor.name}</span>
                          <Badge variant="outline" className="border-border text-muted-foreground">{competitor.strength}</Badge>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card className="border-border bg-card text-card-foreground">
                <CardHeader>
                  <CardTitle>Daily Fantasy Sports (DFS)</CardTitle>
                  <CardDescription>Direct competitors in skill-based sports engagement</CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div>
                    <h5 className="font-semibold text-sm">Examples</h5>
                    <p className="text-sm text-muted-foreground">PrizePicks, DraftKings, FanDuel</p>
                  </div>
                  <div>
                    <h5 className="font-semibold text-sm">Strengths</h5>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      <li>• Large user bases</li>
                      <li>• Established brands</li>
                      <li>• Strong data integration</li>
                    </ul>
                  </div>
                  <div>
                    <h5 className="font-semibold text-sm">Weaknesses</h5>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      <li>• Complex for casual users</li>
                      <li>• Regulatory scrutiny</li>
                      <li>• Limited educational focus</li>
                    </ul>
                  </div>
                </CardContent>
              </Card>

              <Card className="border-border bg-card text-card-foreground">
                <CardHeader>
                  <CardTitle>Prediction Markets</CardTitle>
                  <CardDescription>Emerging platforms for event prediction</CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div>
                    <h5 className="font-semibold text-sm">Examples</h5>
                    <p className="text-sm text-muted-foreground">BettorEdge, PredictionStrike</p>
                  </div>
                  <div>
                    <h5 className="font-semibold text-sm">Strengths</h5>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      <li>• Innovative approach</li>
                      <li>• Market dynamics appeal</li>
                      <li>• Diverse prediction opportunities</li>
                    </ul>
                  </div>
                  <div>
                    <h5 className="font-semibold text-sm">Weaknesses</h5>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      <li>• Complex for new users</li>
                      <li>• Evolving regulations</li>
                      <li>• Limited sports focus</li>
                    </ul>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* SWOT Tab */}
          <TabsContent value="swot" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card className="border-border bg-card text-card-foreground">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-green-500">
                    <CheckCircle className="h-5 w-5" />
                    Strengths
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2 text-sm text-muted-foreground">
                    <li>• <strong>Skill-based & Educational Focus:</strong> Clear positioning as learning platform</li>
                    <li>• <strong>Comprehensive AI Assistant:</strong> Unique competitive advantage</li>
                    <li>• <strong>Robust Gamification:</strong> Drives engagement and retention</li>
                    <li>• <strong>Strong Community Features:</strong> Forums and real-time chat</li>
                    <li>• <strong>Microservices Architecture:</strong> Scalable and reliable</li>
                    <li>• <strong>Data-Driven Approach:</strong> Real-time sports data validation</li>
                  </ul>
                </CardContent>
              </Card>

              <Card className="border-border bg-card text-card-foreground">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-primary">
                    <AlertTriangle className="h-5 w-5" />
                    Weaknesses
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2 text-sm text-muted-foreground">
                    <li>• <strong>New Entrant:</strong> Establishing brand recognition challenge</li>
                    <li>• <strong>Regulatory Nuance:</strong> Skill vs gambling perception</li>
                    <li>• <strong>User Acquisition Cost:</strong> Expensive to attract users</li>
                    <li>• <strong>Subscription Dependence:</strong> Users must perceive value</li>
                    <li>• <strong>Data Sourcing Reliability:</strong> External API dependencies</li>
                    <li>• <strong>AI Development Complexity:</strong> Resource-intensive</li>
                  </ul>
                </CardContent>
              </Card>

              <Card className="border-border bg-card text-card-foreground">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-accent">
                    <Zap className="h-5 w-5" />
                    Opportunities
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2 text-sm text-muted-foreground">
                    <li>• <strong>Growing Skill-Based Demand:</strong> Increasing interest in prediction markets</li>
                    <li>• <strong>Untapped Educational Niche:</strong> Few platforms combine sports + education</li>
                    <li>• <strong>Technological Advancements:</strong> AI and ML capabilities</li>
                    <li>• <strong>Partnership Potential:</strong> Sports data providers, media outlets</li>
                    <li>• <strong>International Expansion:</strong> Clear legal frameworks abroad</li>
                    <li>• <strong>Esports Integration:</strong> Rapidly growing audience</li>
                  </ul>
                </CardContent>
              </Card>

              <Card className="border-border bg-card text-card-foreground">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-orange-500">
                    <Shield className="h-5 w-5" />
                    Threats
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2 text-sm text-muted-foreground">
                    <li>• <strong>Evolving Regulations:</strong> Changing laws for skill games</li>
                    <li>• <strong>Well-Funded Competition:</strong> Large companies entering market</li>
                    <li>• <strong>Public Perception:</strong> Misconceptions about gambling</li>
                    <li>• <strong>Data Security Concerns:</strong> Breaches could damage trust</li>
                    <li>• <strong>Technological Obsolescence:</strong> Rapid AI advancement</li>
                    <li>• <strong>User Churn:</strong> If value perception decreases</li>
                  </ul>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* GTM Strategy Tab */}
          <TabsContent value="gtm" className="space-y-6">
            <Card className="border-border bg-card text-card-foreground">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Target className="h-5 w-5 text-primary" />
                  Go-to-Market Strategy
                </CardTitle>
                <CardDescription>Three-phase approach to market entry and growth</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  <div className="border-l-4 border-primary pl-4">
                    <h4 className="font-semibold text-primary">Phase 1: Pre-Launch & Beta</h4>
                    <p className="text-sm text-muted-foreground mb-2">Focus: Validation & Early Adopters</p>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      <li>• Closed beta program with select users</li>
                      <li>• Structured feedback mechanisms</li>
                      <li>• Early content marketing for data-driven learners</li>
                      <li>• Initial community building in private forums</li>
                    </ul>
                  </div>

                  <div className="border-l-4 border-secondary pl-4">
                    <h4 className="font-semibold text-primary">Phase 2: Launch & Growth</h4>
                    <p className="text-sm text-muted-foreground mb-2">Focus: User Acquisition & Engagement</p>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      <li>• Digital marketing campaigns (SEO, SEM, Social)</li>
                      <li>• Influencer partnerships with sports analysts</li>
                      <li>• Content marketing at scale</li>
                      <li>• Strategic partnerships with sports media</li>
                      <li>• Gamification promotion and referral programs</li>
                    </ul>
                  </div>

                  <div className="border-l-4 border-accent pl-4">
                    <h4 className="font-semibold text-primary">Phase 3: Retention & Expansion</h4>
                    <p className="text-sm text-muted-foreground mb-2">Focus: Long-term Value & New Features</p>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      <li>• Continuous product improvement</li>
                      <li>• Personalized engagement strategies</li>
                      <li>• Community events and tournaments</li>
                      <li>• Monetization optimization</li>
                      <li>• International expansion planning</li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-border bg-card text-card-foreground">
              <CardHeader>
                <CardTitle>Key Performance Indicators (KPIs)</CardTitle>
                <CardDescription>Critical metrics for measuring success</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {kpiData.map((kpi, index) => (
                    <div key={index} className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="font-medium">{kpi.metric}</span>
                        <span className="text-sm text-muted-foreground">
                          {kpi.current} / {kpi.target}
                        </span>
                      </div>
                      <Progress value={kpi.progress} className="h-2" />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Legal Tab */}
          <TabsContent value="legal" className="space-y-6">
            <Card className="border-border bg-card text-card-foreground">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Shield className="h-5 w-5 text-primary" />
                  Legal Compliance Framework
                </CardTitle>
                <CardDescription>Ensuring skill-based classification and regulatory compliance</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-semibold text-primary mb-3">Skill vs. Chance Distinction</h4>
                    <ul className="space-y-2 text-sm text-muted-foreground">
                      <li>• <strong>Predominance of Skill:</strong> Outcomes determined by user knowledge and analysis</li>
                      <li>• <strong>No Random Elements:</strong> No RNG or hidden factors affecting results</li>
                      <li>• <strong>Transparent Rules:</strong> Clear scoring and evaluation mechanisms</li>
                      <li>• <strong>Educational Focus:</strong> Platform positioned as learning tool</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold text-primary mb-3">Florida Statute Compliance</h4>
                    <ul className="space-y-2 text-sm text-muted-foreground">
                      <li>• <strong>Fla. Stat. § 546.10:</strong> Meets amusement game criteria</li>
                      <li>• <strong>No Bookmaking:</strong> Third-party odds only, no house positions</li>
                      <li>• <strong>Virtual Currency:</strong> Non-redeemable coins for engagement</li>
                      <li>• <strong>Prize Structure:</strong> Skill-based rewards from fixed pools</li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card className="border-border bg-card text-card-foreground">
                <CardHeader>
                  <CardTitle className="text-green-500">Compliance Strategies</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2 text-sm text-muted-foreground">
                    <li>• <strong>Skill-Based Design:</strong> Transparent, user-controlled outcomes</li>
                    <li>• <strong>Educational Content:</strong> Continuous learning resources</li>
                    <li>• <strong>No Direct Cash-Out:</strong> Virtual coins not redeemable</li>
                    <li>• <strong>Third-Party Odds:</strong> Independent data sources only</li>
                    <li>• <strong>Legal Counsel:</strong> Ongoing compliance monitoring</li>
                  </ul>
                </CardContent>
              </Card>

              <Card className="border-border bg-card text-card-foreground">
                <CardHeader>
                  <CardTitle className="text-accent">Data Privacy & Security</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2 text-sm text-muted-foreground">
                    <li>• <strong>GDPR/CCPA Compliance:</strong> Comprehensive data protection</li>
                    <li>• <strong>Age Verification:</strong> Robust processes for legal participation</li>
                    <li>• <strong>Data Minimization:</strong> Collect only necessary information</li>
                    <li>• <strong>Security Measures:</strong> Strong protection against breaches</li>
                    <li>• <strong>Transparency:</strong> Clear privacy policies and consent</li>
                  </ul>
                </CardContent>
              </Card>
            </div>

            <Card className="border-border bg-card text-card-foreground">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-orange-500">
                  <AlertTriangle className="h-5 w-5" />
                  Key Recommendations
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="p-3 bg-muted rounded-lg">
                    <h5 className="font-semibold text-sm mb-1">Strict Adherence to Skill-Based Design</h5>
                    <p className="text-sm text-muted-foreground">Ensure outcomes are solely dependent on user knowledge, research, and analytical skill with no chance elements.</p>
                  </div>
                  <div className="p-3 bg-muted rounded-lg">
                    <h5 className="font-semibold text-sm mb-1">Clear Monetization Model</h5>
                    <p className="text-sm text-muted-foreground">Subscription for access, virtual coins non-redeemable, prizes from pre-defined pools not user losses.</p>
                  </div>
                  <div className="p-3 bg-muted rounded-lg">
                    <h5 className="font-semibold text-sm mb-1">Avoid Bookmaking Activities</h5>
                    <p className="text-sm text-muted-foreground">Never generate own odds or act as counterparty. Use independent third-party data sources only.</p>
                  </div>
                  <div className="p-3 bg-muted rounded-lg">
                    <h5 className="font-semibold text-sm mb-1">Robust Legal Framework</h5>
                    <p className="text-sm text-muted-foreground">Engage specialized legal counsel, implement geo-fencing, and maintain comprehensive terms of service.</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default App

