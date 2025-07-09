// Simple test script to check AI providers
const { getAvailableProviders, getAvailableModels, createAIClient } = require('./lib/ai-providers.ts');

async function testProviders() {
  try {
    console.log('Testing AI Providers...\n');
    
    // Check available providers
    const providers = getAvailableProviders();
    console.log('Available Providers:', providers.length);
    providers.forEach(p => {
      console.log(`- ${p.name} (${p.id}): ${p.models.length} models`);
    });
    
    // Check available models
    const models = getAvailableModels();
    console.log('\nAvailable Models:', models.length);
    models.slice(0, 5).forEach(m => {
      console.log(`- ${m.name} (${m.provider})`);
    });
    
    // Test first provider
    if (providers.length > 0) {
      console.log(`\nTesting ${providers[0].name}...`);
      const client = createAIClient(providers[0].id);
      
      const response = await client.chat({
        model: providers[0].models[0].id,
        messages: [{ role: 'user', content: 'Hello! Just testing the connection.' }],
        maxTokens: 50
      });
      
      console.log('Test successful!');
      console.log('Response:', response.choices[0]?.message?.content);
    } else {
      console.log('No providers available!');
    }
    
  } catch (error) {
    console.error('Test failed:', error.message);
  }
}

testProviders();
