"use client";

import Link from "next/link";

export function Navigation() {
  return (
    <nav className="relative z-50 px-6 py-4" data-oid="pu70l68">
      <div
        className="mx-auto max-w-7xl flex items-center justify-between"
        data-oid=":io9cdy"
      >
        <div className="flex items-center space-x-2" data-oid="g03o:3r">
          <div
            className="w-8 h-8 bg-teal-500 rounded-lg flex items-center justify-center"
            data-oid="s:jpr2_"
          >
            <span className="text-white font-bold text-sm" data-oid="pdxy8k6">
              A
            </span>
          </div>
          <span className="text-white font-semibold text-xl" data-oid="v31d8p6">
            Aigency
          </span>
        </div>

        <div
          className="hidden md:flex items-center space-x-8"
          data-oid="_f854u2"
        >
          <Link
            href="#features"
            className="text-slate-300 hover:text-white transition-colors"
            data-oid=".2di6wu"
          >
            Features
          </Link>
          <Link
            href="#about"
            className="text-slate-300 hover:text-white transition-colors"
            data-oid="aj3__vf"
          >
            About
          </Link>
          <Link
            href="#pricing"
            className="text-slate-300 hover:text-white transition-colors"
            data-oid="-3jjil-"
          >
            Pricing
          </Link>
        </div>

        <button
          className="bg-teal-500 hover:bg-teal-600 text-white px-6 py-2 rounded-lg font-medium transition-colors"
          data-oid="nl18559"
        >
          Get Started
        </button>
      </div>
    </nav>
  );
}
