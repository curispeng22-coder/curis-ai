import assert from "node:assert/strict";
import test from "node:test";

import {
  buildOrganizationProjection,
  organizationBusinessMatches,
  organizationEmployeeMatches,
} from "../lib/organizationProjection.js";
import { getOrganizationProjection } from "../lib/runtimeApi.js";


const payload = {
  company: { company_id: "company-1", name: "Curis", status: "active" },
  departments: [{ id: "department-1", company_id: "company-1", name: "内容与市场部", mission: "负责增长" }],
  employees: [{ id: "employee-1", company_id: "company-1", department_id: "department-1", name: "小策", role: "内容策划", status: "idle", enabled: 1 }],
  businesses: [{
    business_id: "business-1",
    company_id: "company-1",
    department_id: "department-1",
    name: "内容增长",
    lifecycle_status: "ACTIVE",
    definition: { goal: "稳定增长", positioning: "内容经营" },
    operatingSummary: { workspaceCount: 1, needsAttentionCount: 0 },
    workspaces: [{ workspace_id: "workspace-1", name: "小红书运营", status: "DRAFT" }],
    team: [{
      entity_id: "assignment-1",
      owner_ref: "runtime-employee-1",
      data: {
        employeeRef: "runtime-employee-1",
        companyEmployeeRef: "employee-1",
        employeeIdentityStatus: "VERIFIED_EXPLICIT_BRIDGE",
        roleRef: "role-content",
        responsibility: "负责内容增长计划",
        isLeader: true,
      },
    }],
  }],
};


test("Organization projection keeps Business first and resolves canonical Employee identity", () => {
  const projection = buildOrganizationProjection(payload);
  const business = projection.departments[0].businesses[0];
  assert.equal(business.leader.name, "小策");
  assert.equal(business.staffingCount, 1);
  assert.equal(business.roleCount, 1);
  assert.equal(business.vacancyCount, 0);
  assert.equal(projection.employees[0].assignments[0].businessName, "内容增长");
  assert.equal(organizationBusinessMatches(business, "小策"), true);
  assert.equal(organizationEmployeeMatches(projection.employees[0], "内容增长"), true);
});


test("Unverified Runtime Employee reference does not become a Company Employee", () => {
  const unverified = structuredClone(payload);
  delete unverified.businesses[0].team[0].data.companyEmployeeRef;
  unverified.businesses[0].team[0].data.employeeIdentityStatus = "UNRESOLVED";
  const projection = buildOrganizationProjection(unverified);
  assert.equal(projection.businesses[0].leader, null);
  assert.equal(projection.businesses[0].staffingCount, 0);
  assert.equal(projection.employees[0].assignments.length, 0);
});


test("One Employee keeps multiple real Business assignments without a fake primary", () => {
  const multiple = structuredClone(payload);
  multiple.businesses.push({
    ...structuredClone(multiple.businesses[0]),
    business_id: "business-2",
    name: "品牌经营",
    team: [{
      ...structuredClone(multiple.businesses[0].team[0]),
      entity_id: "assignment-2",
      data: {
        ...structuredClone(multiple.businesses[0].team[0].data),
        responsibility: "负责品牌内容规划",
      },
    }],
  });
  const employee = buildOrganizationProjection(multiple).employees[0];
  assert.deepEqual(employee.assignments.map((item) => item.businessName), ["内容增长", "品牌经营"]);
  assert.equal(Object.hasOwn(employee, "primaryAssignment"), false);
});


test("Empty canonical data stays empty instead of rendering Figma fixtures", () => {
  const projection = buildOrganizationProjection({
    company: payload.company,
    departments: [],
    businesses: [],
    employees: [],
  });
  assert.equal(projection.departments.length, 0);
  assert.equal(projection.businesses.length, 0);
  assert.equal(projection.employees.length, 0);
});


test("Organization API wrapper keeps the canonical company path", async () => {
  let path;
  await getOrganizationProjection("company/一", async (value) => {
    path = value;
    return payload;
  });
  assert.equal(path, "/api/workspace/runtime/foundation/companies/company%2F%E4%B8%80/organization");
});

test("current scoped team has two responsibilities and one renamed disabled holder", () => {
  const employee = { id: "holder", company_id: "A", name: "当前名字", enabled: 0, department_id: "", status: "idle" };
  const data = { companyEmployeeRef: "holder", employeeIdentityStatus: "VERIFIED_EXPLICIT_BRIDGE", employeeEnabled: false, roleName: "章节作者", roleStatus: "ASSIGNED" };
  const projection = buildOrganizationProjection({ company: { company_id: "A" }, departments: [], employees: [employee], businesses: [{ business_id: "B", company_id: "A", team: [
    { entity_id: "leader", lifecycle_status: "ACTIVE", data: { ...data, scopeType: "BUSINESS", scopeRef: "B", roleRef: "leader-role", isLeader: true } },
    { entity_id: "author", lifecycle_status: "ACTIVE", workspace_id: "W", data: { ...data, scopeType: "WORKSPACE", scopeRef: "W", roleRef: "author-role" } },
    { entity_id: "old", lifecycle_status: "CLOSED", data: { ...data, roleRef: "old-role" } }] }] });
  const business = projection.businessById.get("B");
  assert.equal(business.staffingCount, 1); assert.equal(business.roleCount, 2);
  assert.equal(business.leader.name, "当前名字");
  assert.equal(projection.employees[0].enabled, false);
  assert.equal(projection.employees[0].status, "已停用");
  assert.ok(business.assignments.every((item) => item.enabled === false));
  assert.equal(business.assignments[1].workspaceId, "W");
});

test("Workspace leader is not substituted for the Business Leader", () => {
  const p = buildOrganizationProjection({ company: { company_id: "A" }, employees: [{ id: "E", company_id: "A" }], businesses: [{ company_id: "A", business_id: "B", team: [{ entity_id: "W-leader", data: { companyEmployeeRef: "E", isLeader: true, scopeType: "WORKSPACE", scopeRef: "W" } }] }] });
  assert.equal(p.businessById.get("B").leader, null);
});


test("staffing display actual BusinessFocus separates one holder and two responsibilities without coverage",async()=>{
 const {readFileSync}=await import('node:fs'),{createRequire}=await import('node:module'),vm=await import('node:vm');const require=createRequire(import.meta.url),React=require('react'),server=require('react-dom/server'),swc=require('next/dist/build/swc');await swc.loadBindings();
 const source=readFileSync(new URL('../app/ceo-office/organization/OrganizationCenter.js',import.meta.url),'utf8').replace('function BusinessFocus(', 'export function BusinessFocus(');
 const code=(await swc.transform(source,{filename:'OrganizationCenter.js',isModule:true,jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'automatic'}}},module:{type:'commonjs'}})).code;
 const loaded={exports:{}};const tag=({children,...props})=>React.createElement('a',props,children);
 vm.runInNewContext(code,{module:loaded,exports:loaded.exports,require:path=>{
  if(path==='react'||path==='react/jsx-runtime')return require(path);
  if(path==='next/link')return {__esModule:true,default:tag};
  if(path.endsWith('.module.css'))return {__esModule:true,default:new Proxy({},{get:(_,key)=>String(key)})};
  if(path.includes('EmployeeAvatar'))return {EmployeeAvatar:()=>React.createElement('span')};
  if(path.includes('theme.js'))return {roleLabel:value=>value};
  return {};
 }});
 const data=structuredClone(payload);data.businesses[0].team=[{entity_id:'leader-assignment',company_id:'company-1',lifecycle_status:'ACTIVE',data:{roleRef:'leader-role',roleName:'业务负责人',companyEmployeeRef:'employee-1',scopeType:'BUSINESS',scopeRef:'business-1',isLeader:true,employeeEnabled:true,roleStatus:'ASSIGNED'}},{entity_id:'author-assignment',company_id:'company-1',workspace_id:'workspace-1',lifecycle_status:'ACTIVE',data:{roleRef:'author-role',roleName:'工作空间创作负责人',companyEmployeeRef:'employee-1',scopeType:'WORKSPACE',scopeRef:'workspace-1',employeeEnabled:true,roleStatus:'ASSIGNED'}}];
 function render(value){const projection=buildOrganizationProjection(value),business=projection.businesses[0];return {business,html:server.renderToStaticMarkup(React.createElement(loaded.exports.BusinessFocus,{business,projection}))};}
 let result=render(data);assert.equal(result.business.staffingCount,1);assert.equal(result.business.roleCount,2);assert.match(result.html,/<dt>岗位职责<\/dt><dd>2 项<\/dd>/);assert.match(result.html,/<dt>员工<\/dt><dd>1 名<\/dd>/);assert.doesNotMatch(result.html,/1\/2 已配置|全部岗位已配置/);
 data.employees[0].enabled=0;result=render(data);assert.equal(result.business.assignments.every(a=>a.enabled),false);assert.doesNotMatch(result.html,/已配置|全部岗位已配置/);
 data.businesses[0].team=[];result=render(data);assert.match(result.html,/尚无岗位事实/);assert.match(result.html,/<dt>员工<\/dt><dd>0 名<\/dd>/);assert.doesNotMatch(result.html,/已配置/);
});
