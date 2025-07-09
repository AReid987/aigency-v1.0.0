import type { InferSelectModel, InferInsertModel } from 'drizzle-orm';
import type {
  users,
  teams,
  teamMemberships,
  knowledgeBases,
  documents,
  chunks,
  agents,
  sessions,
  queries,
} from './schema';

// Select types (for reading from database)
export type User = InferSelectModel<typeof users>;
export type Team = InferSelectModel<typeof teams>;
export type TeamMembership = InferSelectModel<typeof teamMemberships>;
export type KnowledgeBase = InferSelectModel<typeof knowledgeBases>;
export type Document = InferSelectModel<typeof documents>;
export type Chunk = InferSelectModel<typeof chunks>;
export type Agent = InferSelectModel<typeof agents>;
export type Session = InferSelectModel<typeof sessions>;
export type Query = InferSelectModel<typeof queries>;

// Insert types (for creating new records)
export type NewUser = InferInsertModel<typeof users>;
export type NewTeam = InferInsertModel<typeof teams>;
export type NewTeamMembership = InferInsertModel<typeof teamMemberships>;
export type NewKnowledgeBase = InferInsertModel<typeof knowledgeBases>;
export type NewDocument = InferInsertModel<typeof documents>;
export type NewChunk = InferInsertModel<typeof chunks>;
export type NewAgent = InferInsertModel<typeof agents>;
export type NewSession = InferInsertModel<typeof sessions>;
export type NewQuery = InferInsertModel<typeof queries>;

// Enum types
export type UserRole = 'USER' | 'ADMIN';
export type TeamRole = 'MEMBER' | 'EDITOR' | 'ADMIN' | 'OWNER';
export type ContentType = 'TEXT' | 'MARKDOWN' | 'HTML' | 'PDF' | 'CODE' | 'JSON';
export type AgentType = 'ASSISTANT' | 'RESEARCHER' | 'CODER' | 'ANALYST' | 'CREATIVE' | 'CUSTOM';

// Extended types with relations
export type UserWithRelations = User & {
  knowledgeBases?: KnowledgeBase[];
  agents?: Agent[];
  sessions?: Session[];
  queries?: Query[];
  teamMemberships?: (TeamMembership & { team: Team })[];
};

export type KnowledgeBaseWithRelations = KnowledgeBase & {
  owner?: User;
  team?: Team;
  documents?: Document[];
  agents?: Agent[];
};

export type DocumentWithRelations = Document & {
  knowledgeBase?: KnowledgeBase;
  chunks?: Chunk[];
};

export type AgentWithRelations = Agent & {
  owner?: User;
  knowledgeBase?: KnowledgeBase;
  sessions?: Session[];
};

export type SessionWithRelations = Session & {
  user?: User;
  agent?: Agent;
  queries?: Query[];
};

export type TeamWithRelations = Team & {
  memberships?: (TeamMembership & { user: User })[];
  knowledgeBases?: KnowledgeBase[];
};

// API response types
export type ApiResponse<T> = {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
};

export type PaginatedResponse<T> = ApiResponse<{
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}>;

// Search and filter types
export type SearchFilters = {
  query?: string;
  contentType?: ContentType;
  agentType?: AgentType;
  dateFrom?: Date;
  dateTo?: Date;
  ownerId?: string;
  teamId?: string;
};

export type SortOptions = {
  field: string;
  direction: 'asc' | 'desc';
};

export type PaginationOptions = {
  page: number;
  pageSize: number;
  sort?: SortOptions;
};
