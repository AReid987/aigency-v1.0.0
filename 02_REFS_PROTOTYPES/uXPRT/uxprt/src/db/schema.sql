-- public.users table is removed. Users are managed by Supabase Auth in auth.users table.

-- Create the profiles table
CREATE TABLE profiles (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    username VARCHAR(50) UNIQUE,
    full_name VARCHAR(100),
    avatar_url TEXT,
    bio TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create a trigger to automatically create a profile for new users
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $
BEGIN
  INSERT INTO public.profiles (user_id, username)
  VALUES (NEW.id, NEW.email);
  RETURN NEW;
END;
$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();

-- Create the projects table
CREATE TABLE projects (
    project_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create the conversations table
CREATE TABLE conversations (
    conversation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id), -- References Supabase Auth users
    start_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP WITH TIME ZONE,
    title VARCHAR(255),
    context JSONB NOT NULL
);

-- Create the artifacts table
CREATE TABLE artifacts (
    artifact_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id), -- References Supabase Auth users
    conversation_id UUID REFERENCES conversations(conversation_id),
    artifact_type VARCHAR(50) NOT NULL,
    generated_data TEXT NOT NULL, -- Using TEXT for now, can be refined to JSONB if needed for structured data
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    version INTEGER DEFAULT 1,
    filename VARCHAR(255)
);

-- Create the search_queries table
CREATE TABLE search_queries (
    query_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id), -- References Supabase Auth users
    query_text TEXT NOT NULL,
    search_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    results JSONB -- Optional: Stored search results
);

-- Create indexes on foreign key columns
-- Note: Supabase automatically creates indexes for foreign keys.
-- These explicit index creations might be redundant or could be adjusted if specific performance needs arise.
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_artifacts_user_id ON artifacts(user_id);
CREATE INDEX idx_artifacts_conversation_id ON artifacts(conversation_id);
CREATE INDEX idx_search_queries_user_id ON search_queries(user_id);

-- Optional indexes based on common query patterns
CREATE INDEX idx_artifacts_artifact_type ON artifacts(artifact_type);
CREATE INDEX idx_search_queries_search_time ON search_queries(search_time);