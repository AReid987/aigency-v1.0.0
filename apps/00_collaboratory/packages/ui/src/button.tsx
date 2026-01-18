'use client'

import * as React from 'react'
import { motion } from 'framer-motion'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'secondary' | 'outline' | 'ghost' | 'link'
  size?: 'default' | 'sm' | 'lg' | 'icon'
  loading?: boolean
  animate?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({
    className = '',
    variant = 'default',
    size = 'default',
    loading = false,
    animate = true,
    children,
    ...props
  }, ref) => {
    const baseClasses = 'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary disabled:pointer-events-none disabled:opacity-50'

    const variantClasses = {
      default: 'bg-primary text-white shadow hover:bg-primary/90',
      secondary: 'bg-secondary text-white shadow-sm hover:bg-secondary/90',
      outline: 'border border-gray-600 bg-transparent shadow-sm hover:bg-gray-800 hover:text-white',
      ghost: 'hover:bg-gray-800 hover:text-white',
      link: 'text-primary underline-offset-4 hover:underline',
    }

    const sizeClasses = {
      default: 'h-9 px-4 py-2',
      sm: 'h-8 rounded-md px-3 text-xs',
      lg: 'h-10 rounded-md px-8',
      icon: 'h-9 w-9',
    }

    const classes = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`

    const animationProps = animate ? {
      whileHover: { scale: 1.02 },
      whileTap: { scale: 0.98 },
      transition: { duration: 0.2 }
    } : {}

    return (
      <motion.button
        className={classes}
        ref={ref}
        disabled={loading || props.disabled}
        {...animationProps}
        {...props}
      >
        {loading && (
          <div className="mr-2">
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
          </div>
        )}
        {children}
      </motion.button>
    )
  }
)

Button.displayName = 'Button'

export { Button }
export type { ButtonProps }
