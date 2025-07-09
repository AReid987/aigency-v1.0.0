'use client'

import * as React from 'react'
import * as DialogPrimitive from '@radix-ui/react-dialog'

const Dialog = DialogPrimitive.Root
const DialogTrigger = DialogPrimitive.Trigger
const DialogClose = DialogPrimitive.Close

const DialogContent = ({
    children,
    className = '',
    ...props
}: DialogPrimitive.DialogContentProps) => (
    <DialogPrimitive.Portal>
        <DialogPrimitive.Overlay className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm" />
        <DialogPrimitive.Content
            className={`fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border border-gray-700 bg-gray-900 p-6 shadow-lg duration-200 rounded-lg ${className}`}
            {...props}
        >
            {children}
            <DialogClose className="absolute right-4 top-4 rounded-sm opacity-70 hover:opacity-100">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="h-4 w-4"
                >
                    <line x1="18" y1="6" x2="6" y2="18" />
                    <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
                <span className="sr-only">Close</span>
            </DialogClose>
        </DialogPrimitive.Content>
    </DialogPrimitive.Portal>
)

const DialogHeader = ({
    className = '',
    ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
    <div
        className={`flex flex-col space-y-1.5 text-center sm:text-left ${className}`}
        {...props}
    />
)

const DialogTitle = ({
    className = '',
    ...props
}: DialogPrimitive.DialogTitleProps) => (
    <DialogPrimitive.Title
        className={`text-lg font-semibold leading-none tracking-tight ${className}`}
        {...props}
    />
)

const DialogDescription = ({
    className = '',
    ...props
}: DialogPrimitive.DialogDescriptionProps) => (
    <DialogPrimitive.Description
        className={`text-sm text-gray-400 ${className}`}
        {...props}
    />
)

export {
    Dialog,
    DialogTrigger,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
    DialogClose,
}
