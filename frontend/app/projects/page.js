import { redirect } from "next/navigation";

// 旧暗色项目中心页 → 重定向到新 Terra 浅色项目中心
export default function ProjectsRedirect() {
  redirect("/ceo-office/projects");
}
