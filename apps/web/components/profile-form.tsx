
'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Loader2 } from 'lucide-react';
// import { createClientComponentClient } from '@supabase/ssr';

export const ProfileForm = ({ initialData }: { initialData: any }) => {
  const [username, setUsername] = useState(initialData.username || '');
  const [fullName, setFullName] = useState(initialData.full_name || '');
  const [avatarUrl, setAvatarUrl] = useState(initialData.avatar_url || '');
  const [bio, setBio] = useState(initialData.bio || '');
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  // const supabase = createClientComponentClient();

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsLoading(true);
    setMessage('');
    setError('');

    try {
      // const { data: { session } } = await supabase.auth.getSession();
      const session = { access_token: "" }; // Placeholder
      if (!session) {
        setError('User not authenticated.');
        setIsLoading(false);
        return;
      }

      const response = await fetch(`http://localhost:8000/api/user/profile`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.access_token}`,
        },
        body: JSON.stringify({
          username,
          full_name: fullName,
          avatar_url: avatarUrl,
          bio,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage('Profile updated successfully!');
      } else {
        setError(data.detail || 'Failed to update profile.');
      }
    } catch (err) {
      setError('An unexpected error occurred.');
    }

    setIsLoading(false);
  };

  return (
    <motion.form
      onSubmit={handleSubmit}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="space-y-4"
    >
      <div>
        <label htmlFor="username" className="block text-sm font-medium text-gray-300">Username</label>
        <input
          type="text"
          id="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="mt-1 block w-full px-3 py-2 bg-[#1F1F1F] border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-[#615EFF]"
        />
      </div>
      <div>
        <label htmlFor="fullName" className="block text-sm font-medium text-gray-300">Full Name</label>
        <input
          type="text"
          id="fullName"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          className="mt-1 block w-full px-3 py-2 bg-[#1F1F1F] border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-[#615EFF]"
        />
      </div>
      <div>
        <label htmlFor="avatarUrl" className="block text-sm font-medium text-gray-300">Avatar URL</label>
        <input
          type="text"
          id="avatarUrl"
          value={avatarUrl}
          onChange={(e) => setAvatarUrl(e.target.value)}
          className="mt-1 block w-full px-3 py-2 bg-[#1F1F1F] border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-[#615EFF]"
        />
      </div>
      <div>
        <label htmlFor="bio" className="block text-sm font-medium text-gray-300">Bio</label>
        <textarea
          id="bio"
          value={bio}
          onChange={(e) => setBio(e.target.value)}
          rows={3}
          className="mt-1 block w-full px-3 py-2 bg-[#1F1F1F] border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-[#615EFF]"
        ></textarea>
      </div>

      {message && <p className="text-green-500 text-center">{message}</p>}
      {error && <p className="text-red-500 text-center">{error}</p>}

      <motion.button
        type="submit"
        disabled={isLoading}
        whileHover={{ scale: isLoading ? 1 : 1.05 }}
        whileTap={{ scale: isLoading ? 1 : 0.95 }}
        className="w-full py-3 font-semibold text-white bg-[#615EFF] rounded-lg hover:bg-[#4E4AFF] transition-colors duration-300 flex items-center justify-center disabled:opacity-50"
      >
        {isLoading ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            Updating...
          </>
        ) : (
          'Update Profile'
        )}
      </motion.button>
    </motion.form>
  );
};
