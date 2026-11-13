/* eslint-disable @next/next/no-img-element */
"use client";

import { useEffect, useMemo, useState } from "react";

import { getEmployeeAvatarBlob } from "../../lib/api.js";

export const EMPLOYEE_AVATAR_PRESETS = [
  { id: "iris", label: "鸢尾", src: "/avatars/curis-employee/iris.svg" },
  { id: "sage", label: "青禾", src: "/avatars/curis-employee/sage.svg" },
  { id: "coral", label: "珊瑚", src: "/avatars/curis-employee/coral.svg" },
  { id: "amber", label: "琥珀", src: "/avatars/curis-employee/amber.svg" },
  { id: "sky", label: "晴空", src: "/avatars/curis-employee/sky.svg" },
  { id: "plum", label: "青梅", src: "/avatars/curis-employee/plum.svg" },
  { id: "mint", label: "薄荷", src: "/avatars/curis-employee/mint.svg" },
  { id: "slate", label: "岩蓝", src: "/avatars/curis-employee/slate.svg" },
];

const PRESET_BY_REF = new Map(
  EMPLOYEE_AVATAR_PRESETS.map((preset) => [`preset:${preset.id}`, preset]),
);

export function EmployeeAvatar({ employee, className = "h-10 w-10", previewUrl = "" }) {
  const avatarRef = String(employee?.avatar_ref || employee?.avatarRef || "");
  const [assetUrl, setAssetUrl] = useState("");
  const [failed, setFailed] = useState(false);
  const preset = PRESET_BY_REF.get(avatarRef);
  const name = String(employee?.name || "?").trim();

  useEffect(() => {
    let disposed = false;
    let objectUrl = "";
    setAssetUrl("");
    setFailed(false);
    if (!avatarRef.startsWith("asset:") || !employee?.id) return undefined;
    getEmployeeAvatarBlob(employee.id)
      .then((blob) => {
        if (disposed) return;
        objectUrl = URL.createObjectURL(blob);
        setAssetUrl(objectUrl);
      })
      .catch(() => {
        if (!disposed) setFailed(true);
      });
    return () => {
      disposed = true;
      if (objectUrl) URL.revokeObjectURL(objectUrl);
    };
  }, [avatarRef, employee?.id]);

  const source = useMemo(
    () => (failed ? "" : previewUrl || preset?.src || assetUrl),
    [assetUrl, failed, preset?.src, previewUrl],
  );

  return (
    <span
      className={`relative inline-grid shrink-0 place-items-center overflow-hidden rounded-full bg-ui-primary text-ui-primary-fg font-bold ${className}`}
      aria-label={`${name || "员工"}的头像`}
      data-avatar-ref={avatarRef || "fallback"}
    >
      {source ? (
        <img src={source} alt="" className="h-full w-full object-cover" onError={() => setFailed(true)} />
      ) : (
        <span aria-hidden="true">{name.slice(0, 1).toUpperCase() || "?"}</span>
      )}
    </span>
  );
}
