/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://api:8000/:path*',
      },
    ]
  },
  // Increase timeout for API calls
  experimental: {
    serverComponentsExternalPackages: [],
  },
  // Configure server timeout
  serverRuntimeConfig: {
    maxDuration: 300, // 5 minutes
  },
}

export default nextConfig
