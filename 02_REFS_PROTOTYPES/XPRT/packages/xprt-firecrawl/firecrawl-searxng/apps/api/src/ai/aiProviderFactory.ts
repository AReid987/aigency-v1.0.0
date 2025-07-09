import { Configuration } from './types';

export interface AIProvider {
  generate(prompt: string): Promise<string>;
  // Add other common methods as needed
}

export function createAIProvider(config: Configuration): AIProvider {
  switch (config.activeAIProvider) {
    case 'openrouter':
      return new OpenRouterProvider(config.openRouterApiKey, config.openRouterModel);
    case 'gemini':
      return new GeminiProvider(config.geminiApiKey);
    case 'mistral':
      return new MistralProvider(config.mistralApiKey);
    case 'requesty':
      return new RequestyProvider(config.requestyApiKey);
    case 'groq':
      return new GroqProvider(config.groqApiKey);
    case 'cerebras':
      return new CerebrasProvider(config.cerebrasApiKey);
    case 'github':
      return new GitHubModelsProvider(config.githubModelsApiKey, config.githubModelsEndpoint);
    case 'huggingface':
      return new HuggingFaceProvider(config.huggingfaceApiKey, config.huggingfaceModel);
    default:
      throw new Error(`Unsupported AI provider: ${config.activeAIProvider}`);
  }
}