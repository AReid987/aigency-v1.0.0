'use client'

import { useAuth } from '../../lib/auth-context'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
import { Button, Avatar } from '@collaboratory/ui'
import Link from 'next/link'

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode
}) {
    const { user, loading, signOut } = useAuth()
    const router = useRouter()

    useEffect(() => {
        if (!loading && !user) {
            router.push('/login')
        }
    }, [user, loading, router])

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
            </div>
        )
    }

    if (!user) {
        return null
    }

    const handleSignOut = async () => {
        await signOut()
        router.push('/')
    }

    return (
        <div className="min-h-screen bg-background">
            {/* Header */}
            <header className="border-b border-gray-800 bg-card/50 backdrop-blur">
                <div className="container mx-auto px-6 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-8">
                            <Link href="/dashboard" className="text-xl font-bold">
                                Collaboratory
                            </Link>
                            <nav className="hidden md:flex space-x-6">
                                <Link
                                    href="/dashboard"
                                    className="text-gray-300 hover:text-white transition-colors"
                                >
                                    Documents
                                </Link>
                                <Link
                                    href="/dashboard/upload"
                                    className="text-gray-300 hover:text-white transition-colors"
                                >
                                    Upload
                                </Link>
                            </nav>
                        </div>

                        <div className="flex items-center space-x-4">
                            <Link href="/dashboard/profile">
                                <Avatar className="h-8 w-8">
                                    {user.user_metadata?.full_name?.[0] || user.email?.[0] || 'U'}
                                </Avatar>
                            </Link>
                            <Button
                                variant="outline"
                                onClick={handleSignOut}
                                className="text-sm"
                            >
                                Sign Out
                            </Button>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="container mx-auto px-6 py-8">
                {children}
            </main>
        </div>
    )
}
