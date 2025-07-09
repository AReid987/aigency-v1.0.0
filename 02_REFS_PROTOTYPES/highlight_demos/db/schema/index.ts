import {
  pgTable,
  text,
  timestamp,
  varchar,
  json,
  integer,
  real,
  unique,
  foreignKey,
} from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';
import { createId } from '@paralleldrive/cuid2';
import { userRoleEnum, teamRoleEnum, contentTypeEnum, agentTypeEnum } from './enums';

// Users table
export const users = pgTable('users', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  profileImage: text('profile_image'),
  role: userRoleEnum('role').notNull().default('USER'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
});

// Teams table
export const teams = pgTable('teams', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  name: text('name').notNull(),
  description: text('description'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
});

// Team memberships table
export const teamMemberships = pgTable('team_memberships', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  role: teamRoleEnum('role').notNull().default('MEMBER'),
  teamId: text('team_id').notNull(),
  userId: text('user_id').notNull(),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
}, (table) => ({
  teamUserUnique: unique().on(table.teamId, table.userId),
}));

// Knowledge bases table
export const knowledgeBases = pgTable('knowledge_bases', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  name: text('name').notNull(),
  description: text('description'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
  ownerId: text('owner_id').notNull(),
  teamId: text('team_id'),
});

// Documents table
export const documents = pgTable('documents', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  title: text('title').notNull(),
  content: text('content').notNull(),
  contentType: contentTypeEnum('content_type').notNull().default('TEXT'),
  vectorId: text('vector_id').unique(),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
  knowledgeBaseId: text('knowledge_base_id').notNull(),
  metadata: json('metadata'),
});

// Chunks table
export const chunks = pgTable('chunks', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  content: text('content').notNull(),
  vectorId: text('vector_id').notNull().unique(),
  startIndex: integer('start_index').notNull(),
  endIndex: integer('end_index').notNull(),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
  documentId: text('document_id').notNull(),
  embeddings: real('embeddings').array(),
});

// Agents table
export const agents = pgTable('agents', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  name: text('name').notNull(),
  description: text('description'),
  type: agentTypeEnum('type').notNull().default('ASSISTANT'),
  capabilities: text('capabilities').array().notNull().default([]),
  config: json('config').notNull(),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
  ownerId: text('owner_id').notNull(),
  knowledgeBaseId: text('knowledge_base_id'),
});

// Sessions table
export const sessions = pgTable('sessions', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  name: text('name'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
  userId: text('user_id').notNull(),
  agentId: text('agent_id').notNull(),
});

// Queries table
export const queries = pgTable('queries', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  content: text('content').notNull(),
  response: text('response').notNull(),
  metadata: json('metadata'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  sessionId: text('session_id').notNull(),
  userId: text('user_id').notNull(),
});

// Relations
export const usersRelations = relations(users, ({ many }) => ({
  knowledgeBases: many(knowledgeBases),
  agents: many(agents),
  sessions: many(sessions),
  queries: many(queries),
  teamMemberships: many(teamMemberships),
}));

export const teamsRelations = relations(teams, ({ many }) => ({
  memberships: many(teamMemberships),
  knowledgeBases: many(knowledgeBases),
}));

export const teamMembershipsRelations = relations(teamMemberships, ({ one }) => ({
  team: one(teams, {
    fields: [teamMemberships.teamId],
    references: [teams.id],
  }),
  user: one(users, {
    fields: [teamMemberships.userId],
    references: [users.id],
  }),
}));

export const knowledgeBasesRelations = relations(knowledgeBases, ({ one, many }) => ({
  owner: one(users, {
    fields: [knowledgeBases.ownerId],
    references: [users.id],
  }),
  team: one(teams, {
    fields: [knowledgeBases.teamId],
    references: [teams.id],
  }),
  documents: many(documents),
  agents: many(agents),
}));

export const documentsRelations = relations(documents, ({ one, many }) => ({
  knowledgeBase: one(knowledgeBases, {
    fields: [documents.knowledgeBaseId],
    references: [knowledgeBases.id],
  }),
  chunks: many(chunks),
}));

export const chunksRelations = relations(chunks, ({ one }) => ({
  document: one(documents, {
    fields: [chunks.documentId],
    references: [documents.id],
  }),
}));

export const agentsRelations = relations(agents, ({ one, many }) => ({
  owner: one(users, {
    fields: [agents.ownerId],
    references: [users.id],
  }),
  knowledgeBase: one(knowledgeBases, {
    fields: [agents.knowledgeBaseId],
    references: [knowledgeBases.id],
  }),
  sessions: many(sessions),
}));

export const sessionsRelations = relations(sessions, ({ one, many }) => ({
  user: one(users, {
    fields: [sessions.userId],
    references: [users.id],
  }),
  agent: one(agents, {
    fields: [sessions.agentId],
    references: [agents.id],
  }),
  queries: many(queries),
}));

export const queriesRelations = relations(queries, ({ one }) => ({
  session: one(sessions, {
    fields: [queries.sessionId],
    references: [sessions.id],
  }),
  user: one(users, {
    fields: [queries.userId],
    references: [users.id],
  }),
}));

// Export all tables for easy access
export const schema = {
  users,
  teams,
  teamMemberships,
  knowledgeBases,
  documents,
  chunks,
  agents,
  sessions,
  queries,
  // Relations
  usersRelations,
  teamsRelations,
  teamMembershipsRelations,
  knowledgeBasesRelations,
  documentsRelations,
  chunksRelations,
  agentsRelations,
  sessionsRelations,
  queriesRelations,
};
