"use client";

import { useState } from "react";
import Image from "next/image";
import LoginForm from "../components/LoginForm";
import SignupForm from "../components/SignupForm";
import { Button } from "@/components/ui/button"; // Keep for potential social buttons

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);

  const toggleForm = () => setIsLogin(!isLogin);

  return (
    <div className='min-h-screen flex flex-col items-center justify-center bg-background text-foreground p-4'>
      <div className='w-full max-w-md space-y-8'>
        <div className='text-center'>
          <Image
            src='/xprt-atom-logo-neg.svg'
            alt='XPRT Logo'
            width={80}
            height={80}
            className='mx-auto mb-6'
          />
          <h1 className='text-3xl font-bold text-foreground mb-3'>
            {isLogin ? "Sign in to your account" : "Create an account"}
          </h1>
        </div>

        {/* Placeholder for Social Sign-up Buttons */}
        <div className='space-y-4'>
          <Button
            variant='outline'
            className='w-full bg-card hover:bg-card/90 text-card-foreground'
          >
            Sign in with Google (Placeholder)
          </Button>
          <Button
            variant='outline'
            className='w-full bg-card hover:bg-card/90 text-card-foreground'
          >
            Sign in with GitHub (Placeholder)
          </Button>
        </div>

        {/* OR Separator */}
        <div className='flex items-center my-6'>
          <hr className='flex-grow border-border' />
          <span className='mx-4 text-muted-foreground'>OR</span>
          <hr className='flex-grow border-border' />
        </div>

        {isLogin ? <LoginForm /> : <SignupForm onGoBack={toggleForm} />}

        <div className='text-center mt-6'>
          <button
            onClick={toggleForm}
            className='text-sm text-primary hover:underline'
          >
            {isLogin
              ? "Don't have an account? Create one."
              : "Already have an account? Sign in."}
          </button>
        </div>
      </div>
    </div>
  );
}
