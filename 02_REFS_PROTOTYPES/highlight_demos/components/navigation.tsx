"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";

export default function Navigation() {
  const pathname = usePathname();

  const navItems = [
    { href: "/", label: "Dashboard", icon: "🏠" },
    { href: "/network", label: "Network Graph", icon: "🌐" },
    { href: "/knowledge-graph", label: "3D Knowledge Graph", icon: "🔮" },
    { href: "/agents", label: "AI Agents", icon: "🤖" },
  ];

  return (
    <nav className='bg-white dark:bg-gray-800 shadow-sm border-b'>
      <div className='max-w-7xl mx-auto px-8 py-4'>
        <div className='flex items-center justify-between'>
          <div className='flex items-center space-x-8'>
            <Link
              href='/'
              className='text-xl font-bold text-gray-900 dark:text-white'
            >
              AI Agent Hub
            </Link>

            <div className='flex space-x-4'>
              {navItems.map((item) => (
                <Link key={item.href} href={item.href}>
                  <Button
                    variant={pathname === item.href ? "default" : "ghost"}
                    className='flex items-center gap-2'
                  >
                    <span>{item.icon}</span>
                    {item.label}
                  </Button>
                </Link>
              ))}
            </div>
          </div>

          <div className='text-sm text-gray-600 dark:text-gray-300'>
            AI Agent Network Visualization
          </div>
        </div>
      </div>
    </nav>
  );
}
