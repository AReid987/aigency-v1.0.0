#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const http = require('http');
const { Select, MultiSelect } = require('enquirer');

// Get all app and package directories for scopes
const getDirectories = (source) => {
  try {
    return fs.readdirSync(source, { withFileTypes: true })
      .filter(dirent => dirent.isDirectory())
      .map(dirent => dirent.name);
  } catch (error) {
    return [];
  }
};

// Get scopes from apps and packages directories
const getScopes = () => {
  const scopes = [];
  const rootDir = path.resolve(__dirname, '..');
  
  try {
    const apps = getDirectories(path.join(rootDir, 'apps'));
    const packages = getDirectories(path.join(rootDir, 'packages'));
    
    return [...apps, ...packages];
  } catch (error) {
    return scopes;
  }
};

// Get the staged changes
function getStagedChanges() {
  try {
    return execSync('git diff --cached').toString();
  } catch (error) {
    console.error('Error getting staged changes:', error.message);
    return '';
  }
}

// Generate commit message using Ollama with retry logic
async function generateCommitMessage(diff, type, scopes) {
  return new Promise((resolve) => {
    const scopeText = scopes.length > 0 ? `(${scopes.join(',')})` : '';
    
    // Limit the diff size to avoid overwhelming the API
    const truncatedDiff = diff.length > 5000 ? diff.substring(0, 5000) + "\n... [diff truncated for brevity]" : diff;
    
    const prompt = `
You are an expert developer helping write a concise and informative git commit message.
The commit is of type: ${type}${scopeText ? ` with scopes: ${scopeText}` : ''}

Here is the git diff of the staged changes:
\`\`\`
${truncatedDiff}
\`\`\`

Please generate a short, clear commit message (50-70 characters) that follows conventional commit format.
The message should be in the format "${type}${scopeText}: <description>"
Do not include the type or scope prefix in your response, just provide the commit message text.
`;

    // Fall back to API approach directly - skip CLI attempt
    const data = JSON.stringify({
      model: 'gemma3',
      prompt: prompt,
      stream: false,
      options: {
        temperature: 0.3,
        top_p: 0.9,
        max_tokens: 100
      }
    });

    const options = {
      hostname: 'localhost',
      port: 11434,
      path: '/api/generate',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length
      },
      timeout: 10000 // 10 second timeout
    };

    const req = http.request(options, (res) => {
      let responseData = '';

      res.on('data', (chunk) => {
        responseData += chunk;
      });

      res.on('end', () => {
        try {
          const parsedData = JSON.parse(responseData);
          if (parsedData && parsedData.response) {
            resolve(parsedData.response.trim());
          } else {
            console.error('Unexpected response format from Ollama:', responseData);
            resolve('update project configuration'); // Default message if we can't parse the response
          }
        } catch (error) {
          console.error('Error parsing Ollama response:', error);
          console.error('Raw response:', responseData);
          resolve('update project configuration'); // Default message if we can't parse the response
        }
      });
    });

    req.on('error', (error) => {
      console.error('Error making request to Ollama:', error);
      resolve('update project configuration'); // Default message if request fails
    });

    req.on('timeout', () => {
      console.error('Request to Ollama timed out');
      req.destroy();
      resolve('update project configuration');
    });

    req.write(data);
    req.end();
    
    // Set a timeout as a backup in case the request hangs
    setTimeout(() => {
      resolve('update project configuration');
    }, 15000); // 15 seconds total timeout
  });
}

// Main function
async function main() {
  const diff = getStagedChanges();
  
  if (!diff) {
    console.error('No staged changes found');
    process.exit(1);
  }

  // Define commit types with emojis
  const types = [
    { name: 'feat:     ✨  A new feature', value: 'feat' },
    { name: 'fix:      🐛  A bug fix', value: 'fix' },
    { name: 'docs:     📝  Documentation only changes', value: 'docs' },
    { name: 'style:    💄  Changes that do not affect the meaning of the code', value: 'style' },
    { name: 'refactor: ♻️   A code change that neither fixes a bug nor adds a feature', value: 'refactor' },
    { name: 'perf:     ⚡️  A code change that improves performance', value: 'perf' },
    { name: 'test:     ✅  Adding missing tests or correcting existing tests', value: 'test' },
    { name: 'build:    📦️  Changes that affect the build system or external dependencies', value: 'build' },
    { name: 'ci:       🎡  Changes to our CI configuration files and scripts', value: 'ci' },
    { name: 'chore:    🔨  Other changes that don\'t modify src or test files', value: 'chore' },
    { name: 'revert:   ⏪️  Reverts a previous commit', value: 'revert' }
  ];

  // Prompt for commit type
  const typePrompt = new Select({
    name: 'commitType',
    message: 'Select the type of change that you\'re committing:',
    choices: types.map(type => type.name),
    initial: 0
  });

  let selectedType;
  try {
    const answer = await typePrompt.run();
    selectedType = types.find(type => type.name === answer).value;
  } catch (error) {
    console.error('Commit type selection cancelled');
    process.exit(1);
  }

  // Get available scopes
  const availableScopes = getScopes();
  availableScopes.push('custom', 'empty');

  // Prompt for scopes if available
  let selectedScopes = [];
  if (availableScopes.length > 0) {
    const scopePrompt = new MultiSelect({
      name: 'commitScopes',
      message: 'Select the scope(s) this component affects:',
      choices: availableScopes,
      result(names) {
        return this.map(names);
      }
    });

    try {
      const scopeAnswers = await scopePrompt.run();
      
      // Handle custom scope
      if (scopeAnswers.custom) {
        const { Input } = require('enquirer');
        const customScopePrompt = new Input({
          name: 'customScope',
          message: 'Enter custom scope:'
        });
        
        const customScope = await customScopePrompt.run();
        if (customScope) {
          delete scopeAnswers.custom;
          scopeAnswers[customScope] = true;
        }
      }
      
      // Remove 'empty' from scopes if selected
      if (scopeAnswers.empty) {
        delete scopeAnswers.empty;
      }
      
      selectedScopes = Object.keys(scopeAnswers);
    } catch (error) {
      console.error('Scope selection cancelled');
      process.exit(1);
    }
  }

  console.log(`\nGenerating commit message for type: ${selectedType}${selectedScopes.length > 0 ? ` with scopes: ${selectedScopes.join(',')}` : ''}...`);
  
  try {
    const message = await generateCommitMessage(diff, selectedType, selectedScopes);
    
    const scopeText = selectedScopes.length > 0 ? `(${selectedScopes.join(',')})` : '';
    const fullMessage = `${selectedType}${scopeText}: ${message}`;
    
    console.log('\nGenerated commit message:');
    console.log(fullMessage);
    
    // Ask user if they want to use this message
    const { Confirm } = require('enquirer');
    const confirmPrompt = new Confirm({
      name: 'useMessage',
      message: 'Use this message?',
      initial: true
    });

    const useMessage = await confirmPrompt.run();
    
    if (useMessage) {
      // Use the generated message
      try {
        execSync(`git commit -m "${fullMessage.replace(/"/g, '\\"')}"`);
        console.log('Commit successful!');
      } catch (error) {
        console.error('Error creating commit:', error.message);
      }
    } else {
      console.log('Commit aborted. You can create your commit manually.');
    }
  } catch (error) {
    console.error('Failed to generate commit message:', error);
    process.exit(1);
  }
}

main();
