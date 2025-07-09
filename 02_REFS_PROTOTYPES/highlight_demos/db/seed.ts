import { db } from './config';
import { 
  userUtils, 
  teamUtils, 
  knowledgeBaseUtils, 
  agentUtils, 
  documentUtils 
} from './utils';

async function seed() {
  console.log('🌱 Starting database seed...');

  try {
    // Create admin user
    const adminUser = await userUtils.create({
      name: 'Admin User',
      email: 'admin@knowledgeos.com',
      role: 'ADMIN',
      profileImage: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face',
    });
    console.log('✅ Created admin user:', adminUser.email);

    // Create regular user
    const regularUser = await userUtils.create({
      name: 'John Doe',
      email: 'john@example.com',
      role: 'USER',
      profileImage: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop&crop=face',
    });
    console.log('✅ Created regular user:', regularUser.email);

    // Create a team
    const team = await teamUtils.create({
      name: 'AI Research Team',
      description: 'A team focused on AI research and development',
    });
    console.log('✅ Created team:', team.name);

    // Add users to team
    await teamUtils.addMember({
      teamId: team.id,
      userId: adminUser.id,
      role: 'OWNER',
    });

    await teamUtils.addMember({
      teamId: team.id,
      userId: regularUser.id,
      role: 'MEMBER',
    });
    console.log('✅ Added users to team');

    // Create knowledge bases
    const personalKB = await knowledgeBaseUtils.create({
      name: 'Personal Knowledge Base',
      description: 'My personal collection of knowledge and documents',
      ownerId: regularUser.id,
    });

    const teamKB = await knowledgeBaseUtils.create({
      name: 'Team Knowledge Base',
      description: 'Shared knowledge base for the AI research team',
      ownerId: adminUser.id,
      teamId: team.id,
    });
    console.log('✅ Created knowledge bases');

    // Create sample documents
    const doc1 = await documentUtils.create({
      title: 'Introduction to AI Agents',
      content: `# Introduction to AI Agents

AI agents are autonomous software entities that can perceive their environment, make decisions, and take actions to achieve specific goals. They are designed to operate independently and can adapt to changing conditions.

## Key Characteristics

1. **Autonomy**: AI agents can operate without direct human intervention
2. **Reactivity**: They can respond to changes in their environment
3. **Proactivity**: They can take initiative to achieve their goals
4. **Social Ability**: They can interact with other agents and humans

## Types of AI Agents

- **Simple Reflex Agents**: React to current percepts
- **Model-based Agents**: Maintain internal state
- **Goal-based Agents**: Act to achieve specific goals
- **Utility-based Agents**: Maximize expected utility
- **Learning Agents**: Improve performance over time

This document provides a foundation for understanding how AI agents work and their applications in various domains.`,
      contentType: 'MARKDOWN',
      knowledgeBaseId: personalKB.id,
      metadata: {
        tags: ['AI', 'agents', 'introduction'],
        author: 'John Doe',
        version: '1.0',
      },
    });

    const doc2 = await documentUtils.create({
      title: 'Team Collaboration Guidelines',
      content: `# Team Collaboration Guidelines

## Communication Protocols

- Use Slack for daily communication
- Weekly team meetings every Monday at 10 AM
- Document all decisions in our knowledge base

## Code Review Process

1. Create feature branch
2. Submit pull request
3. At least 2 reviewers required
4. All tests must pass
5. Merge after approval

## Knowledge Sharing

- Document learnings in the team knowledge base
- Share interesting articles and papers
- Present findings in monthly tech talks`,
      contentType: 'MARKDOWN',
      knowledgeBaseId: teamKB.id,
      metadata: {
        tags: ['team', 'collaboration', 'guidelines'],
        author: 'Admin User',
        version: '1.0',
      },
    });
    console.log('✅ Created sample documents');

    // Create AI agents
    const assistantAgent = await agentUtils.create({
      name: 'AI Assistant',
      description: 'A helpful AI assistant that can answer questions and provide information',
      type: 'ASSISTANT',
      capabilities: ['Q&A', 'Research', 'Writing', 'Analysis'],
      config: {
        model: 'gpt-4',
        temperature: 0.7,
        maxTokens: 2048,
        systemPrompt: 'You are a helpful AI assistant. Provide accurate and helpful responses.',
      },
      ownerId: regularUser.id,
      knowledgeBaseId: personalKB.id,
    });

    const coderAgent = await agentUtils.create({
      name: 'Code Expert',
      description: 'Specialized in programming, code review, and software development',
      type: 'CODER',
      capabilities: ['Coding', 'Debugging', 'Code Review', 'Architecture'],
      config: {
        model: 'gpt-4',
        temperature: 0.3,
        maxTokens: 4096,
        systemPrompt: 'You are an expert software developer. Help with coding tasks, debugging, and best practices.',
        languages: ['JavaScript', 'TypeScript', 'Python', 'Go', 'Rust'],
      },
      ownerId: adminUser.id,
      knowledgeBaseId: teamKB.id,
    });

    const researcherAgent = await agentUtils.create({
      name: 'Research Assistant',
      description: 'Specialized in research, analysis, and information gathering',
      type: 'RESEARCHER',
      capabilities: ['Research', 'Analysis', 'Data Processing', 'Report Generation'],
      config: {
        model: 'gpt-4',
        temperature: 0.5,
        maxTokens: 3072,
        systemPrompt: 'You are a research assistant. Help with research tasks, analysis, and generating insights.',
        searchEnabled: true,
        citationStyle: 'APA',
      },
      ownerId: adminUser.id,
      knowledgeBaseId: teamKB.id,
    });
    console.log('✅ Created AI agents');

    console.log('🎉 Database seed completed successfully!');
    console.log('\n📊 Summary:');
    console.log(`- Users: 2 (1 admin, 1 regular)`);
    console.log(`- Teams: 1`);
    console.log(`- Knowledge Bases: 2`);
    console.log(`- Documents: 2`);
    console.log(`- Agents: 3`);

  } catch (error) {
    console.error('❌ Error seeding database:', error);
    throw error;
  }
}

// Run seed if this file is executed directly
if (require.main === module) {
  seed()
    .then(() => {
      console.log('✅ Seed completed');
      process.exit(0);
    })
    .catch((error) => {
      console.error('❌ Seed failed:', error);
      process.exit(1);
    });
}

export { seed };
