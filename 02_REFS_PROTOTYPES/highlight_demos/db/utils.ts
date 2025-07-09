import { eq, and, desc, asc } from 'drizzle-orm';
import { db } from './config';
import { 
  users, 
  knowledgeBases, 
  documents, 
  chunks, 
  agents, 
  sessions, 
  queries, 
  teams, 
  teamMemberships 
} from './schema';

// User utilities
export const userUtils = {
  // Create a new user
  async create(data: {
    name: string;
    email: string;
    profileImage?: string;
    role?: 'USER' | 'ADMIN';
  }) {
    const [user] = await db.insert(users).values(data).returning();
    return user;
  },

  // Get user by ID
  async getById(id: string) {
    const [user] = await db.select().from(users).where(eq(users.id, id));
    return user;
  },

  // Get user by email
  async getByEmail(email: string) {
    const [user] = await db.select().from(users).where(eq(users.email, email));
    return user;
  },

  // Update user
  async update(id: string, data: Partial<typeof users.$inferInsert>) {
    const [user] = await db
      .update(users)
      .set({ ...data, updatedAt: new Date() })
      .where(eq(users.id, id))
      .returning();
    return user;
  },

  // Delete user
  async delete(id: string) {
    await db.delete(users).where(eq(users.id, id));
  },
};

// Knowledge Base utilities
export const knowledgeBaseUtils = {
  // Create knowledge base
  async create(data: {
    name: string;
    description?: string;
    ownerId: string;
    teamId?: string;
  }) {
    // Input validation
    if (!data.name?.trim()) {
      throw new Error('Knowledge base name is required');
    }
    if (!data.ownerId) {
      throw new Error('Owner ID is required');
    }

    try {
      // Verify owner exists
      const owner = await userUtils.getById(data.ownerId);
      if (!owner) {
        throw new Error('Specified owner does not exist');
      }

      const [kb] = await db
        .insert(knowledgeBases)
        .values({
          ...data,
          name: data.name.trim(),
          description: data.description?.trim(),
        })
        .returning();
      
      return kb;
    } catch (error: any) {
      if (error.code === '23505') { // Unique violation
        throw new Error('A knowledge base with this name already exists');
      } else if (error.code === '23503') { // Foreign key violation
        throw new Error('Invalid owner or team reference');
      }
      console.error('Error creating knowledge base:', error);
      throw new Error('Failed to create knowledge base');
    }
  },

  // Get knowledge base by ID with relations
  async getById(id: string) {
    if (!id) {
      throw new Error('Knowledge base ID is required');
    }

    try {
      const [kb] = await db
        .select()
        .from(knowledgeBases)
        .where(eq(knowledgeBases.id, id));
      
      if (!kb) {
        throw new Error('Knowledge base not found');
      }
      
      return kb;
    } catch (error) {
      console.error(`Error fetching knowledge base ${id}:`, error);
      throw new Error('Failed to retrieve knowledge base');
    }
  },

  // Get knowledge bases by owner
  async getByOwner(ownerId: string) {
    if (!ownerId) {
      throw new Error('Owner ID is required');
    }

    try {
      // Verify owner exists
      const owner = await userUtils.getById(ownerId);
      if (!owner) {
        throw new Error('Specified owner does not exist');
      }

      return await db
        .select()
        .from(knowledgeBases)
        .where(eq(knowledgeBases.ownerId, ownerId))
        .orderBy(desc(knowledgeBases.createdAt));
    } catch (error) {
      console.error(`Error fetching knowledge bases for owner ${ownerId}:`, error);
      throw new Error('Failed to retrieve knowledge bases');
    }
  },

  // Update knowledge base
  async update(id: string, data: Partial<typeof knowledgeBases.$inferInsert>) {
    if (!id) {
      throw new Error('Knowledge base ID is required');
    }
    
    if (data.name !== undefined && !data.name.trim()) {
      throw new Error('Knowledge base name cannot be empty');
    }

    try {
      // Verify knowledge base exists
      const existingKb = await this.getById(id);
      if (!existingKb) {
        throw new Error('Knowledge base not found');
      }

      // If owner is being updated, verify new owner exists
      if (data.ownerId) {
        const owner = await userUtils.getById(data.ownerId);
        if (!owner) {
          throw new Error('Specified owner does not exist');
        }
      }

      const [kb] = await db
        .update(knowledgeBases)
        .set({ 
          ...data,
          name: data.name?.trim(),
          description: data.description?.trim(),
          updatedAt: new Date() 
        })
        .where(eq(knowledgeBases.id, id))
        .returning();
      
      if (!kb) {
        throw new Error('Failed to update knowledge base');
      }
      
      return kb;
    } catch (error: any) {
      if (error.code === '23505') { // Unique violation
        throw new Error('A knowledge base with this name already exists');
      } else if (error.code === '23503') { // Foreign key violation
        throw new Error('Invalid owner or team reference');
      }
      console.error(`Error updating knowledge base ${id}:`, error);
      throw new Error('Failed to update knowledge base');
    }
  },

  // Delete knowledge base
  async delete(id: string) {
    if (!id) {
      throw new Error('Knowledge base ID is required');
    }

    try {
      // Verify knowledge base exists
      const kb = await this.getById(id);
      if (!kb) {
        throw new Error('Knowledge base not found');
      }

      await db
        .delete(knowledgeBases)
        .where(eq(knowledgeBases.id, id));
      
      return { success: true, message: 'Knowledge base deleted successfully' };
    } catch (error) {
      console.error(`Error deleting knowledge base ${id}:`, error);
      throw new Error('Failed to delete knowledge base');
    }
  },
};

// Document utilities
export const documentUtils = {
  // Create document
  async create(data: {
    title: string;
    content: string;
    contentType?: 'TEXT' | 'MARKDOWN' | 'HTML' | 'PDF' | 'CODE' | 'JSON';
    knowledgeBaseId: string;
    vectorId?: string;
    metadata?: any;
  }) {
    const [doc] = await db.insert(documents).values(data).returning();
    return doc;
  },

  // Get document by ID
  async getById(id: string) {
    const [doc] = await db.select().from(documents).where(eq(documents.id, id));
    return doc;
  },

  // Get documents by knowledge base
  async getByKnowledgeBase(knowledgeBaseId: string) {
    return await db
      .select()
      .from(documents)
      .where(eq(documents.knowledgeBaseId, knowledgeBaseId))
      .orderBy(desc(documents.createdAt));
  },

  // Update document
  async update(id: string, data: Partial<typeof documents.$inferInsert>) {
    const [doc] = await db
      .update(documents)
      .set({ ...data, updatedAt: new Date() })
      .where(eq(documents.id, id))
      .returning();
    return doc;
  },

  // Delete document
  async delete(id: string) {
    await db.delete(documents).where(eq(documents.id, id));
  },
};

// Chunk utilities
export const chunkUtils = {
  // Create chunk
  async create(data: {
    content: string;
    vectorId: string;
    startIndex: number;
    endIndex: number;
    documentId: string;
    embeddings?: number[];
  }) {
    const [chunk] = await db.insert(chunks).values(data).returning();
    return chunk;
  },

  // Get chunks by document
  async getByDocument(documentId: string) {
    return await db
      .select()
      .from(chunks)
      .where(eq(chunks.documentId, documentId))
      .orderBy(asc(chunks.startIndex));
  },

  // Search chunks by vector similarity (placeholder - would need vector extension)
  async searchSimilar(vectorId: string, limit: number = 10) {
    // This would require pgvector extension and similarity search
    // For now, return recent chunks
    return await db
      .select()
      .from(chunks)
      .orderBy(desc(chunks.createdAt))
      .limit(limit);
  },

  // Delete chunk
  async delete(id: string) {
    await db.delete(chunks).where(eq(chunks.id, id));
  },
};

// Agent utilities
export const agentUtils = {
  // Create agent
  async create(data: {
    name: string;
    description?: string;
    type?: 'ASSISTANT' | 'RESEARCHER' | 'CODER' | 'ANALYST' | 'CREATIVE' | 'CUSTOM';
    capabilities: string[];
    config: any;
    ownerId: string;
    knowledgeBaseId?: string;
  }) {
    const [agent] = await db.insert(agents).values(data).returning();
    return agent;
  },

  // Get agent by ID
  async getById(id: string) {
    const [agent] = await db.select().from(agents).where(eq(agents.id, id));
    return agent;
  },

  // Get agents by owner
  async getByOwner(ownerId: string) {
    return await db
      .select()
      .from(agents)
      .where(eq(agents.ownerId, ownerId))
      .orderBy(desc(agents.createdAt));
  },

  // Update agent
  async update(id: string, data: Partial<typeof agents.$inferInsert>) {
    const [agent] = await db
      .update(agents)
      .set({ ...data, updatedAt: new Date() })
      .where(eq(agents.id, id))
      .returning();
    return agent;
  },

  // Delete agent
  async delete(id: string) {
    await db.delete(agents).where(eq(agents.id, id));
  },
};

// Session utilities
export const sessionUtils = {
  // Create session
  async create(data: {
    name?: string;
    userId: string;
    agentId: string;
  }) {
    const [session] = await db.insert(sessions).values(data).returning();
    return session;
  },

  // Get session by ID
  async getById(id: string) {
    const [session] = await db.select().from(sessions).where(eq(sessions.id, id));
    return session;
  },

  // Get sessions by user
  async getByUser(userId: string) {
    return await db
      .select()
      .from(sessions)
      .where(eq(sessions.userId, userId))
      .orderBy(desc(sessions.createdAt));
  },

  // Update session
  async update(id: string, data: Partial<typeof sessions.$inferInsert>) {
    const [session] = await db
      .update(sessions)
      .set({ ...data, updatedAt: new Date() })
      .where(eq(sessions.id, id))
      .returning();
    return session;
  },

  // Delete session
  async delete(id: string) {
    await db.delete(sessions).where(eq(sessions.id, id));
  },
};

// Query utilities
export const queryUtils = {
  // Create query
  async create(data: {
    content: string;
    response: string;
    sessionId: string;
    userId: string;
    metadata?: any;
  }) {
    const [query] = await db.insert(queries).values(data).returning();
    return query;
  },

  // Get queries by session
  async getBySession(sessionId: string) {
    return await db
      .select()
      .from(queries)
      .where(eq(queries.sessionId, sessionId))
      .orderBy(asc(queries.createdAt));
  },

  // Get recent queries by user
  async getRecentByUser(userId: string, limit: number = 50) {
    return await db
      .select()
      .from(queries)
      .where(eq(queries.userId, userId))
      .orderBy(desc(queries.createdAt))
      .limit(limit);
  },

  // Delete query
  async delete(id: string) {
    await db.delete(queries).where(eq(queries.id, id));
  },
};

// Team utilities
export const teamUtils = {
  // Create team
  async create(data: {
    name: string;
    description?: string;
  }) {
    const [team] = await db.insert(teams).values(data).returning();
    return team;
  },

  // Get team by ID
  async getById(id: string) {
    const [team] = await db.select().from(teams).where(eq(teams.id, id));
    return team;
  },

  // Add member to team
  async addMember(data: {
    teamId: string;
    userId: string;
    role?: 'MEMBER' | 'EDITOR' | 'ADMIN' | 'OWNER';
  }) {
    const [membership] = await db.insert(teamMemberships).values(data).returning();
    return membership;
  },

  // Get team members
  async getMembers(teamId: string) {
    return await db
      .select({
        id: teamMemberships.id,
        role: teamMemberships.role,
        user: users,
        createdAt: teamMemberships.createdAt,
      })
      .from(teamMemberships)
      .innerJoin(users, eq(teamMemberships.userId, users.id))
      .where(eq(teamMemberships.teamId, teamId));
  },

  // Remove member from team
  async removeMember(teamId: string, userId: string) {
    await db
      .delete(teamMemberships)
      .where(and(
        eq(teamMemberships.teamId, teamId),
        eq(teamMemberships.userId, userId)
      ));
  },

  // Update member role
  async updateMemberRole(teamId: string, userId: string, role: 'MEMBER' | 'EDITOR' | 'ADMIN' | 'OWNER') {
    const [membership] = await db
      .update(teamMemberships)
      .set({ role, updatedAt: new Date() })
      .where(and(
        eq(teamMemberships.teamId, teamId),
        eq(teamMemberships.userId, userId)
      ))
      .returning();
    return membership;
  },

  // Delete team
  async delete(id: string) {
    await db.delete(teams).where(eq(teams.id, id));
  },
};
