'use client';

import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Loader2 } from 'lucide-react';

const SignIn: React.FC = () => {
  const { loginWithRedirect, logout, isAuthenticated, isLoading, user } = useAuth0();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#141313] flex flex-col items-center justify-center p-4">
        <Loader2 className="h-8 w-8 animate-spin text-white" />
        <p className="text-white mt-2">Loading authentication...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#141313] flex flex-col items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md p-8 space-y-6 bg-[#1F1F1F] rounded-2xl shadow-lg text-white"
      >
        <div className="text-center">
          <motion.h1
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className="text-4xl font-bold text-white"
          >
            Aigency
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.5 }}
            className="mt-2 text-[#E7E9EF]"
          >
            {isAuthenticated ? 'Welcome back!' : 'Sign in to your account'}
          </motion.p>
        </div>

        {isAuthenticated ? (
          <div className="space-y-4">
            <p>Hello, {user?.name || user?.nickname || user?.email}!</p>
            <Button
              onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}
              className="w-full py-3 font-semibold text-white bg-[#615EFF] rounded-lg hover:bg-[#4E4AFF] transition-colors duration-300"
            >
              Log Out
            </Button>
          </div>
        ) : (
          <Button
            onClick={() => loginWithRedirect()}
            className="w-full py-3 font-semibold text-white bg-[#615EFF] rounded-lg hover:bg-[#4E4AFF] transition-colors duration-300"
          >
            Log In
          </Button>
        )}
      </motion.div>
    </div>
  );
};

export default SignIn;