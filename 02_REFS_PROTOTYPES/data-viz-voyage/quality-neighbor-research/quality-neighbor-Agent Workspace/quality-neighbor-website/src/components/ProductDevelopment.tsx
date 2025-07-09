import { useState } from 'react'
import { Cog, Database, Cloud, Shield, Zap, Code, ArrowRight, CheckCircle, Layers, GitBranch, Users, Bell, Calendar, MapPin, DollarSign } from 'lucide-react'

const ProductDevelopment = () => {
  const [activeTab, setActiveTab] = useState('prd')

  const productFeatures = [
    {
      category: 'Core Newsletter Platform',
      features: [
        { name: 'Professional Newsletter Creation', priority: 'High', status: 'MVP' },
        { name: 'Content Curation System', priority: 'High', status: 'MVP' },
        { name: 'Email Distribution Engine', priority: 'High', status: 'MVP' },
        { name: 'Mobile-Optimized Reading Experience', priority: 'High', status: 'MVP' }
      ]
    },
    {
      category: 'Business Integration',
      features: [
        { name: 'Local Business Directory', priority: 'High', status: 'MVP' },
        { name: 'Business Listing Management', priority: 'High', status: 'MVP' },
        { name: 'Advertising Integration', priority: 'Medium', status: 'Phase 2' },
        { name: 'Performance Analytics Dashboard', priority: 'Medium', status: 'Phase 2' }
      ]
    },
    {
      category: 'Community Features',
      features: [
        { name: 'Community Event Calendar', priority: 'Medium', status: 'Phase 2' },
        { name: 'Emergency Alert System', priority: 'High', status: 'MVP' },
        { name: 'Neighbor Spotlight Feature', priority: 'Low', status: 'Phase 3' },
        { name: 'Community Marketplace', priority: 'Low', status: 'Phase 3' }
      ]
    },
    {
      category: 'Platform Management',
      features: [
        { name: 'Multi-Community Management', priority: 'High', status: 'Phase 2' },
        { name: 'Content Approval Workflow', priority: 'Medium', status: 'Phase 2' },
        { name: 'User Role Management', priority: 'Medium', status: 'Phase 2' },
        { name: 'Analytics & Reporting Suite', priority: 'High', status: 'Phase 2' }
      ]
    }
  ]

  const systemArchitecture = {
    frontend: {
      title: 'Frontend Layer',
      components: ['React Web App', 'Mobile-Optimized Newsletter', 'Admin Dashboard', 'Business Portal'],
      technologies: ['React 18', 'TypeScript', 'Tailwind CSS', 'PWA Support']
    },
    backend: {
      title: 'Backend Services',
      components: ['API Gateway', 'Content Management', 'Email Service', 'User Management'],
      technologies: ['Node.js', 'Express.js', 'PostgreSQL', 'Redis Cache']
    },
    infrastructure: {
      title: 'Infrastructure',
      components: ['Cloud Hosting', 'CDN', 'Load Balancers', 'Monitoring'],
      technologies: ['AWS/Azure', 'CloudFront', 'Docker', 'Kubernetes']
    },
    integrations: {
      title: 'Third-Party Integrations',
      components: ['Email Service Provider', 'Payment Processing', 'Analytics', 'CRM Systems'],
      technologies: ['SendGrid/Mailgun', 'Stripe', 'Google Analytics', 'HubSpot/Salesforce']
    }
  }

  const multiAgentSystem = {
    contentAgent: {
      name: 'Content Creation Agent',
      description: 'AI-powered content generation and curation',
      capabilities: ['Article writing', 'Content summarization', 'Local news aggregation', 'SEO optimization'],
      icon: Code
    },
    businessAgent: {
      name: 'Business Integration Agent',
      description: 'Local business content and advertising management',
      capabilities: ['Business profile creation', 'Promotional content generation', 'Review summarization', 'Event promotion'],
      icon: Cog
    },
    moderationAgent: {
      name: 'Content Moderation Agent',
      description: 'Quality control and content approval',
      capabilities: ['Content quality assessment', 'Community guidelines enforcement', 'Spam detection', 'Fact-checking'],
      icon: Shield
    },
    analyticsAgent: {
      name: 'Analytics & Optimization Agent',
      description: 'Performance monitoring and optimization',
      capabilities: ['Engagement analytics', 'A/B testing', 'Content optimization', 'Revenue tracking'],
      icon: Layers
    }
  }

  const technicalRoadmap = [
    {
      phase: 'MVP Development',
      timeline: 'Months 1-3',
      budget: '$150K-200K',
      deliverables: [
        'Core newsletter platform',
        'Basic business directory',
        'Email distribution system',
        'Admin dashboard'
      ]
    },
    {
      phase: 'Platform Enhancement',
      timeline: 'Months 4-9',
      budget: '$300K-400K',
      deliverables: [
        'Multi-community support',
        'Advanced analytics',
        'Mobile app development',
        'API ecosystem'
      ]
    },
    {
      phase: 'Scale & Automation',
      timeline: 'Months 10-18',
      budget: '$500K-700K',
      deliverables: [
        'Multi-agent content system',
        'Advanced AI features',
        'Enterprise integrations',
        'Platform scaling infrastructure'
      ]
    }
  ]

  const userStories = [
    {
      persona: 'Community Member',
      story: 'As a community member, I want to receive a weekly newsletter with relevant local information so that I stay informed about my neighborhood.',
      acceptance: ['Newsletter delivered weekly', 'Content is relevant and local', 'Easy to read on mobile', 'Unsubscribe option available']
    },
    {
      persona: 'Local Business Owner',
      story: 'As a local business owner, I want to create and manage my business listing so that community members can discover my services.',
      acceptance: ['Easy business profile creation', 'Ability to update information', 'Performance analytics', 'Multiple pricing tiers']
    },
    {
      persona: 'Community Leader',
      story: 'As a community leader, I want to promote community events and important announcements so that residents stay engaged.',
      acceptance: ['Event creation interface', 'Emergency alert capability', 'Content approval workflow', 'Engagement tracking']
    },
    {
      persona: 'Platform Administrator',
      story: 'As a platform administrator, I want to manage multiple communities efficiently so that I can scale the platform effectively.',
      acceptance: ['Multi-community dashboard', 'Bulk content management', 'User role management', 'Revenue tracking']
    }
  ]

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'High': return 'bg-red-100 text-red-800'
      case 'Medium': return 'bg-yellow-100 text-yellow-800'
      case 'Low': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'MVP': return 'bg-blue-100 text-blue-800'
      case 'Phase 2': return 'bg-purple-100 text-purple-800'
      case 'Phase 3': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">Product Development & Technical Architecture</h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Comprehensive PRD, system architecture, and multi-agent content creation system 
              for Quality Neighbor platform development
            </p>
          </div>
        </div>
      </section>

      {/* Navigation Tabs */}
      <section className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {[
              { id: 'prd', label: 'Product Requirements', icon: Cog },
              { id: 'architecture', label: 'System Architecture', icon: Database },
              { id: 'agents', label: 'Multi-Agent System', icon: GitBranch },
              { id: 'roadmap', label: 'Technical Roadmap', icon: Calendar }
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

      {/* Product Requirements Document */}
      {activeTab === 'prd' && (
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">Product Requirements Document</h2>
            
            {/* Feature Categories */}
            <div className="space-y-8">
              {productFeatures.map((category, categoryIndex) => (
                <div key={categoryIndex} className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-xl font-semibold text-gray-900 mb-6">{category.category}</h3>
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead>
                        <tr className="border-b border-gray-200">
                          <th className="text-left py-3 px-4 font-medium text-gray-900">Feature</th>
                          <th className="text-left py-3 px-4 font-medium text-gray-900">Priority</th>
                          <th className="text-left py-3 px-4 font-medium text-gray-900">Development Phase</th>
                        </tr>
                      </thead>
                      <tbody>
                        {category.features.map((feature, featureIndex) => (
                          <tr key={featureIndex} className="border-b border-gray-100">
                            <td className="py-3 px-4 text-gray-700">{feature.name}</td>
                            <td className="py-3 px-4">
                              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(feature.priority)}`}>
                                {feature.priority}
                              </span>
                            </td>
                            <td className="py-3 px-4">
                              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(feature.status)}`}>
                                {feature.status}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              ))}
            </div>

            {/* User Stories */}
            <div className="mt-16">
              <h3 className="text-2xl font-bold text-gray-900 mb-8 text-center">Key User Stories</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {userStories.map((story, index) => (
                  <div key={index} className="bg-white rounded-lg shadow-md p-6">
                    <div className="flex items-center space-x-2 mb-4">
                      <Users className="text-blue-600" size={20} />
                      <h4 className="font-semibold text-gray-900">{story.persona}</h4>
                    </div>
                    <p className="text-gray-700 mb-4 italic">"{story.story}"</p>
                    <div>
                      <h5 className="font-medium text-gray-900 mb-2">Acceptance Criteria:</h5>
                      <ul className="space-y-1">
                        {story.acceptance.map((criteria, criteriaIndex) => (
                          <li key={criteriaIndex} className="flex items-center text-sm text-gray-600">
                            <CheckCircle className="text-green-500 mr-2 flex-shrink-0" size={14} />
                            {criteria}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* System Architecture */}
      {activeTab === 'architecture' && (
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">System Architecture Overview</h2>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
              {Object.entries(systemArchitecture).map(([key, layer]) => {
                const icons = {
                  frontend: Code,
                  backend: Database,
                  infrastructure: Cloud,
                  integrations: Zap
                }
                const Icon = icons[key as keyof typeof icons]
                
                return (
                  <div key={key} className="bg-white rounded-lg shadow-md p-6">
                    <div className="flex items-center space-x-2 mb-4">
                      <Icon className="text-blue-600" size={24} />
                      <h3 className="text-xl font-semibold text-gray-900">{layer.title}</h3>
                    </div>
                    
                    <div className="mb-4">
                      <h4 className="font-medium text-gray-900 mb-2">Components:</h4>
                      <div className="flex flex-wrap gap-2">
                        {layer.components.map((component, index) => (
                          <span key={index} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                            {component}
                          </span>
                        ))}
                      </div>
                    </div>
                    
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Technologies:</h4>
                      <div className="flex flex-wrap gap-2">
                        {layer.technologies.map((tech, index) => (
                          <span key={index} className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-sm">
                            {tech}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>

            {/* Architecture Diagram */}
            <div className="bg-white rounded-lg shadow-md p-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-6 text-center">System Architecture Diagram</h3>
              <div className="flex justify-center">
                <img 
                  src="/images/system_architecture.jpeg" 
                  alt="System Architecture Diagram" 
                  className="max-w-full h-auto rounded-lg"
                />
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Multi-Agent System */}
      {activeTab === 'agents' && (
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">Multi-Agent Content Creation System</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {Object.entries(multiAgentSystem).map(([key, agent]) => {
                const Icon = agent.icon
                return (
                  <div key={key} className="bg-white rounded-lg shadow-md p-6">
                    <div className="flex items-center space-x-3 mb-4">
                      <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                        <Icon className="text-blue-600" size={24} />
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">{agent.name}</h3>
                        <p className="text-sm text-gray-600">{agent.description}</p>
                      </div>
                    </div>
                    
                    <div>
                      <h4 className="font-medium text-gray-900 mb-3">Capabilities:</h4>
                      <ul className="space-y-2">
                        {agent.capabilities.map((capability, index) => (
                          <li key={index} className="flex items-center text-sm text-gray-700">
                            <CheckCircle className="text-green-500 mr-2 flex-shrink-0" size={14} />
                            {capability}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                )
              })}
            </div>

            {/* Agent Workflow */}
            <div className="mt-12 bg-white rounded-lg shadow-md p-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-6 text-center">Agent Collaboration Workflow</h3>
              <div className="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0 md:space-x-4">
                <div className="text-center">
                  <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2">
                    <Code className="text-blue-600" size={24} />
                  </div>
                  <h4 className="font-medium text-gray-900">Content Creation</h4>
                  <p className="text-sm text-gray-600">AI generates initial content</p>
                </div>
                <ArrowRight className="text-gray-400 hidden md:block" size={20} />
                <div className="text-center">
                  <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
                    <Cog className="text-green-600" size={24} />
                  </div>
                  <h4 className="font-medium text-gray-900">Business Integration</h4>
                  <p className="text-sm text-gray-600">Local business content added</p>
                </div>
                <ArrowRight className="text-gray-400 hidden md:block" size={20} />
                <div className="text-center">
                  <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-2">
                    <Shield className="text-red-600" size={24} />
                  </div>
                  <h4 className="font-medium text-gray-900">Quality Control</h4>
                  <p className="text-sm text-gray-600">Content moderation & approval</p>
                </div>
                <ArrowRight className="text-gray-400 hidden md:block" size={20} />
                <div className="text-center">
                  <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-2">
                    <Layers className="text-purple-600" size={24} />
                  </div>
                  <h4 className="font-medium text-gray-900">Optimization</h4>
                  <p className="text-sm text-gray-600">Performance analysis & refinement</p>
                </div>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Technical Roadmap */}
      {activeTab === 'roadmap' && (
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">Technical Implementation Roadmap</h2>
            
            <div className="space-y-8">
              {technicalRoadmap.map((phase, index) => (
                <div key={index} className="bg-white rounded-lg shadow-md p-6">
                  <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-2">{phase.phase}</h3>
                      <div className="space-y-2">
                        <div className="flex items-center space-x-2">
                          <Calendar className="text-blue-600" size={16} />
                          <span className="text-sm text-gray-600">{phase.timeline}</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <DollarSign className="text-green-600" size={16} />
                          <span className="text-sm text-gray-600">{phase.budget}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="lg:col-span-2">
                      <h4 className="font-medium text-gray-900 mb-3">Key Deliverables:</h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                        {phase.deliverables.map((deliverable, deliverableIndex) => (
                          <div key={deliverableIndex} className="flex items-center space-x-2">
                            <CheckCircle className="text-green-500 flex-shrink-0" size={16} />
                            <span className="text-sm text-gray-700">{deliverable}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Technical Specifications */}
            <div className="mt-16 bg-white rounded-lg shadow-md p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">Scalability Specifications</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="text-center">
                  <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Users className="text-blue-600" size={24} />
                  </div>
                  <h4 className="font-semibold text-gray-900 mb-2">User Capacity</h4>
                  <p className="text-3xl font-bold text-blue-600 mb-2">50K+</p>
                  <p className="text-sm text-gray-600">Concurrent users supported</p>
                </div>
                <div className="text-center">
                  <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <MapPin className="text-green-600" size={24} />
                  </div>
                  <h4 className="font-semibold text-gray-900 mb-2">Communities</h4>
                  <p className="text-3xl font-bold text-green-600 mb-2">100+</p>
                  <p className="text-sm text-gray-600">Simultaneous communities</p>
                </div>
                <div className="text-center">
                  <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Bell className="text-purple-600" size={24} />
                  </div>
                  <h4 className="font-semibold text-gray-900 mb-2">Newsletters</h4>
                  <p className="text-3xl font-bold text-purple-600 mb-2">1M+</p>
                  <p className="text-sm text-gray-600">Monthly email deliveries</p>
                </div>
              </div>
            </div>
          </div>
        </section>
      )}
    </div>
  )
}

export default ProductDevelopment
