"use client";

import { useEffect, useId, useRef, useState } from "react";
import Link from "next/link";
import { TerraIcon } from "./TerraIcons";
import { DATA_COPY } from "./TerraState";

export function TerraButton({ children, variant = "primary", size = "md", icon, className = "", ...props }) {
  const base = "inline-flex items-center justify-center gap-1.5 rounded-ui-sm text-ui-1 font-bold leading-none cursor-pointer transition-colors w-full sm:w-auto disabled:cursor-not-allowed disabled:opacity-50";
  // B1：Primary 前景走 --ui-action-primary-fg（深色主题下背景为亮绿，
  // 写死 text-white 会掉到 1.75:1 对比度）。danger 背景在两套主题下都是
  // 中低明度红，白字对比度达标，保持 text-white。
  const styles = {
    primary: "bg-ui-primary text-ui-primary-fg hover:bg-ui-primary-dark",
    ghost: "bg-ui-surface text-ui-txt-2 border border-ui-line-2 hover:border-ui-accent hover:text-ui-accent",
    danger: "bg-ui-red text-white hover:brightness-95",
  };
  const sizes = { sm: "px-3 py-2", md: "px-4 py-2.5" };
  return (
    <button className={`${base} ${styles[variant] || styles.primary} ${sizes[size] || sizes.md} ${className}`} {...props}>
      {icon && <TerraIcon name={icon} className="w-4 h-4" />}
      {children}
    </button>
  );
}

export function TerraInput({
  id,
  label,
  error,
  hint,
  className = "",
  inputClassName = "",
  required,
  ...props
}) {
  const generatedId = useId();
  const inputId = id || generatedId;
  const messageId = `${inputId}-message`;
  return (
    <div className={className}>
      {label && (
        <label htmlFor={inputId} className="block text-ui-1 font-bold text-ui-txt-2 mb-1.5 tracking-wide">
          {label}{required ? " *" : ""}
        </label>
      )}
      <input
        id={inputId}
        required={required}
        aria-invalid={error ? "true" : undefined}
        aria-describedby={error || hint ? messageId : undefined}
        className={`w-full px-3 py-2 rounded-ui-sm border text-ui-3 text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-accent ${
          error ? "border-ui-red" : "border-ui-line"
        } ${inputClassName}`}
        {...props}
      />
      {(error || hint) && (
        <p id={messageId} className={`text-ui-1 mt-1 ${error ? "text-ui-red" : "text-ui-txt-3"}`}>
          {error || hint}
        </p>
      )}
    </div>
  );
}

export function TerraTable({
  columns = [],
  rows = [],
  rowKey = "id",
  empty = "暂无数据",
  caption,
  sortKey,
  sortDirection,
  onSort,
}) {
  const keyFor = (row, index) => typeof rowKey === "function" ? rowKey(row) : row?.[rowKey] ?? index;
  return (
    <div className="overflow-x-auto rounded-ui-md border border-ui-line">
      <table className="w-full border-collapse text-left text-ui-1">
        {caption && <caption className="sr-only">{caption}</caption>}
        <thead className="bg-ui-surface-2 text-ui-txt-2">
          <tr>
            {columns.map((column) => (
              <th key={column.key} scope="col" className="px-3 py-2.5 font-bold whitespace-nowrap">
                {column.sortable && onSort ? (
                  <button
                    type="button"
                    className="inline-flex items-center min-h-[32px] gap-1 hover:text-ui-accent"
                    onClick={() => onSort(column.key)}
                    aria-label={`按${column.label}排序`}
                  >
                    {column.label}
                    {sortKey === column.key ? (sortDirection === "desc" ? "↓" : "↑") : "↕"}
                  </button>
                ) : column.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-ui-line bg-ui-surface">
          {rows.length === 0 ? (
            <tr>
              <td colSpan={Math.max(columns.length, 1)} className="px-3 py-8 text-center text-ui-txt-3">
                {empty}
              </td>
            </tr>
          ) : rows.map((row, index) => (
            <tr key={keyFor(row, index)} className="hover:bg-ui-surface-2/60">
              {columns.map((column) => (
                <td key={column.key} className="px-3 py-2.5 text-ui-txt-2 align-top">
                  {column.render ? column.render(row) : row?.[column.key] ?? DATA_COPY.noData}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function TerraDialog({ open, title, description, onClose, children, footer, drawer = false }) {
  const dialogRef = useRef(null);
  const titleId = useId();

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (open && !dialog.open) dialog.showModal();
    if (!open && dialog.open) dialog.close();
  }, [open]);

  useEffect(() => {
    if (!open) return;
    const closeOnEscape = (event) => {
      if (event.key === "Escape") onClose?.();
    };
    document.addEventListener("keydown", closeOnEscape);
    return () => document.removeEventListener("keydown", closeOnEscape);
  }, [open, onClose]);

  return (
    <dialog
      ref={dialogRef}
      aria-labelledby={titleId}
      onCancel={(event) => {
        event.preventDefault();
        onClose?.();
      }}
      onClick={(event) => {
        if (event.target === event.currentTarget) onClose?.();
      }}
      className={`m-0 border-0 bg-transparent p-0 backdrop:bg-black/35 ${
        drawer
          ? "ml-auto h-[100dvh] max-h-none w-[min(92vw,520px)]"
          : "m-auto w-[min(92vw,560px)] max-h-[90vh]"
      }`}
    >
      <section className={`bg-ui-surface border border-ui-line shadow-ui-3 flex flex-col overflow-hidden ${
        drawer ? "h-full rounded-none" : "max-h-[90vh] rounded-ui-lg"
      }`}>
        <header className="px-5 py-4 border-b border-ui-line flex items-start gap-4">
          <div className="min-w-0 flex-1">
            <h2 id={titleId} className="font-ui-sans font-semibold text-ui-4 text-ui-txt">{title}</h2>
            {description && <p className="text-ui-1 text-ui-txt-3 mt-1 leading-relaxed">{description}</p>}
          </div>
          <button type="button" onClick={onClose} className="p-1 rounded hover:bg-ui-surface-2" aria-label="关闭">
            <TerraIcon name="i-close" className="w-5 h-5 text-ui-txt-3" />
          </button>
        </header>
        <div className="flex-1 overflow-y-auto p-5">{children}</div>
        {footer && <footer className="px-5 py-4 border-t border-ui-line">{footer}</footer>}
      </section>
    </dialog>
  );
}

export function TerraModal(props) {
  return <TerraDialog {...props} />;
}

export function TerraDrawer(props) {
  return <TerraDialog {...props} drawer />;
}

export function TerraCard({ children, className = "", hover = false }) {
  return (
    <div
      className={`bg-ui-surface border border-ui-line rounded-ui-md p-4 shadow-ui ${
        hover ? "transition-all hover:shadow-ui-2 hover:-translate-y-0.5 hover:border-ui-accent" : ""
      } ${className}`}
    >
      {children}
    </div>
  );
}

export function TerraCardHeader({ icon, iconClass = "primary", title }) {
  const iconBg = {
    green: "bg-ui-green-soft text-ui-green",
    cyan: "bg-ui-cyan-soft text-ui-cyan",
    amber: "bg-ui-amber-soft text-ui-amber",
    red: "bg-ui-red-soft text-ui-red",
    primary: "bg-ui-primary-light text-ui-primary",
    surface: "bg-ui-surface-2 text-ui-txt-2",
    violet: "bg-ui-violet-soft text-ui-violet",
  };
  return (
    <div className="flex items-center gap-2 mb-3">
      <span className={`w-[34px] h-[34px] rounded-ui-sm grid place-items-center flex-shrink-0 ${iconBg[iconClass]}`}>
        <TerraIcon name={icon} className="w-5 h-5" />
      </span>
      <h3 className="font-ui-sans font-semibold text-ui-4 leading-tight text-ui-txt">{title}</h3>
    </div>
  );
}

export function TerraEmpty({ icon, children, className = "" }) {
  return (
    <div
      className={`border-[1.5px] border-dashed border-ui-line-2 rounded-ui-md py-5 px-6 text-center text-ui-txt-3 text-ui-2 leading-relaxed bg-ui-surface-2 ${className}`}
    >
      {icon && <TerraIcon name={icon} className="w-6 h-6 text-ui-line-2 block mx-auto mb-1.5" />}
      {children}
    </div>
  );
}

export function TerraBoundary({ children, className = "" }) {
  return (
    <div className={`flex items-center gap-2 bg-ui-accent-light border border-ui-line rounded-ui-sm px-3 py-2 text-ui-1 text-ui-accent ${className}`}>
      <TerraIcon name="i-verified" className="w-4 h-4 text-ui-accent" />
      {children}
    </div>
  );
}

// B7：语义标签一律胶囊圆角（--ui-r-pill），语义只靠 --ui-success/warning/danger/
// accent 文字色 + 中性底承载，与原型 `.status` / `.mock-badge` 同构。
// 未知 color 回落到 grey，避免拼出 `undefined` 类名导致标签完全无样式。
export function TerraTag({ children, color = "grey", icon, className = "" }) {
  const styles = {
    green: "bg-ui-green-soft text-ui-green",
    amber: "bg-ui-amber-soft text-ui-amber",
    red: "bg-ui-red-soft text-ui-red",
    primary: "bg-ui-primary-light text-ui-primary",
    cyan: "bg-ui-cyan-soft text-ui-cyan",
    violet: "bg-ui-violet-soft text-ui-violet",
    grey: "bg-ui-surface-3 text-ui-txt-3",
  };
  return (
    <span className={`inline-flex items-center gap-1 text-ui-1 font-semibold rounded-ui-pill px-2 py-0.5 ${styles[color] || styles.grey} ${className}`}>
      {icon && <span className="w-2 h-2 rounded-ui-pill bg-current" />}
      {children}
    </span>
  );
}

function fact(value, fallback = DATA_COPY.noData) {
  return value === null || value === undefined || value === "" ? fallback : value;
}

export function ProjectCard({ project = {}, href, actions }) {
  const status = {
    planned: { label: "规划中", color: "grey" },
    active: { label: "执行中", color: "green" },
    blocked: { label: "阻塞", color: "red" },
    completed: { label: "已完成", color: "cyan" },
    archived: { label: "已归档", color: "amber" },
  }[project.status] || { label: fact(project.status, "未记录"), color: "grey" };
  const content = (
    <TerraCard hover={!!href}>
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <h3 className="font-ui-sans font-semibold text-ui-4 text-ui-txt truncate">{fact(project.name, "未命名项目")}</h3>
          <p className="text-ui-1 text-ui-txt-3 mt-1">{fact(project.department || project.stage)}</p>
        </div>
        <TerraTag color={status.color}>{status.label}</TerraTag>
      </div>
      {project.goal && <p className="mt-3 text-ui-1 text-ui-txt-2 line-clamp-2">{project.goal}</p>}
      <div className="mt-3 text-ui-1 text-ui-txt-2">负责人：{fact(project.owner, DATA_COPY.noOwner)}</div>
      {typeof project.progress === "number" && (
        <div className="mt-3">
          <div className="h-1.5 rounded-full bg-ui-surface-3 overflow-hidden" aria-label={`进度 ${project.progress}%`}>
            <div className="h-full bg-ui-primary" style={{ width: `${Math.min(100, Math.max(0, project.progress))}%` }} />
          </div>
        </div>
      )}
      {actions && <div className="flex gap-2 mt-3">{actions}</div>}
    </TerraCard>
  );
  return href ? <Link href={href} className="block no-underline text-inherit">{content}</Link> : content;
}

export function EmployeeCard({ employee = {}, department, project, actions }) {
  const capabilities = employee.capabilityProfile || employee.capability_profile ||
    (Array.isArray(employee.capabilities) ? employee.capabilities.join("、") : "");
  const status = {
    idle: { label: "空闲", color: "grey" },
    assigned: { label: "工作中", color: "cyan" },
    working: { label: "工作中", color: "cyan" },
    completed: { label: "已完成", color: "green" },
    error: { label: "异常", color: "red" },
    disabled: { label: "已暂停", color: "amber" },
  }[employee.status] || { label: fact(employee.status, "未记录"), color: "grey" };
  return (
    <TerraCard>
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2.5 min-w-0">
          <span className="w-9 h-9 rounded-full bg-ui-primary text-ui-primary-fg grid place-items-center text-ui-3 font-bold flex-shrink-0">
            {fact(employee.name, "?").slice(0, 1)}
          </span>
          <div className="min-w-0">
            <h3 className="font-semibold text-ui-3 text-ui-txt truncate">{fact(employee.name, "未命名员工")}</h3>
            <p className="text-ui-1 text-ui-txt-3 truncate">{fact(employee.role, DATA_COPY.unassigned)}</p>
          </div>
        </div>
        <TerraTag color={status.color}>
          {status.label}
        </TerraTag>
      </div>
      <dl className="mt-3 space-y-1 text-ui-1 text-ui-txt-3">
        <div><dt className="inline">部门：</dt><dd className="inline">{fact(department, DATA_COPY.unassigned)}</dd></div>
        <div><dt className="inline">项目：</dt><dd className="inline">{fact(project, DATA_COPY.unassigned)}</dd></div>
        <div><dt className="inline">能力：</dt><dd className="inline">{fact(capabilities, DATA_COPY.unassigned)}</dd></div>
      </dl>
      {actions && <div className="flex gap-2 mt-3">{actions}</div>}
    </TerraCard>
  );
}

export function CapabilityCard({ capability = {}, actions }) {
  return (
    <TerraCard>
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <h3 className="font-ui-sans font-semibold text-ui-4 text-ui-txt truncate">
            {fact(capability.name, "未命名能力")}
          </h3>
          <p className="text-ui-1 text-ui-txt-3 mt-1">
            {fact(capability.type)} · {fact(capability.provider)}
          </p>
        </div>
        <TerraTag color={capability.status === "available" ? "green" : capability.status === "blocked" ? "red" : "grey"}>
          {fact(capability.status)}
        </TerraTag>
      </div>
      {actions && <div className="flex gap-2 mt-3">{actions}</div>}
    </TerraCard>
  );
}

export function TerraStatusBadge({ label, status }) {
  const styles = {
    available: "bg-ui-green-soft text-ui-green",
    blocked: "bg-ui-amber-soft text-ui-amber",
    official: "bg-ui-primary-light text-ui-primary",
    custom: "bg-ui-violet-soft text-ui-violet",
  };
  return (
    <span className={`text-ui-1 font-bold px-2 py-0.5 rounded ${styles[status] || styles.available}`}>
      {label}
    </span>
  );
}

export function TerraFact({ value, label }) {
  return (
    <div className="bg-ui-surface border border-ui-line rounded-ui-md px-3.5 py-2.5 min-w-[96px]">
      <div className="font-ui-sans font-bold text-ui-7 text-ui-primary leading-none">{value}</div>
      <div className="text-ui-1 text-ui-txt-3 mt-0.5">{label}</div>
    </div>
  );
}

export function TerraFacts({ items }) {
  return (
    <div className="flex flex-wrap gap-2.5">
      {items.map((it, i) => (
        <TerraFact key={i} value={it.value} label={it.label} />
      ))}
    </div>
  );
}

export function TerraPageHead({ title, subtitle, pill, facts, actions, children }) {
  return (
    <div className="flex flex-col sm:flex-row items-start gap-4 mb-3.5">
      <div className="flex-1 min-w-0">
        <h1 className="font-ui-sans font-bold text-ui-6 leading-tight text-ui-txt">{title}</h1>
        {subtitle && <div className="text-ui-1 text-ui-txt-3 mt-1">{subtitle}</div>}
        {pill && (
          <div className="inline-flex items-center gap-1.5 bg-ui-accent-light text-ui-accent rounded-full px-3 py-1 text-ui-1 font-semibold mt-1.5">
            {pill.icon && <TerraIcon name={pill.icon} className="w-4 h-4" />}
            {pill.text}
          </div>
        )}
      </div>
      <div className="hidden sm:block flex-1" />
      <div className="flex flex-col items-start sm:items-end gap-3 max-w-full">
        {facts && <TerraFacts items={facts} />}
        {actions && <div className="flex items-center gap-2">{actions}</div>}
      </div>
      {children}
    </div>
  );
}

export function TerraBackLink({ href, children }) {
  return (
    // min-h-[32px]：Frozen 触达红线 ≥32px（12px 文本行高仅 18px，需补足命中区）
    <Link href={href} className="inline-flex items-center min-h-[32px] gap-1 text-ui-primary text-ui-1 font-bold no-underline mb-2.5 hover:opacity-80">
      <TerraIcon name="i-arrow_back" className="w-4 h-4" />
      {children}
    </Link>
  );
}

export function TerraSearch({ placeholder, ariaLabel, className = "", value, onChange }) {
  const [inner, setInner] = useState("");
  const isControlled = value !== undefined;
  const current = isControlled ? value : inner;
  const handle = (e) => {
    const next = e.target.value;
    if (!isControlled) setInner(next);
    if (onChange) onChange(next);
  };
  return (
    // 容器高度锁到 --ui-ctl-h-sm(32px)，input 撑满高度 —— 输入框本身也需满足触达红线。
    // 描边用 ring-inset 而非 border：border 会吃掉 2px 内容盒高度，导致 input 只有 30px。
    <div className={`flex items-center gap-1.5 bg-ui-surface ring-1 ring-inset ring-ui-line-2 rounded-full px-3 h-[var(--ui-ctl-h-sm)] w-[220px] max-w-full ${className}`}>
      <TerraIcon name="i-search" className="w-4 h-4 text-ui-txt-3 flex-shrink-0" />
      <input
        type="text"
        value={current}
        placeholder={placeholder}
        aria-label={ariaLabel}
        onChange={handle}
        className="border-0 outline-0 bg-transparent text-ui-2 w-full h-full text-ui-txt placeholder:text-ui-txt-3 min-w-0"
      />
    </div>
  );
}
