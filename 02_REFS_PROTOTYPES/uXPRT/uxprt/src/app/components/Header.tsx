import React from "react";
import Link from "next/link";
import Image from "next/image";

interface HeaderProps {
  onLoginClick: () => void;
}

const Header: React.FC<HeaderProps> = ({ onLoginClick }) => {
  return (
    <header className='fixed top-4 left-1/2 -translate-x-1/2 w-[calc(100%-2rem)] max-w-screen-lg z-50'>
      <div
        className='container mx-auto flex justify-between items-center
                      bg-card/70 text-card-foreground p-3 shadow-lg rounded-full
                      backdrop-blur-md border border-border/30'
      >
        <div className='flex items-center gap-2'>
          <Link href='/' className='flex items-center'>
            <Image
              src='/xprt-atom-logo-neg.svg'
              alt='XPRT Logo'
              width={28} // Smaller logo
              height={28}
              className='mr-2'
            />
            <span className='text-xl font-bold hover:text-card-foreground/90'>
              XPRT
            </span>
          </Link>
        </div>
        <nav>
          <button
            onClick={onLoginClick}
            className='bg-primary hover:bg-primary/90 text-primary-foreground px-5 py-2.5 rounded-full text-sm font-semibold shadow-md hover:shadow-lg transition-all'
          >
            Login
          </button>
        </nav>
      </div>
    </header>
  );
};

export default Header;
