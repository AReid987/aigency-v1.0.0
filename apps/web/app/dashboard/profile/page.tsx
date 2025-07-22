
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
// import { createClientComponentClient } from '@supabase/ssr';
import { ProfileForm } from '@/components/profile-form';

const ProfilePage = () => {
  const router = useRouter();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  // const supabase = createClientComponentClient();

  useEffect(() => {
    const fetchProfile = async () => {
      // const { data: { session } } = await supabase.auth.getSession();
    const session = { access_token: "" }; // Placeholder

      if (!session) {
        router.push('/sign-in'); // Redirect to login if not signed in
        return;
      }

      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`http://localhost:8000/api/user/profile`, {
          headers: {
            'Authorization': `Bearer ${session.access_token}`,
          },
        });
        if (!response.ok) {
          throw new Error('Failed to fetch profile');
        }
        const data = await response.json();
        setProfile(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [router]);

  if (loading) return <div className="text-white">Loading profile...</div>;
  if (error) return <div className="text-red-500">Error: {error}</div>;
  if (!profile) return <div className="text-white">No profile found.</div>;

  return (
    <div className="min-h-screen bg-[#141313] flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md p-8 space-y-6 bg-[#1F1F1F] rounded-2xl shadow-lg text-white">
        <h1 className="text-3xl font-bold text-center">User Profile</h1>
        <ProfileForm initialData={profile} />
      </div>
    </div>
  );
};

export default ProfilePage;
