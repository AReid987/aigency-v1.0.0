import { pgEnum } from 'drizzle-orm/pg-core';

// User role enum
export const userRoleEnum = pgEnum('user_role', ['USER', 'ADMIN']);

// Team role enum  
export const teamRoleEnum = pgEnum('team_role', ['MEMBER', 'EDITOR', 'ADMIN', 'OWNER']);

// Content type enum
export const contentTypeEnum = pgEnum('content_type', [
  'TEXT',
  'MARKDOWN', 
  'HTML',
  'PDF',
  'CODE',
  'JSON'
]);

// Agent type enum
export const agentTypeEnum = pgEnum('agent_type', [
  'ASSISTANT',
  'RESEARCHER',
  'CODER', 
  'ANALYST',
  'CREATIVE',
  'CUSTOM'
]);
