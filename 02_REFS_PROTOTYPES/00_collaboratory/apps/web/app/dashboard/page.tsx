'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '../../lib/auth-context'
import { createClient } from '../../lib/supabase'
import { Button } from '@collaboratory/ui'
import { Card, CardHeader, CardTitle, CardContent } from '@collaboratory/ui'
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator } from '@collaboratory/ui'
import { IconGridDots, IconList, IconDots, IconUpload, IconUsers, IconClock, IconTrash, IconShare, IconDownload, IconEdit } from '@tabler/icons-react'

interface Document {
    id: string
    title: string
    description?: string
    file_type: string
    file_size: number
    file_url?: string
    created_at: string
    owner_id: string
    tags: string[]
}

function ChatSidebar() {
    return (
        <div className="bg-black/50 backdrop-blur-md border border-white/20 rounded-lg p-4 text-white flex flex-col">
            <h2 className="text-xl font-semibold mb-4">Chat UI (Placeholder)</h2>
            <div className="flex-grow overflow-auto">
                {/* Chat messages will go here */}
                <p className="text-gray-300">Chat messages will appear here.</p>
            </div>
            <input
                type="text"
                placeholder="Type a message..."
                className="mt-4 p-2 rounded bg-white/10 border border-white/30 focus:outline-none focus:ring-2 focus:ring-primary"
            />
        </div>
    )
}

function DocsBrowser({ documents }: { documents: Document[] }) {
    return (
        <div className="bg-black/50 backdrop-blur-md border border-white/20 rounded-lg p-4 text-white overflow-auto">
            <h2 className="text-xl font-semibold mb-4">Embedded Docs Browser (Placeholder)</h2>
            {documents.length === 0 ? (
                <p className="text-gray-300">No documents available.</p>
            ) : (
                <ul className="space-y-2">
                    {documents.map((doc) => (
                        <li
                            key={doc.id}
                            className="p-2 bg-white/10 rounded hover:bg-white/20 cursor-pointer"
                        >
                            {doc.title}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    )
}

export default function DashboardPage() {
    const { user, loading, signOut } = useAuth()
    const router = useRouter()
    const [documents, setDocuments] = useState<Document[]>([])
    const [selectedDocs, setSelectedDocs] = useState<Set<string>>(new Set())
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState('')
    const supabase = createClient()

    useEffect(() => {
        if (!loading && !user) {
            router.push('/login')
        }
    }, [user, loading, router])

    useEffect(() => {
        if (user) {
            fetchDocuments()
        }
    }, [user])

    const fetchDocuments = async () => {
        setIsLoading(true)
        setError('')
        try {
            const { data: { session } } = await supabase.auth.getSession()
            if (!session?.access_token) {
                return
            }

            const response = await fetch('http://localhost:8000/api/documents', {
                headers: {
                    Authorization: `Bearer ${session.access_token}`,
                    'Content-Type': 'application/json',
                },
            })
            if (response.ok) {
                const docs = await response.json()
                setDocuments(docs)
            } else {
                throw new Error('Failed to fetch documents')
            }
        } catch (error) {
            setError('Error loading documents. Please try again.')
            console.error('Error fetching documents:', error)
        } finally {
            setIsLoading(false)
        }
    }

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
        )
    }

    return (
        <div className="container mx-auto px-4 py-8 flex gap-6 min-h-screen">
            <aside className="w-1/4">
                <ChatSidebar />
            </aside>
            <main className="w-3/4">
                <DocsBrowser documents={documents} />
            </main>
        </div>
    )
}
