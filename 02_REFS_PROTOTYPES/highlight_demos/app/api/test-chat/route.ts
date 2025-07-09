import { NextRequest, NextResponse } from 'next/server';
import { getAvailableProviders, createAIClient } from '@/lib/ai-providers';

export async function POST(request: NextRequest) {
  try {
    const { message = 'Hello! This is a test message.' } = await request.json();
    
    console.log('Testing chat with message:', message);
    
    // Get available providers
    const providers = getAvailableProviders();
    console.log('Available providers:', providers.map(p => p.id));
    
    if (providers.length === 0) {
      return NextResponse.json({
        success: false,
        error: 'No AI providers available',
        details: 'Check your API keys in environment variables'
      });
    }
    
    // Use first available provider
    const provider = providers[0];
    const model = provider.models[0];
    
    console.log('Using provider:', provider.id, 'with model:', model.id);
    
    // Create client and test
    const client = createAIClient(provider.id);
    
    const response = await client.chat({
      model: model.id,
      messages: [{ role: 'user', content: message }],
      maxTokens: 100,
      temperature: 0.7
    });
    
    console.log('Chat response received');
    
    return NextResponse.json({
      success: true,
      provider: provider.id,
      model: model.id,
      response: response.choices[0]?.message?.content || 'No response content',
      usage: response.usage
    });
    
  } catch (error) {
    console.error('Test chat error:', error);
    return NextResponse.json({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
      stack: error instanceof Error ? error.stack : undefined
    });
  }
}

export async function GET(request: NextRequest) {
  return NextResponse.json({
    message: 'Send a POST request with { "message": "your test message" } to test the chat functionality'
  });
}
