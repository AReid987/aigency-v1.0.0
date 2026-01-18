/** @type {import('tailwindcss').Config} */
const { withRadixTheme } = require('radix-themes-tw')

module.exports = withRadixTheme({
    content: [
        './app/**/*.{js,ts,jsx,tsx,mdx}',
        './components/**/*.{js,ts,jsx,tsx,mdx}',
    ],
    theme: {
        extend: {
            colors: {
                primary: '#5A4FCF', // Radix UI iris 9
                'primary-dark': '#1A103F',
                'primary-light': '#7B6FEF',
                dark: {
                    DEFAULT: '#0A0A0B',
                    100: '#121214',
                    200: '#1A1A1F',
                }
            },
            backgroundImage: {
                'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
                'gradient-dark': 'linear-gradient(to bottom right, #0A0A0B, #1A103F)',
            },
            boxShadow: {
                'glow': '0 0 20px rgba(90, 79, 207, 0.2)',
                'glow-lg': '0 0 30px rgba(90, 79, 207, 0.3)',
            },
            backdropBlur: {
                'xs': '2px',
            }
        },
    },
    plugins: [],
})
