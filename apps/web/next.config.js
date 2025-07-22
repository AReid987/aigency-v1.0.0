/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config, { isServer }) => {
    // Important: return the modified config
    return config;
  },
  experimental: {
    appDir: true,
  },
  
};

export default nextConfig;
