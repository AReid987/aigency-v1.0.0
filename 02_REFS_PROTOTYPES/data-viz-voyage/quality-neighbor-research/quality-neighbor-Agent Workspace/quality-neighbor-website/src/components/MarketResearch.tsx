import { useEffect, useState } from 'react'
import { Bar, Doughnut, Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import { TrendingUp, Users, DollarSign, Target, ArrowUpRight, Building, Newspaper, AlertCircle } from 'lucide-react'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

const MarketResearch = () => {
  const [researchData, setResearchData] = useState<any>(null)
  const [competitorData, setCompetitorData] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadData = async () => {
      try {
        const [researchResponse, competitorResponse] = await Promise.all([
          fetch('/data/quality_neighbor_final_research_summary.json'),
          fetch('/data/comprehensive_competitor_analysis.json')
        ])
        
        const research = await researchResponse.json()
        const competitors = await competitorResponse.json()
        
        setResearchData(research)
        setCompetitorData(competitors)
        setLoading(false)
      } catch (error) {
        console.error('Error loading data:', error)
        setLoading(false)
      }
    }

    loadData()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  const marketSizeData = {
    labels: ['2024 Current', '2027 Projected', '2030 Projected'],
    datasets: [
      {
        label: 'Market Size (Billions USD)',
        data: [1.85, 3.5, 4.7], // Average of ranges from research data
        backgroundColor: ['#3B82F6', '#60A5FA', '#93C5FD'],
        borderColor: ['#1D4ED8', '#2563EB', '#3B82F6'],
        borderWidth: 2,
      },
    ],
  }

  const competitorLandscapeData = {
    labels: ['NextDoor', 'Facebook Groups', 'Front Porch Forum', 'Quality Neighbor'],
    datasets: [
      {
        label: 'User Base (Millions)',
        data: [45, 1800, 0.2, 0], // NextDoor 45M+, Facebook 1.8B+ (scaled), Front Porch 200K
        backgroundColor: ['#EF4444', '#1877F2', '#10B981', '#3B82F6'],
        borderWidth: 0,
      },
    ],
  }

  const newsletterGrowthData = {
    labels: ['2020', '2021', '2022', '2023', '2024', '2025E'],
    datasets: [
      {
        label: 'Newsletter Market Growth (%)',
        data: [15, 25, 45, 68, 96, 120],
        borderColor: '#10B981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        fill: true,
        tension: 0.4,
      },
    ],
  }

  const keyFindings = [
    {
      icon: DollarSign,
      title: 'Market Size',
      value: '$1.2-2.5B',
      description: 'Current market size with strong growth trajectory',
      trend: '+16.2% CAGR',
      color: 'text-green-600 bg-green-50'
    },
    {
      icon: TrendingUp,
      title: 'Newsletter Growth',
      value: '96% YoY',
      description: 'Newsletter platform growth rate in 2024',
      trend: 'Accelerating',
      color: 'text-blue-600 bg-blue-50'
    },
    {
      icon: Users,
      title: 'Target Market',
      value: '80%',
      description: 'Homeowners actively using community apps',
      trend: '41% daily users',
      color: 'text-purple-600 bg-purple-50'
    },
    {
      icon: Building,
      title: 'Revenue Potential',
      value: '$300K',
      description: 'Annual revenue benchmark for local newsletters',
      trend: 'Proven model',
      color: 'text-orange-600 bg-orange-50'
    }
  ]

  const competitiveAdvantages = [
    'Professional newsletter format vs social media feeds',
    'Curated content quality vs user-generated chaos',
    'Local business integration with clear ROI',
    'Privacy-first approach without social media baggage',
    'Community-specific customization capability',
    'Email-based accessibility across age groups'
  ]

  const marketOpportunities = [
    'Growing demand for hyperlocal content',
    'Distrust of major social media platforms',
    'Local business advertising needs',
    'Professional community communication preference',
    'Newsletter format familiarity and trust',
    'Underserved residential development market'
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">Market Research Analysis</h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Comprehensive analysis of the community platform market, competitive landscape, 
              and growth opportunities for Quality Neighbor
            </p>
          </div>
        </div>
      </section>

      {/* Key Findings */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">Key Market Findings</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {keyFindings.map((finding, index) => {
              const Icon = finding.icon
              return (
                <div key={index} className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
                  <div className={`w-12 h-12 rounded-lg ${finding.color} flex items-center justify-center mb-4`}>
                    <Icon size={24} />
                  </div>
                  <div className="text-3xl font-bold text-gray-900 mb-2">{finding.value}</div>
                  <div className="text-lg font-semibold text-gray-900 mb-2">{finding.title}</div>
                  <div className="text-gray-600 mb-3">{finding.description}</div>
                  <div className="flex items-center text-sm font-medium text-green-600">
                    <ArrowUpRight size={16} className="mr-1" />
                    {finding.trend}
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Market Size Analysis */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">Market Size & Growth</h2>
              <div className="space-y-6">
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-blue-600 font-bold text-sm">1</span>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">Current Market Size</h3>
                    <p className="text-gray-600">$1.2-2.5 billion market with established players and growing demand</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-blue-600 font-bold text-sm">2</span>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">Growth Trajectory</h3>
                    <p className="text-gray-600">16.2% CAGR with newsletter segment showing 96% YoY growth</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-blue-600 font-bold text-sm">3</span>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">Future Projection</h3>
                    <p className="text-gray-600">$3-4.7 billion by 2030-2033, driven by hyperlocal content demand</p>
                  </div>
                </div>
              </div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Market Size Projection</h3>
              <Bar data={marketSizeData} options={{
                responsive: true,
                plugins: {
                  legend: {
                    display: false,
                  },
                },
                scales: {
                  y: {
                    beginAtZero: true,
                    title: {
                      display: true,
                      text: 'Billions USD'
                    }
                  }
                }
              }} />
            </div>
          </div>
        </div>
      </section>

      {/* Competitive Landscape */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">Competitive Landscape</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            <div className="bg-gray-50 p-6 rounded-lg">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Market Share Distribution</h3>
              <Doughnut data={competitorLandscapeData} options={{
                responsive: true,
                plugins: {
                  legend: {
                    position: 'bottom',
                  },
                },
              }} />
            </div>
            <div>
              <h3 className="text-xl font-semibold text-gray-900 mb-6">Competitive Analysis</h3>
              <div className="space-y-4">
                <div className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-red-600">NextDoor</h4>
                    <span className="text-sm text-gray-600">Direct Competitor - HIGH Threat</span>
                  </div>
                  <p className="text-sm text-gray-700">45M+ users, social feed format, privacy concerns</p>
                </div>
                <div className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-blue-600">Facebook Groups</h4>
                    <span className="text-sm text-gray-600">Indirect Competitor - HIGH Threat</span>
                  </div>
                  <p className="text-sm text-gray-700">1.8B+ users, algorithm-driven, information overload</p>
                </div>
                <div className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-green-600">Front Porch Forum</h4>
                    <span className="text-sm text-gray-600">Direct Competitor - MEDIUM Threat</span>
                  </div>
                  <p className="text-sm text-gray-700">200K+ users, newsletter format, limited features</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Newsletter Growth Trend */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Newsletter Market Growth</h3>
              <Line data={newsletterGrowthData} options={{
                responsive: true,
                plugins: {
                  legend: {
                    display: false,
                  },
                },
                scales: {
                  y: {
                    beginAtZero: true,
                    title: {
                      display: true,
                      text: 'Growth Rate (%)'
                    }
                  }
                }
              }} />
            </div>
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">Newsletter Renaissance</h2>
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <Newspaper className="text-blue-600" size={24} />
                  <div>
                    <h3 className="font-semibold text-gray-900">96% Year-over-Year Growth</h3>
                    <p className="text-gray-600">Newsletter platforms experiencing unprecedented growth</p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <Target className="text-green-600" size={24} />
                  <div>
                    <h3 className="font-semibold text-gray-900">37.67% Average Open Rate</h3>
                    <p className="text-gray-600">Significantly higher than industry average of 19-23%</p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <DollarSign className="text-purple-600" size={24} />
                  <div>
                    <h3 className="font-semibold text-gray-900">$14.5M Platform Revenue</h3>
                    <p className="text-gray-600">BeehiiV platform total monetization in 2024</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Competitive Advantages */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">Competitive Advantages</h2>
              <div className="space-y-4">
                {competitiveAdvantages.map((advantage, index) => (
                  <div key={index} className="flex items-start space-x-3">
                    <div className="flex-shrink-0 w-6 h-6 bg-green-100 rounded-full flex items-center justify-center mt-1">
                      <span className="text-green-600 text-xs">✓</span>
                    </div>
                    <p className="text-gray-700">{advantage}</p>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">Market Opportunities</h2>
              <div className="space-y-4">
                {marketOpportunities.map((opportunity, index) => (
                  <div key={index} className="flex items-start space-x-3">
                    <div className="flex-shrink-0 w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center mt-1">
                      <ArrowUpRight className="text-blue-600" size={12} />
                    </div>
                    <p className="text-gray-700">{opportunity}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Research Methodology */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-lg p-8 shadow-md">
            <div className="flex items-center space-x-3 mb-6">
              <AlertCircle className="text-blue-600" size={24} />
              <h2 className="text-2xl font-bold text-gray-900">Research Methodology & Sources</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Data Sources</h3>
                <ul className="space-y-2 text-gray-700">
                  <li>• Industry reports and market research studies</li>
                  <li>• Competitor analysis and platform data</li>
                  <li>• Census and demographic data analysis</li>
                  <li>• Technology adoption surveys</li>
                  <li>• Local business engagement patterns</li>
                </ul>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Confidence Levels</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-700">Market Size Claims</span>
                    <span className="font-semibold text-green-600">85%+ High</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-700">Growth Projections</span>
                    <span className="font-semibold text-blue-600">75%+ Medium-High</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-700">Competitive Analysis</span>
                    <span className="font-semibold text-green-600">90%+ Very High</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default MarketResearch
