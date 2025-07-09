'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '../../../lib/auth-context'
import { createClient } from '../../../lib/supabase'

export default function UploadPage() {
    const { user } = useAuth()
    const router = useRouter()
    const [uploading, setUploading] = useState(false)
    const [error, setError] = useState('')
    const supabase = createClient()

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        setUploading(true)
        setError('')

        try {
            const formData = new FormData(e.currentTarget)
            const { data: { session } } = await supabase.auth.getSession()

            if (!session?.access_token) {
                throw new Error('No authentication token found')
            }

            const response = await fetch('http://localhost:8000/api/documents', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${session.access_token}`,
                },
                body: formData,
            })

            if (!response.ok) {
                throw new Error('Failed to upload document')
            }

            // Success - redirect to dashboard
            router.push('/dashboard')
        } catch (err: any) {
            setError(err.message)
        } finally {
            setUploading(false)
        }
    }

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="max-w-2xl mx-auto">
                <div className="flex items-center justify-between mb-8">
                    <h1 className="text-3xl font-bold">Upload Document</h1>
                    <button
                        onClick={() => router.push('/dashboard')}
                        className="text-gray-600 hover:text-gray-900"
                    >
                        Back to Dashboard
                    </button>
                </div>

                <div className="bg-white p-6 rounded-lg shadow-md">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        {error && (
                            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded">
                                {error}
                            </div>
                        )}

                        <div>
                            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                                Document Title
                            </label>
                            <input
                                id="title"
                                name="title"
                                type="text"
                                required
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                placeholder="Enter document title"
                            />
                        </div>

                        <div>
                            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                                Description
                            </label>
                            <textarea
                                id="description"
                                name="description"
                                rows={3}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                placeholder="Enter document description (optional)"
                            />
                        </div>

                        <div>
                            <label htmlFor="file" className="block text-sm font-medium text-gray-700 mb-2">
                                File
                            </label>
                            <input
                                id="file"
                                name="file"
                                type="file"
                                required
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                accept=".pdf,.doc,.docx,.txt,.md"
                            />
                            <p className="mt-1 text-sm text-gray-500">
                                Supported formats: PDF, Word, Text, Markdown
                            </p>
                        </div>

                        <div className="flex justify-end space-x-4">
                            <button
                                type="button"
                                onClick={() => router.push('/dashboard')}
                                className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
                                disabled={uploading}
                            >
                                Cancel
                            </button>
                            <button
                                type="submit"
                                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
                                disabled={uploading}
                            >
                                {uploading ? 'Uploading...' : 'Upload Document'}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}
