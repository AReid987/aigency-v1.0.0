'use client'

import * as React from 'react'
import * as AvatarPrimitive from '@radix-ui/react-avatar'

interface AvatarProps {
    src?: string
    alt?: string
    fallback?: string
    size?: 'sm' | 'md' | 'lg'
    className?: string
}

const Avatar = React.forwardRef<HTMLDivElement, AvatarProps>(
    ({ src, alt = '', fallback, size = 'md', className = '' }, ref) => {
        const sizeClasses = {
            sm: 'h-8 w-8',
            md: 'h-10 w-10',
            lg: 'h-12 w-12'
        }

        return (
            <AvatarPrimitive.Root
                ref={ref}
                className={`relative flex shrink-0 overflow-hidden rounded-full ${sizeClasses[size]} ${className}`}
            >
                <AvatarPrimitive.Image
                    src={src}
                    alt={alt}
                    className="h-full w-full object-cover"
                />
                <AvatarPrimitive.Fallback
                    className="flex h-full w-full items-center justify-center rounded-full bg-gray-800 text-gray-400"
                >
                    {fallback || alt?.charAt(0).toUpperCase()}
                </AvatarPrimitive.Fallback>
            </AvatarPrimitive.Root>
        )
    }
)

Avatar.displayName = 'Avatar'

export { Avatar }
export type { AvatarProps }
