'use client'

import * as React from 'react'
import * as TabsPrimitive from '@radix-ui/react-tabs'

interface TabsProps {
    defaultValue?: string
    value?: string
    onValueChange?: (value: string) => void
    className?: string
    children: React.ReactNode
}

const Tabs = React.forwardRef<HTMLDivElement, TabsProps>(
    ({ defaultValue, value, onValueChange, className = '', children }, ref) => {
        return (
            <TabsPrimitive.Root
                ref={ref}
                defaultValue={defaultValue}
                value={value}
                onValueChange={onValueChange}
                className={className}
            >
                {children}
            </TabsPrimitive.Root>
        )
    }
)

Tabs.displayName = 'Tabs'

const TabsList = React.forwardRef<
    HTMLDivElement,
    React.ComponentProps<typeof TabsPrimitive.List>
>(({ className = '', ...props }, ref) => (
    <TabsPrimitive.List
        ref={ref}
        className={`inline-flex h-10 items-center justify-center rounded-lg bg-gray-800/50 p-1 ${className}`}
        {...props}
    />
))

TabsList.displayName = 'TabsList'

const TabsTrigger = React.forwardRef<
    HTMLButtonElement,
    React.ComponentProps<typeof TabsPrimitive.Trigger>
>(({ className = '', ...props }, ref) => (
    <TabsPrimitive.Trigger
        ref={ref}
        className={`inline-flex items-center justify-center whitespace-nowrap rounded-md px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-gray-700 data-[state=active]:text-white data-[state=active]:shadow-sm ${className}`}
        {...props}
    />
))

TabsTrigger.displayName = 'TabsTrigger'

const TabsContent = React.forwardRef<
    HTMLDivElement,
    React.ComponentProps<typeof TabsPrimitive.Content>
>(({ className = '', ...props }, ref) => (
    <TabsPrimitive.Content
        ref={ref}
        className={`mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 ${className}`}
        {...props}
    />
))

TabsContent.displayName = 'TabsContent'

export { Tabs, TabsList, TabsTrigger, TabsContent }
export type { TabsProps }
