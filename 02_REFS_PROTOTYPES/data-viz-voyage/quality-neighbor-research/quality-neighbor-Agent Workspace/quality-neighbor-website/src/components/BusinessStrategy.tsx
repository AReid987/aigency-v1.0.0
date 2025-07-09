import { useEffect, useState } from 'react'
import { Target, TrendingUp, DollarSign, Users, Calendar, ArrowRight, CheckCircle, BarChart3, Lightbulb } from 'lucide-react'

const BusinessStrategy = () => {
  const [strategyData, setStrategyData] = useState<any>(null)
  const [activePhase, setActivePhase] = useState(0)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadData = async () => {
      try {
        const response = await fetch('/data/quality_neighbor_final_research_summary.json')
        const strategyResponse = await fetch('/data/community_platform_market_analysis.json')
        
        const data = await response.json()
        const strategy = await strategyResponse.json()
        
        setStrategyData({ ...data, ...strategy })
        setLoading(false)
      } catch (error) {
        console.error('Error loading strategy data:', error)
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

  const leanCanvasData = {
    problem: [
      'Information Fragmentation',
      'Content Quality Concerns',
      'Platform Fatigue',
      'Time Constraints',
      'Local Business Connection Challenges'
    ],
    solution: [
      'Professional Newsletter Platform',
      'Local Business Directory',
      'Community Calendar',
      'Emergency Alert System',
      'Content Curation System'
    ],
    uniqueValueProposition: '"Your Community, Professionally Delivered"',
    unfairAdvantage: [
      'Professional Editorial Approach',
      'Community-Specific Focus',
      'Newsletter Format Expertise',
      'Business Integration Model',
      '"Anti-Social Media" Positioning'
    ],
    customerSegments: [
      'Growing Families (40%)',
      'Empty Nesters (25%)',
      'Community Leaders (15%)',
      'Young Professionals (20%)'
    ],
    keyMetrics: [
      'Subscriber Growth: 15%+ monthly',
      'Household Penetration: 60%+ per community',
      'Email Open Rate: 45%+ (vs. 37.67% industry avg)',
      'Monthly Recurring Revenue: $2,500 (M6) to $15,000 (M18)'
    ],
    revenueStreams: [
      'Basic Business Listings: $50/month',
      'Featured Business Listings: $150/month',
      'Newsletter Sponsorships: $500/month',
      'Premium Partnerships: $1,000/month'
    ],
    costStructure: [
      'Content Creation & Curation',
      'Platform Development & Maintenance',
      'Community Acquisition & Onboarding',
      'Business Development & Sales',
      'Technology Infrastructure'
    ],
    channels: [
      'Direct Community Outreach',
      'HOA Partnerships',
      'Local Business Networks',
      'Word-of-Mouth Referrals',
      'Digital Marketing'
    ]
  }

  const gtmPhases = [
    {
      name: 'Foundation',
      timeline: 'Months 1-6',
      budget: '$90,000-$130,000',
      objectives: [
        'Establish product-market fit in Hartland Ranch',
        'Validate core value proposition',
        'Build initial local business relationships',
        'Create replicable community engagement model'
      ],
      keyMetrics: [
        '60% household penetration',
        '10+ paying business partners',
        '$2,500 MRR by Month 6'
      ],
      color: 'bg-blue-50 border-blue-200 text-blue-600'
    },
    {
      name: 'Expansion',
      timeline: 'Months 7-18',
      budget: '$400,000-$600,000',
      objectives: [
        'Expand to 5+ similar communities',
        'Scale and optimize revenue model',
        'Develop feature enhancements',
        'Establish repeatable onboarding'
      ],
      keyMetrics: [
        '5+ active communities',
        '50+ total business partners',
        '$15,000 MRR by Month 18'
      ],
      color: 'bg-green-50 border-green-200 text-green-600'
    },
    {
      name: 'Scale',
      timeline: 'Months 19-36',
      budget: '$1,000,000-$1,500,000',
      objectives: [
        'Accelerate regional expansion',
        'Implement platform scalability',
        'Develop strategic partnerships',
        'Explore advanced monetization'
      ],
      keyMetrics: [
        '20+ active communities',
        '200+ business relationships',
        '$40,000+ MRR by Month 36'
      ],
      color: 'bg-purple-50 border-purple-200 text-purple-600'
    }
  ]

  const marketingChannels = {
    'growing_families': {
      title: 'Growing Families',
      channels: ['Mobile-optimized email', 'Text alerts', 'HOA events'],
      strategy: 'Focus on safety, schools, and family-friendly content'
    },
    'empty_nesters': {
      title: 'Empty Nesters',
      channels: ['Email newsletters', 'Traditional mail', 'Community events'],
      strategy: 'Emphasize community involvement and local business connections'
    },
    'community_leaders': {
      title: 'Community Leaders',
      channels: ['Email', 'HOA meetings', 'Leadership networks'],
      strategy: 'Provide tools for community organization and governance'
    },
    'business_acquisition': {
      title: 'Business Acquisition',
      channels: ['Direct outreach', 'Chamber partnerships', 'Success showcases'],
      strategy: 'Demonstrate clear ROI and category exclusivity benefits'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">Business Strategy Framework</h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Comprehensive Lean Canvas model, Go-to-Market strategy, and marketing framework 
              for Quality Neighbor's scalable growth
            </p>
          </div>
        </div>
      </section>

      {/* Strategic Overview */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Strategic Positioning</h2>
            <div className="bg-blue-50 rounded-lg p-8 max-w-4xl mx-auto">
              <h3 className="text-2xl font-bold text-blue-900 mb-4">
                "Your Community, Professionally Delivered"
              </h3>
              <p className="text-lg text-blue-800">
                Quality Neighbor is the professional community newsletter platform that delivers trusted, 
                relevant local information to residential developments without the noise and negativity of social media.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Lean Canvas */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">Lean Canvas Model</h2>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Problems */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <Target className="mr-2 text-red-600" size={20} />
                Problems
              </h3>
              <ul className="space-y-2">
                {leanCanvasData.problem.map((problem, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-red-500 mr-2">•</span>
                    <span className="text-gray-700">{problem}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Solution */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <Lightbulb className="mr-2 text-green-600" size={20} />
                Solution
              </h3>
              <ul className="space-y-2">
                {leanCanvasData.solution.map((solution, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-green-500 mr-2">•</span>
                    <span className="text-gray-700">{solution}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Value Proposition */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <TrendingUp className="mr-2 text-blue-600" size={20} />
                Value Proposition
              </h3>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600 mb-4">
                  {leanCanvasData.uniqueValueProposition}
                </div>
                <div className="space-y-2">
                  {leanCanvasData.unfairAdvantage.map((advantage, index) => (
                    <div key={index} className="text-sm text-gray-600">
                      {advantage}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Customer Segments */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <Users className="mr-2 text-purple-600" size={20} />
                Customer Segments
              </h3>
              <ul className="space-y-2">
                {leanCanvasData.customerSegments.map((segment, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-purple-500 mr-2">•</span>
                    <span className="text-gray-700">{segment}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Revenue Streams */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <DollarSign className="mr-2 text-green-600" size={20} />
                Revenue Streams
              </h3>
              <ul className="space-y-2">
                {leanCanvasData.revenueStreams.map((stream, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-green-500 mr-2">•</span>
                    <span className="text-gray-700">{stream}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Key Metrics */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <BarChart3 className="mr-2 text-blue-600" size={20} />
                Key Metrics
              </h3>
              <ul className="space-y-2">
                {leanCanvasData.keyMetrics.map((metric, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-blue-500 mr-2">•</span>
                    <span className="text-gray-700 text-sm">{metric}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Go-to-Market Strategy */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">Go-to-Market Strategy</h2>
          
          {/* Phase Selection */}
          <div className="flex flex-wrap justify-center gap-4 mb-12">
            {gtmPhases.map((phase, index) => (
              <button
                key={index}
                onClick={() => setActivePhase(index)}
                className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                  activePhase === index
                    ? phase.color + ' border-2'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {phase.name}
              </button>
            ))}
          </div>

          {/* Active Phase Details */}
          <div className="bg-white border border-gray-200 rounded-lg p-8 shadow-md">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">
                  Phase {activePhase + 1}: {gtmPhases[activePhase].name}
                </h3>
                <div className="space-y-4">
                  <div className="flex items-center space-x-2">
                    <Calendar className="text-blue-600" size={20} />
                    <span className="font-semibold">Timeline:</span>
                    <span>{gtmPhases[activePhase].timeline}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <DollarSign className="text-green-600" size={20} />
                    <span className="font-semibold">Budget:</span>
                    <span>{gtmPhases[activePhase].budget}</span>
                  </div>
                </div>
                
                <h4 className="text-lg font-semibold text-gray-900 mt-6 mb-3">Objectives</h4>
                <ul className="space-y-2">
                  {gtmPhases[activePhase].objectives.map((objective, index) => (
                    <li key={index} className="flex items-start">
                      <CheckCircle className="text-green-500 mr-2 mt-1 flex-shrink-0" size={16} />
                      <span className="text-gray-700">{objective}</span>
                    </li>
                  ))}
                </ul>
              </div>
              
              <div>
                <h4 className="text-lg font-semibold text-gray-900 mb-4">Key Success Metrics</h4>
                <div className="space-y-4">
                  {gtmPhases[activePhase].keyMetrics.map((metric, index) => (
                    <div key={index} className="bg-gray-50 rounded-lg p-4">
                      <div className="flex items-center justify-between">
                        <span className="text-gray-700">{metric}</span>
                        <CheckCircle className="text-green-500" size={16} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Phase Timeline */}
          <div className="mt-12">
            <div className="flex justify-between items-center bg-gray-100 rounded-lg p-6">
              {gtmPhases.map((phase, index) => (
                <div key={index} className="flex items-center">
                  <div className={`w-12 h-12 rounded-full flex items-center justify-center font-bold ${
                    index <= activePhase ? 'bg-blue-600 text-white' : 'bg-gray-300 text-gray-600'
                  }`}>
                    {index + 1}
                  </div>
                  <div className="ml-3">
                    <div className="font-semibold text-gray-900">{phase.name}</div>
                    <div className="text-sm text-gray-600">{phase.timeline}</div>
                  </div>
                  {index < gtmPhases.length - 1 && (
                    <ArrowRight className="ml-6 text-gray-400" size={20} />
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Marketing Framework */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">Marketing Channel Strategy</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {Object.entries(marketingChannels).map(([key, channel]) => (
              <div key={key} className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">{channel.title}</h3>
                <div className="mb-4">
                  <h4 className="font-medium text-gray-900 mb-2">Channels:</h4>
                  <div className="flex flex-wrap gap-2">
                    {channel.channels.map((ch, index) => (
                      <span key={index} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                        {ch}
                      </span>
                    ))}
                  </div>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Strategy:</h4>
                  <p className="text-gray-700 text-sm">{channel.strategy}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Revenue Projections */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">Revenue Growth Trajectory</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-6 bg-blue-50 rounded-lg">
              <div className="text-3xl font-bold text-blue-600 mb-2">$2.5K</div>
              <div className="text-lg font-semibold text-gray-900 mb-2">Month 6 MRR</div>
              <div className="text-sm text-gray-600">1 community, 10+ business partners</div>
            </div>
            <div className="text-center p-6 bg-green-50 rounded-lg">
              <div className="text-3xl font-bold text-green-600 mb-2">$15K</div>
              <div className="text-lg font-semibold text-gray-900 mb-2">Month 18 MRR</div>
              <div className="text-sm text-gray-600">5+ communities, 50+ business partners</div>
            </div>
            <div className="text-center p-6 bg-purple-50 rounded-lg">
              <div className="text-3xl font-bold text-purple-600 mb-2">$40K+</div>
              <div className="text-lg font-semibold text-gray-900 mb-2">Month 36 MRR</div>
              <div className="text-sm text-gray-600">20+ communities, 200+ business partners</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default BusinessStrategy
