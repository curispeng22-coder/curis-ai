import assert from "node:assert/strict";
import test from "node:test";

import { nextOrganizationAction } from "./organizationModel.mjs";

const state = {
  company: { company_id: "company-1" },
  departments: [],
  employees: [],
  projects: [],
};

test("organization onboarding follows business department, employee, then project", () => {
  assert.equal(nextOrganizationAction(state).label, "创建首个业务部门");
  assert.equal(
    nextOrganizationAction({ ...state, departments: [{ id: "department-1" }] }).label,
    "创建首位 AI 员工",
  );
  assert.equal(
    nextOrganizationAction({
      ...state,
      departments: [{ id: "department-1" }],
      employees: [{ id: "employee-1" }],
    }).label,
    "创建首个项目",
  );
});
