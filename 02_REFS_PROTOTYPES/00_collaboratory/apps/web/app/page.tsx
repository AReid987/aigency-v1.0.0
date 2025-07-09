'use client'

import React, { useState, useEffect } from 'react'
import Link from 'next/link'

interface Particle {
  id: number
  left: number
  top: number
  size: number
  animationDelay: number
  animationDuration: number
}

export default function Home() {
  return (
    <div className="h-screen w-full bg-black flex flex-col items-center justify-center overflow-hidden rounded-md">
      <h1 className="md:text-7xl text-3xl lg:text-9xl font-bold text-center text-white relative z-20">
        Aigency
      </h1>
      <div className="w-[40rem] h-40 relative">
        {/* Gradients */}
        <div className="absolute inset-x-20 top-0 bg-gradient-to-r from-transparent via-indigo-500 to-transparent h-[2px] w-3/4 blur-sm" />
        <div className="absolute inset-x-20 top-0 bg-gradient-to-r from-transparent via-indigo-500 to-transparent h-px w-3/4" />
        <div className="absolute inset-x-60 top-0 bg-gradient-to-r from-transparent via-sky-500 to-transparent h-[5px] w-1/4 blur-sm" />
        <div className="absolute inset-x-60 top-0 bg-gradient-to-r from-transparent via-sky-500 to-transparent h-px w-1/4" />

        {/* Core component */}
        <SparklesCore
          background="transparent"
          minSize={0.4}
          maxSize={1}
          particleDensity={1200}
          className="w-full h-full"
          particleColor="#FFFFFF"
        />

        {/* Radial Gradient to prevent sharp edges */}
        <div className="absolute inset-0 w-full h-full bg-black [mask-image:radial-gradient(350px_200px_at_top,transparent_20%,white)]"></div>
      </div>

      <p className="text-xl md:text-3xl font-light text-white mb-8">Collaboratory</p>

      <div className="flex justify-center gap-6 z-20">
        <Link
          href="/login"
          className="bg-white text-black px-8 py-3 rounded-lg hover:bg-gray-200 transition-colors font-medium"
        >
          Sign In
        </Link>
        <Link
          href="/signup"
          className="border border-white text-white px-8 py-3 rounded-lg hover:bg-white hover:text-black transition-colors font-medium"
        >
          Sign Up
        </Link>
      </div>
    </div>
  )
}

const SparklesCore = ({
  background,
  minSize,
  maxSize,
  particleDensity,
  className,
  particleColor,
}: {
  background: string
  minSize: number
  maxSize: number
  particleDensity: number
  className: string
  particleColor: string
}) => {
  const [particles, setParticles] = useState<Particle[]>([])
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    // Generate particles on client side to avoid hydration mismatch
    const generatedParticles: Particle[] = Array.from({ length: particleDensity }, (_, i) => ({
      id: i,
      left: Math.random() * 100,
      top: Math.random() * 100,
      size: Math.random() * (maxSize - minSize) + minSize,
      animationDelay: Math.random() * 3,
      animationDuration: Math.random() * 3 + 2,
    }))

    setParticles(generatedParticles)
    setMounted(true)
  }, [particleDensity, minSize, maxSize])

  if (!mounted) {
    return <div className={className} />
  }

  return (
    <div className={className}>
      <div className="absolute inset-0">
        {particles.map((particle) => (
          <div
            key={particle.id}
            className="absolute animate-pulse"
            style={{
              left: `${particle.left}%`,
              top: `${particle.top}%`,
              width: `${particle.size}px`,
              height: `${particle.size}px`,
              backgroundColor: particleColor,
              borderRadius: '50%',
              animationDelay: `${particle.animationDelay}s`,
              animationDuration: `${particle.animationDuration}s`,
            }}
          />
        ))}
      </div>
    </div>
  )
}
