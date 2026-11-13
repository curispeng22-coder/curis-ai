"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import TerraShell from "../../../components/terra/TerraShell.js";
import { TerraPageHead } from "../../../components/terra/TerraPrimitives.js";
export default function HelpPage() {
  const router = useRouter();
  return <TerraShell topCrumb="本地使用帮助"><TerraPageHead title="本地使用帮助" subtitle="本地 Beta · 手工经营与创作" />
    <button onClick={() => router.back()} className="mb-5 text-ui-primary">← 返回刚才的页面</button>
    <div className="max-w-3xl space-y-6 text-sm leading-7 text-ui-txt-2">
      <section><h2 className="text-lg font-semibold text-ui-txt">建立公司与业务</h2><p>欢迎页填写称呼、公司名称即可建立本机公司和内置部门、员工，不需要先连接模型。在业务目录选择部门、业务类型，核对提案后确认，建立业务及首个工作空间。请求结果不明时保留原记录，先查询再重试。</p><Link href="/ceo-office/business" className="text-ui-primary">打开业务目录 →</Link></section>
      <section><h2 className="text-lg font-semibold text-ui-txt">保存版本与回到原依据</h2><p>在工作空间手工编辑并保存；未保存输入不等于正式版本。写作的作者确认、内容候选采用、歌曲选版与成品确认是独立动作。通过版本、来源和责任员工入口查看原对象；旧依据不会因编辑被覆盖。</p></section>
      <section><h2 className="text-lg font-semibold text-ui-txt">本地文件与 WAV</h2><p>写作确认正式稿后准备本地包并选择保存位置；取消保存不会创建文件。内容增长可导出本地验证 JSON，导出不代表已发布。音乐选择你本机的 PCM WAV：最多 16 MB、10 分钟、1–2 声道、8–192 kHz；实际试听后才能人工选择、独立确认本地成品并建立准备记录。用户文件的商业权利与歌词演唱匹配未核验。本地音频库最多保留64个文件、合计256MiB，失败登记后留下的完整文件也计入；备份不会释放该额度。</p></section>
      <section><h2 className="text-lg font-semibold text-ui-txt">退出、备份与恢复</h2><p>先保存当前编辑，再正常退出 Curis。下次启动继续使用同一本机数据。更新或恢复前，到设置建立完整备份并保留原包；恢复前核对公司、版本及预检结果，明确确认后再恢复。备份不含系统钥匙串凭证。失败时保留现场，不手动删除数据目录。</p><Link href="/ceo-office/settings" className="text-ui-primary">打开设置与备份 →</Link></section>
      <section><h2 className="text-lg font-semibold text-ui-txt">当前范围与问题说明</h2><p>当前集中验证本地手工路径。模型执行、真实员工结果和用量、外部账号连接、音频生成与平台发布尚未交付；空结果、未知费用会如实显示。遇到问题请保留错误文字、所在页面和操作步骤，通过现有交付沟通渠道反馈。本页不发送反馈或上传数据。</p></section>
    </div></TerraShell>;
}
