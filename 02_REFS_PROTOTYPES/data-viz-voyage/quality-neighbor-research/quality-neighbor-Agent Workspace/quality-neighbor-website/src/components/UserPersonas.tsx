import { useEffect, useState } from 'react'
import { User, Heart, MapPin, Smartphone, Mail, Clock, TrendingUp, Home, Baby, Users as UsersIcon } from 'lucide-react'

const UserPersonas = () => {
  const [personaData, setPersonaData] = useState<any>(null)
  const [activePersona, setActivePersona] = useState(0)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadData = async () => {
      try {
        const response = await fetch('/data/hartland_ranch_user_personas.json')
        const data = await response.json()
        setPersonaData(data)
        setLoading(false)
      } catch (error) {
        console.error('Error loading persona data:', error)
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

  const personas = personaData?.user_personas?.personas ? Object.values(personaData.user_personas.personas) : []

  const personaCards = [
    {
      title: 'Growing Families',
      subtitle: 'Sarah & Mike Chen',
      description: 'Young families focused on safety, schools, and community connection',
      icon: Baby,
      color: 'bg-blue-50 border-blue-200 text-blue-600',
      image: '/charts/growing_family_persona.png'
    },
    {
      title: 'Empty Nesters',
      subtitle: 'Robert & Linda Martinez',
      description: 'Mature couples seeking community involvement and local business connections',
      icon: Home,
      color: 'bg-green-50 border-green-200 text-green-600',
      image: '/charts/community_elder_persona.png'
    },
    {
      title: 'Young Professionals',
      subtitle: 'Jessica Thompson',
      description: 'Single professionals prioritizing convenience and social connections',
      icon: User,
      color: 'bg-purple-50 border-purple-200 text-purple-600',
      image: '/charts/growing_family_persona.png' // Using same image as placeholder
    },
    {
      title: 'Community Leaders',
      subtitle: 'David Kim',
      description: 'Active community members driving neighborhood engagement and organization',
      icon: UsersIcon,
      color: 'bg-orange-50 border-orange-200 text-orange-600',
      image: '/charts/community_leader_persona.png'
    }
  ]

  const currentPersona = personas[activePersona]

  const renderPersonaDetails = (persona: any) => {
    if (!persona) return null

    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Demographics */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
            <User className="mr-2 text-blue-600" size={20} />
            Demographics
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Age Range:</span>
              <span className="font-medium">{persona.demographics?.age_range}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Household:</span>
              <span className="font-medium">{persona.demographics?.household_composition}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Income:</span>
              <span className="font-medium">{persona.demographics?.income}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Education:</span>
              <span className="font-medium">{persona.demographics?.education}</span>
            </div>
          </div>
        </div>

        {/* Technology Profile */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
            <Smartphone className="mr-2 text-green-600" size={20} />
            Technology Profile
          </h3>
          <div className="space-y-3">
            <div>
              <span className="text-gray-600 block mb-1">Devices:</span>
              <div className="flex flex-wrap gap-2">
                {persona.technology_profile?.devices?.map((device: string, index: number) => (
                  <span key={index} className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-sm">
                    {device}
                  </span>
                ))}
              </div>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Smart Home Adoption:</span>
              <span className="font-medium">{persona.technology_profile?.smart_home_adoption}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Internet Usage:</span>
              <span className="font-medium">{persona.technology_profile?.internet_usage}</span>
            </div>
          </div>
        </div>

        {/* Communication Preferences */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
            <Mail className="mr-2 text-purple-600" size={20} />
            Communication Preferences
          </h3>
          <div className="space-y-3">
            <div>
              <span className="text-gray-600 block mb-1">Primary Channels:</span>
              <div className="flex flex-wrap gap-2">
                {persona.communication_preferences?.primary_channels?.map((channel: string, index: number) => (
                  <span key={index} className="bg-purple-100 text-purple-700 px-2 py-1 rounded text-sm">
                    {channel}
                  </span>
                ))}
              </div>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Newsletter Receptivity:</span>
              <span className="font-medium">{persona.communication_preferences?.newsletter_receptivity}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Optimal Timing:</span>
              <span className="font-medium">{persona.communication_preferences?.optimal_timing}</span>
            </div>
          </div>
        </div>

        {/* Community Engagement */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
            <Heart className="mr-2 text-red-600" size={20} />
            Community Engagement
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Participation Level:</span>
              <span className="font-medium">{persona.community_engagement?.participation_level}</span>
            </div>
            <div>
              <span className="text-gray-600 block mb-1">Primary Motivations:</span>
              <ul className="text-sm text-gray-700 space-y-1">
                {persona.community_engagement?.primary_motivations?.map((motivation: string, index: number) => (
                  <li key={index} className="flex items-center">
                    <span className="w-1.5 h-1.5 bg-red-400 rounded-full mr-2"></span>
                    {motivation}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">User Personas & Journey Mapping</h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Deep analysis of our target user segments with detailed personas, behavioral insights, 
              and journey mapping for Quality Neighbor
            </p>
          </div>
        </div>
      </section>

      {/* Persona Overview */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">Target User Segments</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {personaCards.map((persona, index) => {
              const Icon = persona.icon
              return (
                <div
                  key={index}
                  onClick={() => setActivePersona(index)}
                  className={`border-2 rounded-lg p-6 cursor-pointer transition-all hover:shadow-lg ${
                    activePersona === index ? persona.color : 'bg-white border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="text-center">
                    <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
                      <Icon size={24} className={activePersona === index ? 'text-current' : 'text-gray-600'} />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">{persona.title}</h3>
                    <p className="text-sm text-blue-600 font-medium mb-2">{persona.subtitle}</p>
                    <p className="text-sm text-gray-600">{persona.description}</p>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Detailed Persona View */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {currentPersona && (
            <>
              <div className="text-center mb-12">
                <h2 className="text-3xl font-bold text-gray-900 mb-4">
                  {(currentPersona as any)?.name} - {(currentPersona as any)?.archetype}
                </h2>
                <p className="text-lg text-gray-600">
                  Detailed profile and behavioral analysis
                </p>
              </div>
              {renderPersonaDetails(currentPersona)}
            </>
          )}
        </div>
      </section>

      {/* Journey Maps */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">User Journey Maps</h2>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="bg-gray-50 rounded-lg p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Growing Family Journey</h3>
              <img 
                src="/charts/growing_family_journey_map.png" 
                alt="Growing Family Journey Map" 
                className="w-full rounded-lg mb-4"
              />
              <p className="text-gray-600 text-sm">
                Focused on safety information, school updates, and family-friendly local services
              </p>
            </div>
            <div className="bg-gray-50 rounded-lg p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Empty Nester Journey</h3>
              <img 
                src="/charts/community_elder_journey_map.png" 
                alt="Community Elder Journey Map" 
                className="w-full rounded-lg mb-4"
              />
              <p className="text-gray-600 text-sm">
                Emphasis on community involvement, local business recommendations, and neighborhood news
              </p>
            </div>
            <div className="bg-gray-50 rounded-lg p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Community Leader Journey</h3>
              <img 
                src="/charts/community_leader_journey_map.png" 
                alt="Community Leader Journey Map" 
                className="w-full rounded-lg mb-4"
              />
              <p className="text-gray-600 text-sm">
                Focus on community organization tools, event promotion, and governance information
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Persona Insights */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">Common Characteristics</h2>
              <div className="space-y-4">
                {personaData?.user_personas?.persona_insights?.common_characteristics?.map((characteristic: string, index: number) => (
                  <div key={index} className="flex items-start space-x-3">
                    <div className="flex-shrink-0 w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center mt-1">
                      <span className="text-blue-600 text-xs">✓</span>
                    </div>
                    <p className="text-gray-700">{characteristic}</p>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">Key Differentiators</h2>
              <div className="space-y-4">
                {personaData?.user_personas?.persona_insights?.key_differentiators?.map((differentiator: string, index: number) => (
                  <div key={index} className="flex items-start space-x-3">
                    <div className="flex-shrink-0 w-6 h-6 bg-orange-100 rounded-full flex items-center justify-center mt-1">
                      <TrendingUp className="text-orange-600" size={12} />
                    </div>
                    <p className="text-gray-700">{differentiator}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Newsletter Platform Implications */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-blue-50 rounded-lg p-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center">
              Newsletter Platform Implications
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {personaData?.user_personas?.persona_insights?.newsletter_platform_implications?.map((implication: string, index: number) => (
                <div key={index} className="bg-white rounded-lg p-4 shadow-sm">
                  <div className="flex items-center space-x-2 mb-2">
                    <MapPin className="text-blue-600" size={16} />
                    <span className="font-medium text-gray-900">Key Insight</span>
                  </div>
                  <p className="text-gray-700 text-sm">{implication}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Quality Neighbor Fit Analysis */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">Quality Neighbor Value Proposition Fit</h2>
          {currentPersona && (currentPersona as any)?.quality_neighbor_fit && (
            <div className="bg-white rounded-lg shadow-md p-8">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="text-center">
                  <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Heart className="text-green-600" size={24} />
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-2">Appeal Factors</h3>
                  <ul className="text-sm text-gray-600 space-y-1">
                    {(currentPersona as any)?.quality_neighbor_fit?.appeal_factors?.map((factor: string, index: number) => (
                      <li key={index}>• {factor}</li>
                    ))}
                  </ul>
                </div>
                <div className="text-center">
                  <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Clock className="text-yellow-600" size={24} />
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-2">Concerns</h3>
                  <ul className="text-sm text-gray-600 space-y-1">
                    {(currentPersona as any)?.quality_neighbor_fit?.concerns?.map((concern: string, index: number) => (
                      <li key={index}>• {concern}</li>
                    ))}
                  </ul>
                </div>
                <div className="text-center">
                  <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <TrendingUp className="text-blue-600" size={24} />
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-2">Value Proposition</h3>
                  <p className="text-sm text-gray-600">{(currentPersona as any)?.quality_neighbor_fit?.value_proposition}</p>
                </div>
                <div className="text-center">
                  <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <UsersIcon className="text-purple-600" size={24} />
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-2">Engagement Likelihood</h3>
                  <p className="text-sm text-gray-600">{(currentPersona as any)?.quality_neighbor_fit?.engagement_likelihood}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </section>
    </div>
  )
}

export default UserPersonas
