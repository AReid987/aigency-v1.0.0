"use client";

import Link from "next/link";

export function Navigation() {
  return (
    <nav className="relative z-50 px-6 py-4" data-oid="cmik2:e">
      <div
        className="mx-auto max-w-7xl flex items-center justify-between"
        data-oid="d:ew9iq"
      >
        <div className="flex items-center space-x-2" data-oid="1ai4how">
          <div
            className="w-8 h-8 bg-teal-500 rounded-lg flex items-center justify-center"
            data-oid="47xf5z0"
          >
            <span className="text-white font-bold text-sm" data-oid="_4a_:hd">
              A
            </span>
          </div>
          <span className="text-white font-semibold text-xl" data-oid="2wl_nc3">
            Aigency
          </span>
        </div>

        <div
          className="hidden md:flex items-center space-x-8"
          data-oid="pvqe848"
        >
          <Link
            href="#features"
            className="text-slate-300 hover:text-white transition-colors"
            data-oid="cpqvne7"
          >
            Features
          </Link>
          <Link
            href="#about"
            className="text-slate-300 hover:text-white transition-colors"
            data-oid="av5vqbd"
          >
            About
          </Link>
          <Link
            href="#pricing"
            className="text-slate-300 hover:text-white transition-colors"
            data-oid="q3u-h1w"
          >
            Pricing
          </Link>
        </div>

        <button
          className="bg-teal-500 hover:bg-teal-600 text-white px-6 py-2 rounded-lg font-medium transition-colors"
          data-oid="5z8al4m"
        >
          Get Started
        </button>
      </div>
    </nav>
  );
}
