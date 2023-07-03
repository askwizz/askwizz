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
        destination: `${process.env.API_BASE_URL}/api/:slug*`,
      },
    ];
  },
  output: "standalone",
};

export default nextConfig;
