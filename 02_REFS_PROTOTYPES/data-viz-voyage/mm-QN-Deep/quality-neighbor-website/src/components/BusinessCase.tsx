import { useEffect, useState } from 'react'
import { Line, Bar, Doughnut } from 'react-chartjs-2'
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
import { DollarSign, TrendingUp, AlertTriangle, CheckCircle, Target, BarChart3, PieChart, Calendar } from 'lucide-react'

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

const BusinessCase = () => {
  const [activeTab, setActiveTab] = useState('revenue')

  // Revenue projections data
  const revenueProjectionData = {
    labels: ['Month 6', 'Month 12', 'Month 18', 'Month 24', 'Month 30', 'Month 36'],
    datasets: [
      {
        label: 'Monthly Recurring Revenue ($)',
        data: [2500, 7500, 15000, 25000, 32000, 40000],
        borderColor: '#3B82F6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.4,
      },
    ],
  }

  // Revenue breakdown by stream
  const revenueBreakdownData = {
    labels: ['Basic Listings', 'Featured Listings', 'Newsletter Sponsorships', 'Premium Partnerships'],
    datasets: [
      {
        data: [30, 25, 25, 20],
        backgroundColor: ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6'],
        borderWidth: 0,
      },
    ],
  }

  // Cost structure over time
  const costStructureData = {
    labels: ['Year 1', 'Year 2', 'Year 3'],
    datasets: [
      {
        label: 'Revenue',
        data: [120000, 300000, 480000],
        backgroundColor: '#10B981',
      },
      {
        label: 'Operating Costs',
        data: [80000, 180000, 240000],
        backgroundColor: '#F59E0B',
      },
      {
        label: 'Net Profit',
        data: [40000, 120000, 240000],
        backgroundColor: '#3B82F6',
      },
    ],
  }

  const financialProjections = [
    {
      metric: 'Year 1 Revenue',
      value: '$120K',
      description: 'Based on 1-2 communities with 15+ business partners',
      trend: '+300% from launch',
      color: 'text-blue-600 bg-blue-50'
    },
    {
      metric: 'Year 2 Revenue',
      value: '$300K',
      description: 'Expansion to 5+ communities with 75+ business partners',
      trend: '+150% YoY growth',
      color: 'text-green-600 bg-green-50'
    },
    {
      metric: 'Year 3 Revenue',
      value: '$480K',
      description: 'Scale to 20+ communities with 200+ business partners',
      trend: '+60% YoY growth',
      color: 'text-purple-600 bg-purple-50'
    },
    {
      metric: 'Break-even Point',
      value: 'Month 8',
      description: 'Positive cash flow with 2 communities operational',
      trend: 'Faster than projected',
      color: 'text-orange-600 bg-orange-50'
    }
  ]

  const revenueStreams = [
    {
      stream: 'Local Business Listings',
      tier: 'Basic ($50/month)',
      description: 'Essential directory presence with contact information',
      marketSize: '200+ businesses per community',
      penetration: '15%',
      monthlyPotential: '$1,500'
    },
    {
      stream: 'Featured Business Listings',
      tier: 'Enhanced ($150/month)',
      description: 'Premium placement with analytics and promotional content',
      marketSize: '200+ businesses per community',
      penetration: '8%',
      monthlyPotential: '$2,400'
    },
    {
      stream: 'Newsletter Sponsorships',
      tier: 'Sponsored ($500/month)',
      description: 'Dedicated newsletter sections and content integration',
      marketSize: '50+ businesses per community',
      penetration: '10%',
      monthlyPotential: '$2,500'
    },
    {
      stream: 'Premium Partnerships',
      tier: 'Exclusive ($1,000/month)',
      description: 'Category exclusivity with multi-platform prominence',
      marketSize: '20+ categories per community',
      penetration: '25%',
      monthlyPotential: '$5,000'
    }
  ]

  const riskAssessment = [
    {
      risk: 'Competition from established platforms',
      impact: 'High',
      probability: 'Medium',
      mitigation: 'Strong differentiation through professional newsletter format and local business integration',
      status: 'Mitigated'
    },
    {
      risk: 'Local business budget constraints',
      impact: 'Medium',
      probability: 'Medium',
      mitigation: 'Flexible pricing tiers and clear ROI demonstration with performance tracking',
      status: 'Managed'
    },
    {
      risk: 'Community adoption challenges',
      impact: 'High',
      probability: 'Low',
      mitigation: 'HOA partnerships, professional content quality, and proven newsletter format appeal',
      status: 'Low Risk'
    },
    {
      risk: 'Technology scaling requirements',
      impact: 'Medium',
      probability: 'Medium',
      mitigation: 'Cloud infrastructure, modular architecture, and phased development approach',
      status: 'Planned'
    }
  ]

  const successFactors = [
    {
      factor: 'Product-Market Fit Validation',
      description: 'Demonstrated demand for professional community newsletters with local business integration',
      evidence: ['96% YoY newsletter growth', '80% homeowner app usage', '37.67% newsletter open rates'],
      status: 'Validated'
    },
    {
      factor: 'Revenue Model Viability',
      description: 'Multiple revenue streams with proven local advertising demand and clear business value',
      evidence: ['$300K annual revenue benchmarks', 'Local business advertising needs', 'Category exclusivity appeal'],
      status: 'Proven'
    },
    {
      factor: 'Scalable Technology Platform',
      description: 'Multi-community architecture with automated content creation and management systems',
      evidence: ['Cloud-native infrastructure', 'Multi-agent content system', 'API-first design'],
      status: 'Designed'
    },
    {
      factor: 'Market Opportunity Size',
      description: 'Large addressable market with strong growth trajectory and underserved segments',
      evidence: ['$1.2-2.5B market size', '16.2% CAGR growth', 'Residential development expansion'],
      status: 'Confirmed'
    }
  ]

  const implementationMilestones = [
    {
      milestone: 'MVP Launch',
      timeline: 'Month 3',
      budget: '$150K',
      success_criteria: ['Platform operational', 'First community onboarded', '5+ business partners'],
      risk_level: 'Low'
    },
    {
      milestone: 'Product-Market Fit',
      timeline: 'Month 6',
      budget: '$250K',
      success_criteria: ['60% household penetration', '10+ business partners', '$2.5K MRR'],
      risk_level: 'Medium'
    },
    {
      milestone: 'Multi-Community Scale',
      timeline: 'Month 12',
      budget: '$500K',
      success_criteria: ['3+ communities active', '30+ business partners', '$10K MRR'],
      risk_level: 'Medium'
    },
    {
      milestone: 'Regional Expansion',
      timeline: 'Month 24',
      budget: '$1M',
      success_criteria: ['10+ communities active', '100+ business partners', '$25K MRR'],
      risk_level: 'High'
    }
  ]

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'High': return 'bg-red-100 text-red-800'
      case 'Medium': return 'bg-yellow-100 text-yellow-800'
      case 'Low': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Validated': case 'Proven': case 'Confirmed': return 'text-green-600'
      case 'Designed': case 'Planned': return 'text-blue-600'
      case 'Mitigated': case 'Managed': return 'text-orange-600'
      case 'Low Risk': return 'text-green-600'
      default: return 'text-gray-600'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">Business Case & Financial Analysis</h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Comprehensive revenue projections, ROI analysis, and implementation strategy 
              for Quality Neighbor platform investment
            </p>
          </div>
        </div>
      </section>

      {/* Navigation Tabs */}
      <section className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {[
              { id: 'revenue', label: 'Revenue Model', icon: DollarSign },
              { id: 'projections', label: 'Financial Projections', icon: TrendingUp },
              { id: 'risks', label: 'Risk Analysis', icon: AlertTriangle },
              { id: 'implementation', label: 'Implementation Plan', icon: Calendar }
            ].map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-4 px-2 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon size={16} />
                  <span>{tab.label}</span>
                </button>
              )
            })}
          </div>
        </div>
      </section>

      {/* Revenue Model */}
      {activeTab === 'revenue' && (
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">Revenue Model Analysis</h2>
            
            {/* Revenue Streams */}
            <div className="space-y-6 mb-16">
              {revenueStreams.map((stream, index) => (
                <div key={index} className="bg-white rounded-lg shadow-md p-6">
                  <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">{stream.stream}</h3>
                      <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                        {stream.tier}
                      </span>
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900 mb-1">Description</h4>
                      <p className="text-sm text-gray-600">{stream.description}</p>
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900 mb-1">Market & Penetration</h4>
                      <p className="text-sm text-gray-600">{stream.marketSize}</p>
                      <p className="text-sm text-blue-600 font-medium">{stream.penetration} penetration rate</p>
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900 mb-1">Monthly Potential</h4>
                      <p className="text-2xl font-bold text-green-600">{stream.monthlyPotential}</p>
                      <p className="text-xs text-gray-500">per community</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Revenue Breakdown Chart */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Revenue Stream Distribution</h3>
                <Doughnut data={revenueBreakdownData} options={{
                  responsive: true,
                  plugins: {
                    legend: {
                      position: 'bottom',
                    },
                  },
                }} />
              </div>
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Key Revenue Metrics</h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                    <span className="text-gray-700">Average Revenue Per Business</span>
                    <span className="font-semibold text-blue-600">$275/month</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                    <span className="text-gray-700">Target Businesses Per Community</span>
                    <span className="font-semibold text-blue-600">15-20</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                    <span className="text-gray-700">Monthly Revenue Per Community</span>
                    <span className="font-semibold text-green-600">$4,000-5,500</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                    <span className="text-gray-700">Customer Lifetime Value</span>
                    <span className="font-semibold text-purple-600">$9,900</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Financial Projections */}
      {activeTab === 'projections' && (
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">Financial Projections & ROI</h2>
            
            {/* Key Financial Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
              {financialProjections.map((projection, index) => (
                <div key={index} className="bg-white rounded-lg shadow-md p-6">
                  <div className={`w-12 h-12 rounded-lg ${projection.color} flex items-center justify-center mb-4`}>
                    <DollarSign size={24} />
                  </div>
                  <div className="text-3xl font-bold text-gray-900 mb-2">{projection.value}</div>
                  <div className="text-lg font-semibold text-gray-900 mb-2">{projection.metric}</div>
                  <div className="text-gray-600 text-sm mb-3">{projection.description}</div>
                  <div className="text-green-600 text-sm font-medium">{projection.trend}</div>
                </div>
              ))}
            </div>

            {/* Revenue Growth Chart */}
            <div className="bg-white rounded-lg shadow-md p-6 mb-16">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Revenue Growth Trajectory</h3>
              <Line data={revenueProjectionData} options={{
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
                      text: 'Monthly Recurring Revenue ($)'
                    },
                    ticks: {
                      callback: function(value: any) {
                        return '$' + Number(value).toLocaleString();
                      }
                    }
                  }
                }
              }} />
            </div>

            {/* Cost Structure and Profitability */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">3-Year Profitability Analysis</h3>
              <Bar data={costStructureData} options={{
                responsive: true,
                plugins: {
                  legend: {
                    position: 'top',
                  },
                },
                scales: {
                  y: {
                    beginAtZero: true,
                    title: {
                      display: true,
                      text: 'Amount ($)'
                    },
                    ticks: {
                      callback: function(value: any) {
                        return '$' + (Number(value) / 1000) + 'K';
                      }
                    }
                  }
                }
              }} />
            </div>
          </div>
        </section>
      )}

      {/* Risk Analysis */}
      {activeTab === 'risks' && (
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">Risk Assessment & Mitigation</h2>
            
            {/* Risk Matrix */}
            <div className="space-y-6 mb-16">
              {riskAssessment.map((risk, index) => (
                <div key={index} className="bg-white rounded-lg shadow-md p-6">
                  <div className="grid grid-cols-1 lg:grid-cols-5 gap-4 items-center">
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-2">{risk.risk}</h3>
                    </div>
                    <div className="text-center">
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(risk.impact)}`}>
                        {risk.impact} Impact
                      </span>
                    </div>
                    <div className="text-center">
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(risk.probability)}`}>
                        {risk.probability} Probability
                      </span>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">{risk.mitigation}</p>
                    </div>
                    <div className="text-center">
                      <span className={`font-semibold ${getStatusColor(risk.status)}`}>
                        {risk.status}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Success Factors */}
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-8 text-center">Critical Success Factors</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {successFactors.map((factor, index) => (
                  <div key={index} className="bg-white rounded-lg shadow-md p-6">
                    <div className="flex items-center space-x-2 mb-4">
                      <CheckCircle className={`${getStatusColor(factor.status)}`} size={20} />
                      <h4 className="text-lg font-semibold text-gray-900">{factor.factor}</h4>
                    </div>
                    <p className="text-gray-600 mb-4">{factor.description}</p>
                    <div>
                      <h5 className="font-medium text-gray-900 mb-2">Supporting Evidence:</h5>
                      <ul className="space-y-1">
                        {factor.evidence.map((evidence, evidenceIndex) => (
                          <li key={evidenceIndex} className="text-sm text-gray-600 flex items-center">
                            <span className="w-1.5 h-1.5 bg-blue-400 rounded-full mr-2"></span>
                            {evidence}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div className="mt-4">
                      <span className={`font-semibold text-sm ${getStatusColor(factor.status)}`}>
                        Status: {factor.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Implementation Plan */}
      {activeTab === 'implementation' && (
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">Implementation Timeline & Milestones</h2>
            
            {/* Milestone Timeline */}
            <div className="space-y-8 mb-16">
              {implementationMilestones.map((milestone, index) => (
                <div key={index} className="bg-white rounded-lg shadow-md p-6">
                  <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">{milestone.milestone}</h3>
                      <div className="flex items-center space-x-2">
                        <Calendar className="text-blue-600" size={16} />
                        <span className="text-sm text-gray-600">{milestone.timeline}</span>
                      </div>
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900 mb-1">Budget</h4>
                      <p className="text-lg font-bold text-green-600">{milestone.budget}</p>
                    </div>
                    <div className="lg:col-span-2">
                      <h4 className="font-medium text-gray-900 mb-2">Success Criteria</h4>
                      <ul className="space-y-1">
                        {milestone.success_criteria.map((criteria, criteriaIndex) => (
                          <li key={criteriaIndex} className="text-sm text-gray-600 flex items-center">
                            <CheckCircle className="text-green-500 mr-2 flex-shrink-0" size={14} />
                            {criteria}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div className="text-center">
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(milestone.risk_level)}`}>
                        {milestone.risk_level} Risk
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Investment Summary */}
            <div className="bg-blue-50 rounded-lg p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">Investment Summary</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600 mb-2">$1.9M</div>
                  <div className="text-lg font-semibold text-gray-900 mb-1">Total Investment</div>
                  <div className="text-sm text-gray-600">Over 24 months</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600 mb-2">$480K</div>
                  <div className="text-lg font-semibold text-gray-900 mb-1">Year 3 Revenue</div>
                  <div className="text-sm text-gray-600">$40K+ MRR by Month 36</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600 mb-2">18 months</div>
                  <div className="text-lg font-semibold text-gray-900 mb-1">Payback Period</div>
                  <div className="text-sm text-gray-600">Break-even by Month 8</div>
                </div>
              </div>
            </div>
          </div>
        </section>
      )}
    </div>
  )
}

export default BusinessCase
