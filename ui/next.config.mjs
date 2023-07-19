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
        destination: `http://${
          process.env.NEXT_PUBLIC_API_HOST ?? "api"
        }:8000/api/:slug*`,
      },
    ];
  },
  output: "standalone",
};

export default nextConfig;
