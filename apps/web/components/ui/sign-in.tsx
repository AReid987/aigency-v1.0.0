
'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Mail, Lock, Eye, EyeOff, ArrowRight, Loader2 } from 'lucide-react';
import { useRouter } from 'next/navigation';

const SignIn = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isSignUp, setIsSignUp] = useState(false);
  const [message, setMessage] = useState('');
  const [emailError, setEmailError] = useState<string | null>(null);
  const [passwordError, setPasswordError] = useState<string | null>(null);
  const router = useRouter();

  const validateForm = (email: string, password: string) => {
    let isValid = true;
    setEmailError(null);
    setPasswordError(null);

    if (!email) {
      setEmailError('Email is required.');
      isValid = false;
    } else if (!/^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/g.test(email)) {
      setEmailError('Invalid email format.');
      isValid = false;
    }

    if (!password) {
      setPasswordError('Password is required.');
      isValid = false;
    } else if (password.length < 6) {
      setPasswordError('Password must be at least 6 characters long.');
      isValid = false;
    }
    // Add more password strength checks here if needed (e.g., regex for special chars, numbers)

    return isValid;
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setMessage('');

    const formData = new FormData(event.currentTarget);
    const email = formData.get('email') as string;
    const password = formData.get('password') as string;

    if (!validateForm(email, password)) {
      return; // Stop submission if client-side validation fails
    }

    setIsLoading(true);
    const endpoint = isSignUp ? '/register' : '/login';

    try {
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        if (isSignUp) {
          setMessage('Registration successful! Please check your email for a confirmation link.');
        } else {
          setMessage('Login successful! Redirecting to dashboard...');
          setTimeout(() => {
            router.push('/dashboard');
          }, 2000);
        }
      } else {
        // Server-side validation errors
        setMessage(data.detail || 'An error occurred.');
        if (data.detail) {
          if (data.detail.includes('email')) {
            setEmailError(data.detail);
          }
          if (data.detail.includes('password')) {
            setPasswordError(data.detail);
          }
        }
      }
    } catch (error) {
      setMessage('An unexpected error occurred. Please try again later.');
    }

    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-[#141313] flex flex-col items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md p-8 space-y-6 bg-[#1F1F1F] rounded-2xl shadow-lg"
      >
        <div className="text-center">
          <motion.h1
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className="text-4xl font-bold text-white"
          >
            {isSignUp ? 'Create Account' : 'Aigency'}
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.5 }}
            className="mt-2 text-[#E7E9EF]"
          >
            {isSignUp ? 'Get started with your new account.' : 'Sign in to your account'}
          </motion.p>
        </div>

        {message && <p className="text-center text-white">{message}</p>}

        <motion.form
          onSubmit={handleSubmit}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6, duration: 0.5 }}
          className="space-y-6"
        >
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-[#E7E9EF]" />
            <input
              name="email"
              type="email"
              placeholder="Email"
              onChange={() => setEmailError(null)}
              className={`w-full pl-10 pr-4 py-2 text-white bg-[#1F1F1F] border rounded-lg focus:outline-none focus:ring-2 ${emailError ? 'border-red-500 focus:ring-red-500' : 'border-gray-600 focus:ring-[#615EFF]'}`}
            />
            {emailError && <p className="text-red-500 text-xs mt-1">{emailError}</p>}
          </div>

          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-[#E7E9EF]" />
            <input
              name="password"
              type={showPassword ? 'text' : 'password'}
              placeholder="Password"
              onChange={() => setPasswordError(null)}
              className={`w-full pl-10 pr-10 py-2 text-white bg-[#1F1F1F] border rounded-lg focus:outline-none focus:ring-2 ${passwordError ? 'border-red-500 focus:ring-red-500' : 'border-gray-600 focus:ring-[#615EFF]'}`}
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-[#E7E9EF] hover:text-white"
            >
              {showPassword ? <EyeOff /> : <Eye />}
            </button>
            {passwordError && <p className="text-red-500 text-xs mt-1">{passwordError}</p>}
          </div>

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
                {isSignUp ? 'Signing up...' : 'Signing in...'}
              </>
            ) : (
              <>
                {isSignUp ? 'Sign Up' : 'Sign In'} <ArrowRight className="ml-2" />
              </>
            )}
          </motion.button>
        </motion.form>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7, duration: 0.5 }}
          className="text-center"
        >
          <a href="#" onClick={() => setIsSignUp(!isSignUp)} className="text-sm text-[#615EFF] hover:underline">
            {isSignUp ? 'Already have an account? Sign in' : 'Don\'t have an account? Sign up'}
          </a>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default SignIn;
