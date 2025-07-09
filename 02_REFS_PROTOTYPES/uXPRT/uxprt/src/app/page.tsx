"use client";

import { useState, Suspense, useEffect } from "react";
import dynamic from "next/dynamic";
import SignupForm from "./components/SignupForm"; // Assuming SignupForm is in components
import LoginForm from "./components/LoginForm"; // Import LoginForm
import { Button } from "@/components/ui/button";
import Image from "next/image";

// Dynamically import DiamondModel to ensure it's client-side only
const DiamondModel = dynamic(() => import("./components/DiamondModel"), {
  ssr: false,
  loading: () => (
    <div className='w-full h-full flex items-center justify-center absolute inset-0 z-0'>
      <div className='loader'></div>
    </div>
  ),
});

export default function Home() {
  const [showSignupOverlay, setShowSignupOverlay] = useState(false);
  // const [showLoginOverlay, setShowLoginOverlay] = useState(false); // State for login overlay is now in layout.tsx
  const [animateHeader, setAnimateHeader] = useState(false);
  const [animateSubHeader, setAnimateSubHeader] = useState(false);
  const [animateSecondSubHeader, setAnimateSecondSubHeader] = useState(false);
  const [animateBodyText, setAnimateBodyText] = useState(false);
  const [animateButtons, setAnimateButtons] = useState(false);

  const toggleSignupOverlay = () => {
    setShowSignupOverlay(!showSignupOverlay);
  };

  // const toggleLoginOverlay = () => {
  //   // Toggle function for login overlay is now in layout.tsx
  //   setShowLoginOverlay(!showLoginOverlay);
  // };

  useEffect(() => {
    const timers: NodeJS.Timeout[] = [];
    timers.push(setTimeout(() => setAnimateHeader(true), 0));
    timers.push(setTimeout(() => setAnimateSubHeader(true), 300));
    timers.push(setTimeout(() => setAnimateSecondSubHeader(true), 600));
    timers.push(setTimeout(() => setAnimateBodyText(true), 900));
    timers.push(setTimeout(() => setAnimateButtons(true), 1200));
    return () => timers.forEach(clearTimeout); // Cleanup timers
  }, []);

  return (
    <main className='min-h-screen flex flex-col relative overflow-hidden'>
      {/* Login overlay toggle is handled by Header via RootLayout */}
      {/* Top Section: Title and Subtitle - positioned above the Diamond */}
      <div className='relative z-10 w-full pt-24 pb-4 text-center'>
        {" "}
        {/* Increased pt-16 to pt-24 for more space */}{" "}
        {/* Further reduced pt and pb */}
        <h1
          className={`text-8xl font-bold tracking-tight sm:text-9xl drop-shadow-lg glowing-gradient-text ${
            animateHeader ? "start-animation" : ""
          }`}
          data-text='XPRT' // Added for pseudo-element content
        >
          XPRT
        </h1>
        <p
          className={`mt-2 text-3xl leading-8 sm:text-4xl drop-shadow-md animate-on-load ${
            animateSubHeader ? "start-animation" : ""
          }`}
          style={{ color: "#ABF0D7" }}
        >
          Knowledge OS
        </p>
      </div>

      {/* Diamond Model - takes up significant vertical space in the middle */}
      {/* Adjusted height and removed vertical margin to pull it up */}
      <div className='relative w-full h-[30vh] sm:h-[35vh] md:h-[40vh] z-0 flex items-center justify-center'>
        <Suspense
          fallback={
            <div className='w-full h-full flex items-center justify-center'>
              <div className='loader'></div>
            </div>
          }
        >
          <DiamondModel />
        </Suspense>
      </div>

      {/* Bottom Section: New Subheading, UVP, and Buttons - positioned below the Diamond */}
      {/* Removed top padding to bring it closer to the diamond, reduced bottom padding */}
      <div className='relative z-10 w-full flex flex-col items-center text-center pb-12 pt-2'>
        <h2
          className={`text-2xl sm:text-3xl font-semibold mb-4 drop-shadow-md animate-on-load ${
            animateSecondSubHeader ? "start-animation" : ""
          }`}
          style={{ color: "#ABF0D7" }}
        >
          <span className='font-extrabold text-primary'>Intel</span>ligent{" "}
          <span className='font-extrabold text-primary'>Op</span>eration
          <span className='font-extrabold text-primary'>s</span>
        </h2>
        <div
          className={`animate-on-load ${
            animateBodyText ? "start-animation" : ""
          }`}
        >
          <p
            className='text-xl leading-relaxed sm:text-2xl drop-shadow-md'
            style={{ color: "#ABF0D7" }}
          >
            <span className='font-bold text-primary'>100x</span> Yourself with
            the <span className='font-bold text-primary'>XPRT</span> Agent Squad
          </p>
          <p
            className='mt-1 text-xl leading-relaxed sm:text-2xl drop-shadow-md max-w-3xl'
            style={{ color: "#ABF0D7" }}
          >
            Next Level{" "}
            <span className='font-bold text-primary'>Product Development</span>{" "}
            & <span className='font-bold text-primary'>Content Creation</span>{" "}
            at Warp Speed
          </p>
        </div>
        <div
          className={`mt-10 flex items-center justify-center gap-x-6 animate-on-load ${
            animateButtons ? "start-animation" : ""
          }`}
        >
          <Button
            onClick={toggleSignupOverlay}
            size='lg'
            className='bg-primary hover:bg-primary/90 text-primary-foreground font-semibold py-3 px-8 text-lg shadow-lg hover:shadow-xl transition-all'
          >
            Get Started
          </Button>
          <a
            href='#'
            className='text-sm font-semibold leading-6 hover:text-white'
            style={{ color: "#ABF0D7" }}
          >
            Learn more <span aria-hidden='true'>→</span>
          </a>
        </div>
      </div>
      {/* Signup Form Overlay */}
      {showSignupOverlay && (
        <div className='fixed inset-0 z-20 flex items-center justify-center bg-black/30 backdrop-blur-sm p-4'>
          <div className='relative bg-card/80 backdrop-blur-lg text-card-foreground p-8 rounded-xl shadow-2xl w-full max-w-md border border-border/50'>
            {/* Close button for the overlay (optional, as SignupForm has "Go back") */}
            <Button
              variant='ghost'
              size='sm'
              onClick={toggleSignupOverlay}
              className='absolute top-2 right-2 text-muted-foreground hover:text-foreground'
            >
              ✕ {/* Simple X, or use an icon */}
            </Button>
            <SignupForm onGoBack={toggleSignupOverlay} />
          </div>
        </div>
      )}

      {/* Login Form Overlay is now rendered in layout.tsx */}
    </main>
  );
}
