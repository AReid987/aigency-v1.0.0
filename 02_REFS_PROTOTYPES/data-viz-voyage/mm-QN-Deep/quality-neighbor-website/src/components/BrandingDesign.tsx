import { useState } from 'react'
import { Palette, Type, Layout, Heart, Shield, Users, Zap, Eye, CheckCircle } from 'lucide-react'

const BrandingDesign = () => {
  const [activeSection, setActiveSection] = useState('identity')

  const brandPillars = [
    {
      title: 'Professional Excellence',
      description: 'High-quality, curated content with journalistic standards',
      icon: Shield,
      color: 'text-blue-600 bg-blue-50'
    },
    {
      title: 'Community Connection',
      description: 'Fostering genuine neighborhood relationships and engagement',
      icon: Users,
      color: 'text-green-600 bg-green-50'
    },
    {
      title: 'Local Business Integration',
      description: 'Supporting and promoting local commerce with clear value',
      icon: Zap,
      color: 'text-purple-600 bg-purple-50'
    },
    {
      title: 'Information Integrity',
      description: 'Trustworthy, fact-checked, and relevant local information',
      icon: Eye,
      color: 'text-orange-600 bg-orange-50'
    },
    {
      title: 'Privacy-Respecting Technology',
      description: 'User-first approach without invasive data collection',
      icon: Heart,
      color: 'text-red-600 bg-red-50'
    }
  ]

  const colorPalette = {
    primary: [
      { name: 'Primary 900', hex: '#062C43', rgb: '6, 44, 67', description: 'Deep navy - primary brand color' },
      { name: 'Primary 700', hex: '#1D5B8C', rgb: '29, 91, 140', description: 'Deep blue - interactive elements' },
      { name: 'Primary 500', hex: '#3E92CC', rgb: '62, 146, 204', description: 'Standard blue - primary actions' },
      { name: 'Primary 300', hex: '#8BC1EA', rgb: '139, 193, 234', description: 'Light blue - highlights' },
      { name: 'Primary 100', hex: '#D6E9FA', rgb: '214, 233, 250', description: 'Very light blue - backgrounds' }
    ],
    secondary: [
      { name: 'Secondary 900', hex: '#444130', rgb: '68, 65, 48', description: 'Deep sage - grounding element' },
      { name: 'Secondary 700', hex: '#696257', rgb: '105, 98, 87', description: 'Medium sage - subdued text' },
      { name: 'Secondary 500', hex: '#928A7B', rgb: '146, 138, 123', description: 'Standard sage - neutral elements' },
      { name: 'Secondary 300', hex: '#BDB8AE', rgb: '189, 184, 174', description: 'Light sage - borders' },
      { name: 'Secondary 100', hex: '#E9E7E3', rgb: '233, 231, 227', description: 'Nearly white sage - backgrounds' }
    ],
    accent: [
      { name: 'Success', hex: '#4F9D69', rgb: '79, 157, 105', description: 'Success messages' },
      { name: 'Warning', hex: '#E9C46A', rgb: '233, 196, 106', description: 'Warning messages' },
      { name: 'Error', hex: '#C75D4F', rgb: '199, 93, 79', description: 'Error messages' },
      { name: 'Info', hex: '#3E92CC', rgb: '62, 146, 204', description: 'Information messages' }
    ]
  }

  const typography = {
    headings: {
      family: 'Playfair Display',
      description: 'Serif font for headings - evokes traditional journalism credibility',
      sizes: ['48px (H1)', '36px (H2)', '28px (H3)', '24px (H4)', '20px (H5)', '18px (H6)'],
      weights: ['400 (Regular)', '700 (Bold)', '900 (Black)']
    },
    body: {
      family: 'Inter',
      description: 'Clean sans-serif for body text - ensures optimal readability',
      sizes: ['16px (Base)', '14px (Small)', '12px (Caption)'],
      weights: ['400 (Regular)', '500 (Medium)', '600 (Semibold)', '700 (Bold)']
    }
  }

  const brandVoice = {
    core: {
      title: 'Core Voice Attributes',
      attributes: [
        { name: 'Professional', description: 'Maintains high standards while remaining accessible' },
        { name: 'Trustworthy', description: 'Reliable, fact-based, and transparent communication' },
        { name: 'Neighborly', description: 'Warm, inclusive, and community-focused tone' },
        { name: 'Insightful', description: 'Provides valuable context and meaningful connections' },
        { name: 'Purposeful', description: 'Every communication has clear value and intent' }
      ]
    },
    audiences: {
      title: 'Audience Adaptations',
      adaptations: [
        {
          audience: 'Growing Families',
          tone: 'Practical and supportive',
          focus: 'Safety, schools, family-friendly activities',
          example: '"Keep your family informed with the latest school updates and neighborhood safety alerts."'
        },
        {
          audience: 'Empty Nesters',
          tone: 'Respectful and informative',
          focus: 'Community involvement, local business, governance',
          example: '"Stay connected with your community through trusted local news and business recommendations."'
        },
        {
          audience: 'Community Leaders',
          tone: 'Collaborative and empowering',
          focus: 'Organization tools, governance, community building',
          example: '"Empower your community leadership with comprehensive communication tools and insights."'
        },
        {
          audience: 'Local Businesses',
          tone: 'Partnership-focused and ROI-driven',
          focus: 'Growth opportunities, community connection, measurable results',
          example: '"Connect with your neighbors and grow your local business through targeted community engagement."'
        }
      ]
    }
  }

  const designComponents = [
    {
      category: 'Atoms',
      description: 'Basic building blocks',
      components: ['Colors', 'Typography', 'Icons', 'Buttons', 'Inputs', 'Dividers']
    },
    {
      category: 'Molecules',
      description: 'Simple combinations',
      components: ['Search bars', 'Form groups', 'Cards', 'Navigation items', 'Article previews']
    },
    {
      category: 'Organisms',
      description: 'Complex components',
      components: ['Headers', 'Newsletter layouts', 'Business listings', 'Community calendars']
    },
    {
      category: 'Templates',
      description: 'Page layouts',
      components: ['Newsletter template', 'Directory page', 'Event listing', 'Business profile']
    },
    {
      category: 'Pages',
      description: 'Specific instances',
      components: ['Weekly newsletter', 'Business directory', 'Community calendar', 'Admin dashboard']
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">Branding & Design System</h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Complete brand identity, voice guidelines, and atomic design system 
              for Quality Neighbor platform
            </p>
          </div>
        </div>
      </section>

      {/* Navigation */}
      <section className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {[
              { id: 'identity', label: 'Brand Identity', icon: Heart },
              { id: 'voice', label: 'Brand Voice', icon: Type },
              { id: 'design', label: 'Design System', icon: Palette },
              { id: 'components', label: 'Components', icon: Layout }
            ].map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveSection(tab.id)}
                  className={`flex items-center space-x-2 py-4 px-2 border-b-2 font-medium text-sm ${
                    activeSection === tab.id
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

      {/* Brand Identity */}
      {activeSection === 'identity' && (
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {/* Mission Statement */}
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-gray-900 mb-8">Mission & Positioning</h2>
              <div className="bg-blue-50 rounded-lg p-8 max-w-4xl mx-auto">
                <h3 className="text-2xl font-bold text-blue-900 mb-4">Mission Statement</h3>
                <p className="text-lg text-blue-800 leading-relaxed">
                  "Quality Neighbor connects residential communities through professional, trusted local information 
                  that strengthens neighborhood bonds and supports local businesses – delivering your community, professionally."
                </p>
              </div>
            </div>

            {/* Brand Pillars */}
            <div className="mb-16">
              <h3 className="text-2xl font-bold text-gray-900 mb-8 text-center">Brand Pillars</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {brandPillars.map((pillar, index) => {
                  const Icon = pillar.icon
                  return (
                    <div key={index} className="bg-white rounded-lg shadow-md p-6">
                      <div className={`w-12 h-12 rounded-lg ${pillar.color} flex items-center justify-center mb-4`}>
                        <Icon size={24} />
                      </div>
                      <h4 className="text-lg font-semibold text-gray-900 mb-2">{pillar.title}</h4>
                      <p className="text-gray-600">{pillar.description}</p>
                    </div>
                  )
                })}
              </div>
            </div>

            {/* Competitive Positioning */}
            <div className="bg-white rounded-lg shadow-md p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">Competitive Positioning</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="text-center">
                  <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-red-600 font-bold">VS</span>
                  </div>
                  <h4 className="font-semibold text-gray-900 mb-2">Social Media Platforms</h4>
                  <p className="text-sm text-gray-600">Professional curation vs. algorithm chaos</p>
                </div>
                <div className="text-center">
                  <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <CheckCircle className="text-blue-600" size={24} />
                  </div>
                  <h4 className="font-semibold text-gray-900 mb-2">Newsletter Format</h4>
                  <p className="text-sm text-gray-600">Trusted, familiar, and purposeful communication</p>
                </div>
                <div className="text-center">
                  <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Heart className="text-green-600" size={24} />
                  </div>
                  <h4 className="font-semibold text-gray-900 mb-2">Community Focus</h4>
                  <p className="text-sm text-gray-600">Hyperlocal relevance with business integration</p>
                </div>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Brand Voice */}
      {activeSection === 'voice' && (
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">Brand Voice & Tone Guidelines</h2>
            
            {/* Core Attributes */}
            <div className="mb-12">
              <h3 className="text-2xl font-bold text-gray-900 mb-8">{brandVoice.core.title}</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {brandVoice.core.attributes.map((attribute, index) => (
                  <div key={index} className="bg-white rounded-lg shadow-md p-6">
                    <h4 className="text-lg font-semibold text-gray-900 mb-2">{attribute.name}</h4>
                    <p className="text-gray-600">{attribute.description}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Audience Adaptations */}
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-8">{brandVoice.audiences.title}</h3>
              <div className="space-y-6">
                {brandVoice.audiences.adaptations.map((adaptation, index) => (
                  <div key={index} className="bg-white rounded-lg shadow-md p-6">
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                      <div>
                        <h4 className="text-lg font-semibold text-gray-900 mb-2">{adaptation.audience}</h4>
                        <div className="space-y-2">
                          <div>
                            <span className="font-medium text-gray-700">Tone:</span>
                            <span className="text-gray-600 ml-2">{adaptation.tone}</span>
                          </div>
                          <div>
                            <span className="font-medium text-gray-700">Focus:</span>
                            <span className="text-gray-600 ml-2">{adaptation.focus}</span>
                          </div>
                        </div>
                      </div>
                      <div className="lg:col-span-2">
                        <span className="font-medium text-gray-700">Example:</span>
                        <p className="text-gray-600 italic mt-1">{adaptation.example}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Design System */}
      {activeSection === 'design' && (
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">Design System</h2>
            
            {/* Color Palette */}
            <div className="mb-16">
              <h3 className="text-2xl font-bold text-gray-900 mb-8">Color Palette</h3>
              
              {Object.entries(colorPalette).map(([category, colors]) => (
                <div key={category} className="mb-8">
                  <h4 className="text-lg font-semibold text-gray-900 mb-4 capitalize">{category} Colors</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
                    {colors.map((color, index) => (
                      <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden">
                        <div 
                          className="h-20 w-full"
                          style={{ backgroundColor: color.hex }}
                        ></div>
                        <div className="p-4">
                          <h5 className="font-medium text-gray-900 text-sm">{color.name}</h5>
                          <p className="text-xs text-gray-600 mt-1">{color.hex}</p>
                          <p className="text-xs text-gray-500">RGB: {color.rgb}</p>
                          <p className="text-xs text-gray-500 mt-1">{color.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            {/* Typography */}
            <div className="mb-16">
              <h3 className="text-2xl font-bold text-gray-900 mb-8">Typography</h3>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h4 className="text-lg font-semibold text-gray-900 mb-4">Headings - {typography.headings.family}</h4>
                  <p className="text-gray-600 mb-4">{typography.headings.description}</p>
                  
                  <div className="space-y-3">
                    <div className="text-4xl font-bold" style={{ fontFamily: 'serif' }}>Heading Example</div>
                    <div>
                      <span className="font-medium text-gray-700">Sizes:</span>
                      <div className="text-sm text-gray-600 mt-1">
                        {typography.headings.sizes.join(' • ')}
                      </div>
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Weights:</span>
                      <div className="text-sm text-gray-600 mt-1">
                        {typography.headings.weights.join(' • ')}
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h4 className="text-lg font-semibold text-gray-900 mb-4">Body Text - {typography.body.family}</h4>
                  <p className="text-gray-600 mb-4">{typography.body.description}</p>
                  
                  <div className="space-y-3">
                    <div className="text-base">This is body text example with optimal readability.</div>
                    <div>
                      <span className="font-medium text-gray-700">Sizes:</span>
                      <div className="text-sm text-gray-600 mt-1">
                        {typography.body.sizes.join(' • ')}
                      </div>
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Weights:</span>
                      <div className="text-sm text-gray-600 mt-1">
                        {typography.body.weights.join(' • ')}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Design Components */}
      {activeSection === 'components' && (
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">Atomic Design Components</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {designComponents.map((component, index) => (
                <div key={index} className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">{component.category}</h3>
                  <p className="text-gray-600 mb-4">{component.description}</p>
                  <ul className="space-y-2">
                    {component.components.map((item, itemIndex) => (
                      <li key={itemIndex} className="flex items-center text-sm text-gray-700">
                        <div className="w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>

            {/* Sample Newsletter Design */}
            <div className="mt-16 bg-white rounded-lg shadow-md p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">Sample Newsletter Design</h3>
              <div className="flex justify-center">
                <img 
                  src="/images/newsletter_design.jpg" 
                  alt="Sample Newsletter Design" 
                  className="max-w-full h-auto rounded-lg shadow-lg"
                />
              </div>
            </div>

            {/* Implementation Guidelines */}
            <div className="mt-16 bg-blue-50 rounded-lg p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">Implementation Guidelines</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <h4 className="text-lg font-semibold text-gray-900 mb-4">Design Principles</h4>
                  <ul className="space-y-2">
                    <li className="flex items-start">
                      <CheckCircle className="text-green-500 mr-2 mt-1 flex-shrink-0" size={16} />
                      <span className="text-gray-700">Maintain visual hierarchy and readability</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="text-green-500 mr-2 mt-1 flex-shrink-0" size={16} />
                      <span className="text-gray-700">Ensure mobile-first responsive design</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="text-green-500 mr-2 mt-1 flex-shrink-0" size={16} />
                      <span className="text-gray-700">Follow WCAG accessibility guidelines</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="text-green-500 mr-2 mt-1 flex-shrink-0" size={16} />
                      <span className="text-gray-700">Maintain consistent brand application</span>
                    </li>
                  </ul>
                </div>
                <div>
                  <h4 className="text-lg font-semibold text-gray-900 mb-4">Usage Standards</h4>
                  <ul className="space-y-2">
                    <li className="flex items-start">
                      <CheckCircle className="text-green-500 mr-2 mt-1 flex-shrink-0" size={16} />
                      <span className="text-gray-700">Use design tokens for all styling decisions</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="text-green-500 mr-2 mt-1 flex-shrink-0" size={16} />
                      <span className="text-gray-700">Test components across all target devices</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="text-green-500 mr-2 mt-1 flex-shrink-0" size={16} />
                      <span className="text-gray-700">Document all component variations and states</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="text-green-500 mr-2 mt-1 flex-shrink-0" size={16} />
                      <span className="text-gray-700">Regular design system audits and updates</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </section>
      )}
    </div>
  )
}

export default BrandingDesign
