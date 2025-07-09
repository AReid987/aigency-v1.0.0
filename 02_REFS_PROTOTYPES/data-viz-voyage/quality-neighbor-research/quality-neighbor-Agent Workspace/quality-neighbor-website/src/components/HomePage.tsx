import { Link } from 'react-router-dom'
import { ArrowRight, TrendingUp, Users, Target, Cog, Palette, DollarSign, CheckCircle, BarChart3 } from 'lucide-react'

const HomePage = () => {
  const keyMetrics = [
    { label: 'Market Size', value: '$1.2-2.5B', description: 'Growing community platform market' },
    { label: 'Newsletter Growth', value: '96% YoY', description: 'Industry growth rate' },
    { label: 'Target Communities', value: '20+', description: 'By Month 36' },
    { label: 'Revenue Projection', value: '$40K+ MRR', description: 'Month 36 target' }
  ]

  const researchSections = [
    {
      title: 'Market Research',
      description: 'Comprehensive analysis of the $1.2-2.5B community platform market with 96% YoY newsletter growth',
      path: '/market-research',
      icon: TrendingUp,
      color: 'bg-blue-50 text-blue-600',
      highlights: ['Market Size Analysis', 'Competitive Landscape', 'Growth Projections']
    },
    {
      title: 'User Personas',
      description: 'Deep dive into 4 key user segments with detailed personas and journey mapping',
      path: '/user-personas',
      icon: Users,
      color: 'bg-green-50 text-green-600',
      highlights: ['Growing Families', 'Empty Nesters', 'Community Leaders']
    },
    {
      title: 'Business Strategy',
      description: 'Complete Lean Canvas, GTM strategy, and marketing framework for scalable growth',
      path: '/business-strategy',
      icon: Target,
      color: 'bg-purple-50 text-purple-600',
      highlights: ['Lean Canvas Model', '3-Phase GTM Strategy', 'Marketing Framework']
    },
    {
      title: 'Product Development',
      description: 'Comprehensive PRD, system architecture, and multi-agent content creation system',
      path: '/product-development',
      icon: Cog,
      color: 'bg-orange-50 text-orange-600',
      highlights: ['Product Requirements', 'System Architecture', 'Technical Roadmap']
    },
    {
      title: 'Branding & Design',
      description: 'Complete brand identity, voice guidelines, and atomic design system',
      path: '/branding-design',
      icon: Palette,
      color: 'bg-pink-50 text-pink-600',
      highlights: ['Brand Positioning', 'Design System', 'Voice Guidelines']
    },
    {
      title: 'Business Case',
      description: 'Revenue projections, ROI analysis, and comprehensive implementation strategy',
      path: '/business-case',
      icon: DollarSign,
      color: 'bg-yellow-50 text-yellow-600',
      highlights: ['Revenue Model', 'Financial Projections', 'Risk Assessment']
    }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-blue-600 via-blue-700 to-blue-800 text-white">
        <div className="absolute inset-0 bg-black opacity-20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h1 className="text-5xl font-bold mb-6">
                Quality Neighbor
                <span className="block text-blue-200">Market Research & Strategy</span>
              </h1>
              <p className="text-xl mb-8 text-blue-100 leading-relaxed">
                Comprehensive market research and product development strategy for the professional community newsletter platform 
                serving residential developments.
              </p>
              <div className="flex items-center space-x-2 mb-8">
                <CheckCircle className="text-green-400" size={20} />
                <span className="text-lg">"Your Community, Professionally Delivered"</span>
              </div>
              <div className="flex flex-col sm:flex-row gap-4">
                <Link 
                  to="/market-research" 
                  className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-blue-50 transition-colors flex items-center justify-center"
                >
                  Explore Research
                  <ArrowRight className="ml-2" size={20} />
                </Link>
                <Link 
                  to="/business-strategy" 
                  className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors flex items-center justify-center"
                >
                  View Strategy
                  <Target className="ml-2" size={20} />
                </Link>
              </div>
            </div>
            <div className="hidden lg:block">
              <img 
                src="/images/community_hero.jpg" 
                alt="Community Newsletter Platform" 
                className="rounded-lg shadow-2xl"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Key Metrics */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Key Research Findings</h2>
            <p className="text-lg text-gray-600">Evidence-based insights driving our strategic recommendations</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {keyMetrics.map((metric, index) => (
              <div key={index} className="text-center p-6 bg-gray-50 rounded-lg">
                <div className="text-3xl font-bold text-blue-600 mb-2">{metric.value}</div>
                <div className="text-lg font-semibold text-gray-900 mb-1">{metric.label}</div>
                <div className="text-sm text-gray-600">{metric.description}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Research Sections */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Comprehensive Research & Strategy</h2>
            <p className="text-lg text-gray-600">Explore detailed analysis across all areas of market research and product development</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {researchSections.map((section, index) => {
              const Icon = section.icon
              return (
                <div key={index} className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
                  <div className="p-6">
                    <div className={`w-12 h-12 rounded-lg ${section.color} flex items-center justify-center mb-4`}>
                      <Icon size={24} />
                    </div>
                    <h3 className="text-xl font-bold text-gray-900 mb-3">{section.title}</h3>
                    <p className="text-gray-600 mb-4">{section.description}</p>
                    <ul className="space-y-2 mb-6">
                      {section.highlights.map((highlight, idx) => (
                        <li key={idx} className="flex items-center text-sm text-gray-700">
                          <CheckCircle size={16} className="text-green-500 mr-2 flex-shrink-0" />
                          {highlight}
                        </li>
                      ))}
                    </ul>
                    <Link 
                      to={section.path}
                      className="inline-flex items-center text-blue-600 font-semibold hover:text-blue-800 transition-colors"
                    >
                      Explore Details
                      <ArrowRight size={16} className="ml-2" />
                    </Link>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Strategic Overview */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">Strategic Positioning</h2>
              <div className="space-y-6">
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Market Opportunity</h3>
                  <p className="text-gray-700">
                    Quality Neighbor addresses a growing $1.2-2.5B market with 96% YoY newsletter growth, 
                    positioning as the professional alternative to social media chaos.
                  </p>
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Target Market</h3>
                  <p className="text-gray-700">
                    Residential developments and planned communities, focusing on homeowners who value 
                    professional community communication over social media platforms.
                  </p>
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Revenue Model</h3>
                  <p className="text-gray-700">
                    Multi-tiered business partnerships ($50-$1,000/month) with local businesses, 
                    targeting $40K+ MRR by Month 36 across 20+ communities.
                  </p>
                </div>
              </div>
            </div>
            <div className="bg-gray-50 rounded-lg p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">Growth Trajectory</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-white rounded-lg">
                  <div>
                    <div className="font-semibold text-gray-900">Phase 1: Foundation</div>
                    <div className="text-sm text-gray-600">Months 1-6</div>
                  </div>
                  <div className="text-right">
                    <div className="font-bold text-blue-600">$2.5K MRR</div>
                    <div className="text-sm text-gray-600">1 community</div>
                  </div>
                </div>
                <div className="flex items-center justify-between p-4 bg-white rounded-lg">
                  <div>
                    <div className="font-semibold text-gray-900">Phase 2: Expansion</div>
                    <div className="text-sm text-gray-600">Months 7-18</div>
                  </div>
                  <div className="text-right">
                    <div className="font-bold text-blue-600">$15K MRR</div>
                    <div className="text-sm text-gray-600">5+ communities</div>
                  </div>
                </div>
                <div className="flex items-center justify-between p-4 bg-white rounded-lg">
                  <div>
                    <div className="font-semibold text-gray-900">Phase 3: Scale</div>
                    <div className="text-sm text-gray-600">Months 19-36</div>
                  </div>
                  <div className="text-right">
                    <div className="font-bold text-blue-600">$40K+ MRR</div>
                    <div className="text-sm text-gray-600">20+ communities</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-16 bg-blue-600 text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Explore the Complete Strategy?</h2>
          <p className="text-xl text-blue-100 mb-8">
            Dive deep into our comprehensive research, user analysis, business strategy, and technical specifications.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              to="/market-research" 
              className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-blue-50 transition-colors flex items-center justify-center"
            >
              <BarChart3 className="mr-2" size={20} />
              Start with Market Research
            </Link>
            <Link 
              to="/business-strategy" 
              className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors flex items-center justify-center"
            >
              <Target className="mr-2" size={20} />
              View Business Strategy
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}

export default HomePage
