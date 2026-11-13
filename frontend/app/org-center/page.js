import { redirect } from "next/navigation";

// 旧暗色组织中心页 → 重定向到新 Terra 浅色组织中心
export default function OrgCenterRedirect() {
  redirect("/ceo-office/organization");
}
