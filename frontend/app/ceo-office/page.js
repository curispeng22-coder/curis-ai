import CeoDeskOperating from "../../components/v1/CeoDeskOperating.js";
import D1Surface from "../../components/delivery/d1/D1Surface.js";

export default async function CeoOfficePage({ searchParams }) {
  // This entry depends on the request URL, including D1's Work/Result query.
  await searchParams;
  return <D1Surface legacyEntry={<CeoDeskOperating />} />;
}
