// API route for agent chat interactions
import { NextRequest, NextResponse } from 'next/server';
import { aiAgentService, type AgentResponse } from '@/lib/ai-agent-service';
import { getAvailableProviders, getAvailableModels } from '@/lib/ai-providers';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { sessionId, message, agentId, userId, options } = body;

    console.log('Chat request received:', { sessionId, agentId, userId, messageLength: message?.length });

    // Validate required fields
    if (!message) {
      return NextResponse.json(
        { error: 'Message is required' },
        { status: 400 }
      );
    }

    let currentSessionId = sessionId;

    // Create new session if none provided
    if (!currentSessionId && agentId && userId) {
      const session = aiAgentService.createSession(agentId, userId);
      currentSessionId = session.id;
    }

    if (!currentSessionId) {
      return NextResponse.json(
        { error: 'Session ID or agent/user IDs required' },
        { status: 400 }
      );
    }

    // Send message to agent
    console.log('Sending message to agent service:', { currentSessionId, agentId });
    const response: AgentResponse = await aiAgentService.sendMessage(
      currentSessionId,
      message,
      options
    );
    console.log('Received response from agent service:', { model: response.model, provider: response.provider });

    return NextResponse.json({
      success: true,
      sessionId: currentSessionId,
      response: response.content,
      model: response.model,
      provider: response.provider,
      usage: response.usage,
      metadata: response.metadata
    });

  } catch (error) {
    console.error('Agent chat error:', error);
    return NextResponse.json(
      {
        error: 'Failed to process agent chat',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const action = searchParams.get('action');

    switch (action) {
      case 'agents':
        // Get available agents
        const agents = aiAgentService.getAvailableAgents();
        return NextResponse.json({ agents });

      case 'providers':
        // Get provider status
        const providers = aiAgentService.getProviderStatus();
        return NextResponse.json({ providers });

      case 'models':
        // Get available models
        const models = getAvailableModels();
        return NextResponse.json({ models });

      case 'session':
        // Get session history
        const sessionId = searchParams.get('sessionId');
        if (!sessionId) {
          return NextResponse.json(
            { error: 'Session ID required' },
            { status: 400 }
          );
        }
        const history = aiAgentService.getSessionHistory(sessionId);
        return NextResponse.json({ history });

      default:
        return NextResponse.json(
          { error: 'Invalid action' },
          { status: 400 }
        );
    }
  } catch (error) {
    console.error('Agent API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
