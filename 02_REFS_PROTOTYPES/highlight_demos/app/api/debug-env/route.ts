import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    const envVars = {
      OPENROUTER_API_KEY: process.env.OPENROUTER_API_KEY ? 'Set' : 'Not set',
      GOOGLE_API_KEY: process.env.GOOGLE_API_KEY ? 'Set' : 'Not set',
      GROQ_API_KEY: process.env.GROQ_API_KEY ? 'Set' : 'Not set',
      CEREBRAS_API_KEY: process.env.CEREBRAS_API_KEY ? 'Set' : 'Not set',
      MISTRAL_API_KEY: process.env.MISTRAL_API_KEY ? 'Set' : 'Not set',
      CHUTES_API_KEY: process.env.CHUTES_API_KEY ? 'Set' : 'Not set',
      OPENAI_API_KEY: process.env.OPENAI_API_KEY ? 'Set' : 'Not set',
      ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY ? 'Set' : 'Not set',
    };
    
    return NextResponse.json({
      success: true,
      environment: envVars,
      nodeEnv: process.env.NODE_ENV
    });
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}
