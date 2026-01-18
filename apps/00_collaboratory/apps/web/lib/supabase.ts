import { createClientComponentClient } from '@supabase/auth-helpers-nextjs'

export const createClient = () => createClientComponentClient<Database>()

export type Database = {
    public: {
        Tables: {
            users: {
                Row: {
                    id: string
                    email: string
                    full_name: string | null
                    avatar_url: string | null
                    created_at: string
                }
                Insert: {
                    id: string
                    email: string
                    full_name?: string | null
                    avatar_url?: string | null
                    created_at?: string
                }
                Update: {
                    id?: string
                    email?: string
                    full_name?: string | null
                    avatar_url?: string | null
                    created_at?: string
                }
            }
            documents: {
                Row: {
                    id: string
                    title: string
                    description: string | null
                    file_url: string
                    file_type: string
                    file_size: number
                    tags: string
                    owner_id: string
                    created_at: string
                    updated_at: string
                }
                Insert: {
                    id: string
                    title: string
                    description?: string | null
                    file_url: string
                    file_type: string
                    file_size: number
                    tags?: string
                    owner_id: string
                    created_at?: string
                    updated_at?: string
                }
                Update: {
                    id?: string
                    title?: string
                    description?: string | null
                    file_url?: string
                    file_type?: string
                    file_size?: number
                    tags?: string
                    owner_id?: string
                    created_at?: string
                    updated_at?: string
                }
            }
        }
    }
}
