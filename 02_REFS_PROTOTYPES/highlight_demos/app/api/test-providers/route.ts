import { NextRequest, NextResponse } from 'next/server';
import { getAvailableProviders, getAvailableModels } from '@/lib/ai-providers';

export async function GET(request: NextRequest) {
  try {
    const providers = getAvailableProviders();
    const models = getAvailableModels();
    
    return NextResponse.json({
      success: true,
      providers: providers.map(p => ({
        id: p.id,
        name: p.name,
        isAvailable: p.isAvailable,
        modelCount: p.models.length,
        hasApiKey: !!p.apiKey
      })),
      models: models.map(m => ({
        id: m.id,
        name: m.name,
        provider: m.provider,
        capabilities: m.capabilities
      })),
      totalProviders: providers.length,
      totalModels: models.length
    });
  } catch (error) {
    console.error('Test providers error:', error);
    return NextResponse.json({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
      providers: [],
      models: []
    });
  }
}
