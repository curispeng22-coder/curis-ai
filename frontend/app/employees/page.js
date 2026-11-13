import { redirect } from "next/navigation";

// 旧暗色员工管理页 → 重定向到新员工管理页
export default function EmployeesRedirect() {
  redirect("/ceo-office/organization/employees");
}
