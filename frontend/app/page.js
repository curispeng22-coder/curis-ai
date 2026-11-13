import { redirect } from "next/navigation";

/** 根路由只负责进入可恢复的 V1 Welcome / First Run。 */
export default function RootEntry() {
  redirect("/welcome");
}
