const nextConfig = {
  // Desktop packaging uses the self-contained standalone server. Development
  // still uses `next dev`; the bundle is produced explicitly by the Desktop
  // packaging script with the Trusted Gateway API base.
  output: "standalone",
  env: {
    // v1 自用（selfuse）默认直连 8000 后端；Docker gateway 模式可通过
    // NEXT_PUBLIC_API_BASE=/gateway 覆盖（构建时内嵌）。
    NEXT_PUBLIC_API_BASE: process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000",
    // 本地 Owner 模式下前后端 CEO_ID 必须一致；默认 selfuse-ceo 仅用于直连 8000 场景。
    NEXT_PUBLIC_CEO_ID: process.env.NEXT_PUBLIC_CEO_ID || "selfuse-ceo",
  },
  turbopack: {
    root: __dirname,
  },
  async redirects() {
    return [
      { source: "/", destination: "/welcome", permanent: false },
    ];
  },
  async rewrites() {
    return [
      {
        source: "/gateway/:path*",
        destination: process.env.CURIS_GATEWAY_TARGET || "http://127.0.0.1:8080/:path*",
      },
    ];
  },
};

module.exports = nextConfig;
