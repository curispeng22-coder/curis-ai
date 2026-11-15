// W-09 formal-version text copy and Markdown export. Pure helpers only:
// the exported text must stay byte-identical to the selected formal snapshot,
// and all DOM/clipboard wiring stays in the component.

export function formalSnapshotText(formal) {
  const text = formal?.snapshot?.text;
  if (typeof text !== "string") throw new Error("所选正式稿缺少正文快照，请重新选择。");
  return text;
}

// 1-based position among formal.confirmed events; matches the 正式稿 N picker label.
export function formalVersionNumber(events, formalRef) {
  if (typeof formalRef !== "string" || !formalRef) throw new Error("请先选择一个已确认正式稿。");
  const number = (Array.isArray(events) ? events : []).filter((event) => event?.action === "formal.confirmed")
    .findIndex((event) => event.ref === formalRef);
  if (number === -1) throw new Error("所选正式稿不在当前章节版本记录中，请重新选择。");
  return number + 1;
}

// Sanitize characters that are invalid in file names on common platforms,
// keep Chinese intact, and cap the title so CJK names stay under OS byte limits.
export function formalMarkdownFilename(chapterTitle, version) {
  const clean = (value) => String(value ?? "")
    .replace(/[\u0000-\u001f\u007f<>:"/\\|?*]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
  const title = clean(chapterTitle) || "未命名章节";
  const capped = Array.from(title).length > 60 ? Array.from(title).slice(0, 60).join("") : title;
  return `${capped}-正式稿${clean(version)}.md`;
}
