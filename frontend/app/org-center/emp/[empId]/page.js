import { redirect } from "next/navigation";

// 旧暗色「员工详情」深链 → 重定向到新 Terra 浅色人事部员工管理
export default function OrgCenterEmpRedirect() {
  redirect("/ceo-office/organization/employees");
}
