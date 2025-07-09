import 'dotenv/config';
import { Configuration } from '../ai/types';

export function loadConfig(): Configuration {
  return {
    activeAIProvider: process.env.ACTIVE_AI_PROVIDER || '',
    openRouterApiKey: process.env.OPENROUTER_API_KEY,
    openRouterModel: process.env.OPENROUTER_MODEL,
    geminiApiKey: process.env.GEMINI_API_KEY,
    mistralApiKey: process.env.MISTRAL_API_KEY,
    requestyApiKey: process.env.REQUESTY_API_KEY,
    groqApiKey: process.env.GROQ_API_KEY,
    cerebrasApiKey: process.env.CEREBRAS_API_KEY,
    githubModelsApiKey: process.env.GITHUB_MODELS_API_KEY,
    githubModelsEndpoint: process.env.GITHUB_MODELS_ENDPOINT,
    huggingfaceApiKey: process.env.HUGGINGFACE_API_KEY,
    huggingfaceModel: process.env.HUGGINGFACE_MODEL
  };
}