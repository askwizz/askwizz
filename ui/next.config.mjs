/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    appDir: true,
  },
  async rewrites() {
    return [
      {
        source: "/api/:slug*",
        destination: "http://localhost:8000/api/:slug*",
      },
    ];
  },
};

export default nextConfig;
