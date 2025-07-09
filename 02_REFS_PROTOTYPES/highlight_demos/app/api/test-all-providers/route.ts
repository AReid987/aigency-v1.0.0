import { NextRequest, NextResponse } from 'next/server';
import { getAvailableProviders, createAIClient } from '@/lib/ai-providers';

export async function GET(request: NextRequest) {
  const results = [];
  
  try {
    const providers = getAvailableProviders();
    
    for (const provider of providers) {
      const result = {
        id: provider.id,
        name: provider.name,
        hasApiKey: !!provider.apiKey,
        apiKeyFormat: provider.apiKey ? `${provider.apiKey.substring(0, 10)}...` : 'None',
        models: provider.models.length,
        status: 'unknown',
        error: null as string | null
      };
      
      try {
        // Try to create client
        const client = createAIClient(provider.id);
        result.status = 'client_created';
        
        // Try a simple chat request
        const model = provider.models[0];
        if (model) {
          const response = await client.chat({
            model: model.id,
            messages: [{ role: 'user', content: 'Hi' }],
            maxTokens: 10,
            temperature: 0.7
          });
          
          if (response.choices[0]?.message?.content) {
            result.status = 'working';
          } else {
            result.status = 'no_response';
          }
        }
      } catch (error) {
        result.status = 'error';
        result.error = error instanceof Error ? error.message : 'Unknown error';
      }
      
      results.push(result);
    }
    
    return NextResponse.json({
      success: true,
      totalProviders: providers.length,
      results
    });
    
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
      results
    });
  }
}
