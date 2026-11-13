import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import type { ProxyOptions } from 'vite'

// 自动为所有 /api/* 代理请求注入 X-Tenant-Id: selfuse 头，
// 配合后端 CURIS_IDENTITY_MODE=selfuse 模式实现自用场景的免登录鉴权。
const apiProxy: ProxyOptions = {
  target: 'http://localhost:8000',
  changeOrigin: true,
  configure(proxy) {
    proxy.on('proxyReq', (proxyReq) => {
      proxyReq.setHeader('X-Tenant-Id', 'selfuse')
    })
  },
}

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': apiProxy,
    },
  },
})
