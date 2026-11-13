import { TerraLoadingSkeleton } from "../components/terra/TerraState.js";

export default function AppLoading() {
  return (
    <main className="min-h-screen bg-ui-bg px-4 py-10" aria-label="页面加载中">
      <div className="mx-auto max-w-6xl">
        <TerraLoadingSkeleton variant="page" />
      </div>
    </main>
  );
}
