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
        destination: "http://api:8000/api/:slug*",
      },
    ];
  },
  output: "standalone",
};

export default nextConfig;
