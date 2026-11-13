import { GlobalAssistantProvider } from "../components/assistant/GlobalAssistant.js";
import { RuntimeProvider } from "../components/runtime/RuntimeProvider.js";
import DevMode from "../components/terra/DevMode.js";
import "./globals.css";

export const metadata = {
  title: "Curis CEO Office",
  description: "Curis AI 公司操作系统 · 总裁办公室",
};

export const viewport = {
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({ children }) {
  return (
    <html lang="zh-CN" data-theme="system" suppressHydrationWarning>
      <body className="font-ui-sans">
        <script
          dangerouslySetInnerHTML={{
            __html: "try{document.documentElement.dataset.theme=localStorage.getItem('curis.theme')||'system'}catch(_error){}",
          }}
        />
        <RuntimeProvider>
          <GlobalAssistantProvider>{children}</GlobalAssistantProvider>
        </RuntimeProvider>
        {/* Frozen 令牌合规标注层：未开启时返回 null，零运行时成本 */}
        <DevMode />
      </body>
    </html>
  );
}
