import { redirect } from "next/navigation";

// 旧暗色能力中心页 → 重定向到新 Terra 浅色能力中心
export default function CapabilitiesRedirect() {
  redirect("/ceo-office/capabilities");
}
