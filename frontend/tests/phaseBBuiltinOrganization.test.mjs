import test from "node:test";
import assert from "node:assert/strict";
import { buildOrganizationProjection } from "../lib/organizationProjection.js";

test("department responsibility stays visible without user businesses", () => {
  const projection = buildOrganizationProjection({
    company: { company_id: "company", name: "Company" }, businesses: [],
    departments: [{ id: "department", company_id: "company", name: "空间工程部" }],
    employees: [{ id: "employee", company_id: "company", department_id: "department", name: "改名仍保留", role: "负责人" }],
    departmentAssignments: [{ entity_id: "assignment", company_id: "company", data: {
      scopeRef: "department", companyEmployeeRef: "employee", roleRef: "role", roleName: "负责人", responsibility: "交付责任",
    } }],
  });
  assert.equal(projection.businesses.length, 0);
  assert.equal(projection.departments[0].assignments[0].employee.name, "改名仍保留");
  assert.equal(projection.employees[0].assignments[0].scopeName, "空间工程部");
});
