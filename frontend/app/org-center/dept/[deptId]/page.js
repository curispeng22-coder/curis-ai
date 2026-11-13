import { redirect } from "next/navigation";

// 旧暗色「部门详情」深链 → 重定向到新 Terra 浅色组织中心（部门详情统一收敛 /ceo-office/organization/departments/[id]）
export default function OrgCenterDeptRedirect() {
  redirect("/ceo-office/organization");
}
