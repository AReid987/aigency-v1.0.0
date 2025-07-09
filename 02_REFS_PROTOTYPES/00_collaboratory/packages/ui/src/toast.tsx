'use client'

import * as React from 'react'
import * as ToastPrimitive from '@radix-ui/react-toast'

interface ToastProps {
    title?: string
    description?: string
    action?: React.ReactNode
    variant?: 'default' | 'success' | 'error' | 'warning'
    duration?: number
    className?: string
}

const ToastProvider = ToastPrimitive.Provider
const ToastViewport = React.forwardRef<
    React.ElementRef<typeof ToastPrimitive.Viewport>,
    React.ComponentPropsWithoutRef<typeof ToastPrimitive.Viewport>
>(({ className = '', ...props }, ref) => (
    <ToastPrimitive.Viewport
        ref={ref}
        className={`fixed bottom-0 right-0 z-50 flex max-h-screen w-full flex-col-reverse p-4 sm:bottom-0 sm:right-0 sm:top-auto sm:flex-col md:max-w-[420px] ${className}`}
        {...props}
    />
))
ToastViewport.displayName = ToastPrimitive.Viewport.displayName

const Toast = React.forwardRef<
    React.ElementRef<typeof ToastPrimitive.Root>,
    ToastProps
>(({ title, description, action, variant = 'default', duration = 3000, className = '' }, ref) => {
    const variantStyles = {
        default: 'bg-gray-800 border-gray-700',
        success: 'bg-green-900 border-green-800',
        error: 'bg-red-900 border-red-800',
        warning: 'bg-yellow-900 border-yellow-800'
    }

    return (
        <ToastPrimitive.Root
            ref={ref}
            duration={duration}
            className={`group pointer-events-auto relative flex w-full items-center justify-between space-x-4 overflow-hidden rounded-md border p-6 pr-8 shadow-lg transition-all ${variantStyles[variant]} ${className}`}
        >
            <div className="flex flex-col gap-1">
                {title && (
                    <ToastPrimitive.Title className="text-sm font-semibold">
                        {title}
                    </ToastPrimitive.Title>
                )}
                {description && (
                    <ToastPrimitive.Description className="text-sm opacity-90">
                        {description}
                    </ToastPrimitive.Description>
                )}
            </div>
            {action && (
                <div className="flex shrink-0 items-center">
                    {action}
                </div>
            )}
            <ToastPrimitive.Close className="absolute right-2 top-2 rounded-md p-1 opacity-0 transition-opacity hover:opacity-100 focus:opacity-100 group-hover:opacity-100">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                >
                    <line x1="18" y1="6" x2="6" y2="18" />
                    <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
            </ToastPrimitive.Close>
        </ToastPrimitive.Root>
    )
})
Toast.displayName = 'Toast'

export { Toast, ToastProvider, ToastViewport }
export type { ToastProps }
