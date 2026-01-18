'use client'

import { useState } from 'react'
import { Button, Card, CardHeader, CardTitle, CardContent, Avatar } from '@collaboratory/ui'
import { useAuth } from '../../../lib/auth-context'

export default function ProfilePage() {
    const { user } = useAuth()
    const [fullName, setFullName] = useState(user?.user_metadata?.full_name || '')
    const [email, setEmail] = useState(user?.email || '')
    const [loading, setLoading] = useState(false)
    const [success, setSuccess] = useState('')
    const [error, setError] = useState('')

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        setError('')
        setSuccess('')

        try {
            // For now, we'll simulate the update since we need to set up the API proxy
            // In production, this would update the user profile via Supabase
            await new Promise(resolve => setTimeout(resolve, 1000))

            setSuccess('Profile updated successfully!')
        } catch (error) {
            setError('Failed to update profile. Please try again.')
            console.error('Profile update error:', error)
        } finally {
            setLoading(false)
        }
    }

    const handleAvatarUpload = async (files: FileList) => {
        if (files.length === 0) return

        const file = files[0]
        if (!file.type.startsWith('image/')) {
            setError('Please select an image file')
            return
        }

        setLoading(true)
        setError('')

        try {
            // For now, we'll simulate the avatar upload
            // In production, this would upload to Supabase Storage
            await new Promise(resolve => setTimeout(resolve, 1000))

            setSuccess('Avatar updated successfully!')
        } catch (error) {
            setError('Failed to update avatar. Please try again.')
            console.error('Avatar upload error:', error)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="max-w-2xl mx-auto">
            <div className="mb-8">
                <h1 className="text-3xl font-bold">Profile Settings</h1>
                <p className="text-gray-400 mt-2">
                    Manage your account information and preferences
                </p>
            </div>

            <div className="space-y-6">
                {/* Avatar Section */}
                <Card>
                    <CardHeader>
                        <CardTitle>Profile Picture</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="flex items-center space-x-6">
                            <Avatar
                                className="h-20 w-20 text-2xl"
                                size="lg"
                                fallback={user?.user_metadata?.full_name?.[0] || user?.email?.[0] || 'U'}
                            />
                            <div>
                                <p className="text-sm text-gray-400 mb-2">
                                    Upload a new profile picture
                                </p>
                                <input
                                    type="file"
                                    accept="image/*"
                                    onChange={(e) => e.target.files && handleAvatarUpload(e.target.files)}
                                    className="hidden"
                                    id="avatar-upload"
                                />
                                <label htmlFor="avatar-upload">
                                    <Button variant="outline" disabled={loading} className="cursor-pointer">
                                        {loading ? 'Uploading...' : 'Change Avatar'}
                                    </Button>
                                </label>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                {/* Profile Information */}
                <Card>
                    <CardHeader>
                        <CardTitle>Personal Information</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            {error && (
                                <div className="bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-3 rounded">
                                    {error}
                                </div>
                            )}

                            {success && (
                                <div className="bg-green-500/10 border border-green-500/20 text-green-400 px-4 py-3 rounded">
                                    {success}
                                </div>
                            )}

                            <div>
                                <label htmlFor="fullName" className="block text-sm font-medium mb-2">
                                    Full Name
                                </label>
                                <input
                                    id="fullName"
                                    type="text"
                                    value={fullName}
                                    onChange={(e) => setFullName(e.target.value)}
                                    required
                                    className="w-full px-3 py-2 bg-card border border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                                    placeholder="Enter your full name"
                                />
                            </div>

                            <div>
                                <label htmlFor="email" className="block text-sm font-medium mb-2">
                                    Email Address
                                </label>
                                <input
                                    id="email"
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                    className="w-full px-3 py-2 bg-card border border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                                    placeholder="Enter your email"
                                />
                                <p className="mt-1 text-sm text-gray-400">
                                    Changing your email will require verification
                                </p>
                            </div>

                            <Button
                                type="submit"
                                disabled={loading}
                                className="w-full"
                            >
                                {loading ? 'Updating...' : 'Update Profile'}
                            </Button>
                        </form>
                    </CardContent>
                </Card>

                {/* Account Settings */}
                <Card>
                    <CardHeader>
                        <CardTitle>Account Settings</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            <div className="flex items-center justify-between">
                                <div>
                                    <h4 className="font-medium">Account Created</h4>
                                    <p className="text-sm text-gray-400">
                                        {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'Unknown'}
                                    </p>
                                </div>
                            </div>

                            <div className="flex items-center justify-between">
                                <div>
                                    <h4 className="font-medium">User ID</h4>
                                    <p className="text-sm text-gray-400 font-mono">
                                        {user?.id || 'Unknown'}
                                    </p>
                                </div>
                            </div>

                            <div className="pt-4 border-t border-gray-700">
                                <Button variant="outline" className="text-red-400 border-red-400 hover:bg-red-400/10">
                                    Delete Account
                                </Button>
                                <p className="mt-2 text-sm text-gray-400">
                                    This action cannot be undone. All your documents will be permanently deleted.
                                </p>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
