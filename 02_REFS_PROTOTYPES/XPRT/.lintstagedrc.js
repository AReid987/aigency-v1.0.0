module.exports = {
  // Format all file types with Prettier
  '*.{js,jsx,ts,tsx,json,md,mdx,css,html,yml,yaml}': ['prettier --write'],
  
  // Lint JS/TS files
  '*.{js,jsx,ts,tsx}': ['eslint --fix'],
  
  // Type check TS files
  '*.{ts,tsx}': () => 'tsc --noEmit',
};
