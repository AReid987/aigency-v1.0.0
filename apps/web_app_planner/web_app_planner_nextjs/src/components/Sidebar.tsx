"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navigation = [
  { name: "Branding", href: "/branding" },
  { name: "Goals & Objectives", href: "/goals" },
  { name: "User Stories", href: "/user-stories" },
  { name: "Core Features", href: "/core-features" },
  { name: "Wireframes/Mockups", href: "/wireframes-mockups" },
  { name: "Atomic Design System", href: "/atomic-design-system" },
  { name: "Data Points", href: "/data-points" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <div className='flex flex-col w-64 bg-gray-800 text-white p-4'>
      <div className='text-2xl font-bold mb-6'>WebApp Planner</div>
      <nav>
        {navigation.map((item) => (
          <Link
            key={item.name}
            href={item.href}
            className={`block py-2 px-4 rounded-md ${
              pathname === item.href ? "bg-gray-700" : "hover:bg-gray-700"
            }`}
          >
            {item.name}
          </Link>
        ))}
      </nav>
    </div>
  );
}
