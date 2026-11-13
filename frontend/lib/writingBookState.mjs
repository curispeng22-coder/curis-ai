export const BOOK_SECTIONS = Object.freeze({ setup: "新书初始化", outline: "故事大纲", world: "世界设定", characters: "人物与关系" });
export const BOOK_KINDS = Object.freeze({ outline: "全书大纲", volume: "卷", chapter: "章节计划", node: "故事节点", world: "世界设定", character: "人物", relationship: "人物关系" });
export function bookLocator(params) {
  const section = params.get("book_section") || "outline", item = params.get("book_item") || "", context = params.get("context_ref") || "";
  if (!Object.hasOwn(BOOK_SECTIONS, section) || [item, context].some(v => v.length > 256 || /[\\/\u0000-\u001f]/.test(v))) throw new Error("作品条目位置无效。");
  for (const key of ["book_section", "book_item", "context_ref"]) if (params.getAll(key).length > 1) throw new Error("作品位置不能重复。");
  return { section, item, context };
}
export function writingBookHref(workspace, book, locator = {}) {
  const query = new URLSearchParams({ writing_mode: "books", book_ref: book });
  for (const [key, value] of [["book_section", locator.section], ["book_item", locator.item], ["context_ref", locator.context]]) if (value) query.set(key, value);
  bookLocator(query);
  return `/ceo-office/workspace/installed/${encodeURIComponent(workspace)}?${query}`;
}
export function bookItemDepth(item, items) {
  let depth = 0, parent = item.parent; const seen = new Set([item.id]);
  while (parent) { if (seen.has(parent)) throw new Error("作品结构位置循环。"); seen.add(parent); const row = items.find(v => v.id === parent); if (!row) break; depth += 1; parent = row.parent; }
  return depth;
}

export function orderedBookItems(items, filter = "all", collapsed = new Set()) {
  const byId = new Map(items.map(v=>[v.id,v])), needed = new Set();
  for (const item of items) if (filter === "all" || item.kind === filter) { let value = item; const seen=new Set(); while(value&&!seen.has(value.id)){needed.add(value.id);seen.add(value.id);value=byId.get(value.parent);} }
  const result=[];
  const walk=parent=>items.filter(v=>(v.parent||"")===parent&&needed.has(v.id)).sort((a,b)=>a.order-b.order||a.id.localeCompare(b.id)).forEach(v=>{result.push(v);if(!collapsed.has(v.id)||filter!=="all")walk(v.id);});
  walk("");return result;
}
