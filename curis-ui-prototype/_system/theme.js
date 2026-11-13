/* ============================================================
   Curis Theme Controller — Frozen
   System / Light / Dark. Default = dark (Frozen stance).
   Persists to localStorage; sets data-theme on <html>.
   ============================================================ */
(function () {
  "use strict";

  var STORAGE_KEY = "curis-theme";
  var root = document.documentElement;

  function apply(theme) {
    if (theme === "light" || theme === "dark" || theme === "system") {
      root.setAttribute("data-theme", theme);
    } else {
      root.setAttribute("data-theme", "system"); // default = system, follows OS via tokens.css media queries
    }
    syncLabel(theme);
  }

  function current() {
    try {
      var stored = localStorage.getItem(STORAGE_KEY);
      if (stored === "light" || stored === "dark" || stored === "system") return stored;
    } catch (e) {
      // localStorage may throw in file:// headless contexts; fall back to dark.
    }
    return "dark"; // Frozen default
  }

  function syncLabel(theme) {
    var btns = document.querySelectorAll("[data-curis-theme]");
    btns.forEach(function (b) {
      var t = b.getAttribute("data-curis-theme");
      b.classList.toggle("active", t === theme);
      b.setAttribute("aria-pressed", String(t === theme));
    });
  }

  function setTheme(theme) {
    localStorage.setItem(STORAGE_KEY, theme);
    apply(theme);
  }

  // Wire up any [data-curis-theme="dark|light|system"] controls
  function bind() {
    document.querySelectorAll("[data-curis-theme]").forEach(function (b) {
      b.addEventListener("click", function () {
        setTheme(b.getAttribute("data-curis-theme"));
      });
    });
  }

  // Initial paint (runs before body paint to avoid flash)
  apply(current());
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bind);
  } else {
    bind();
  }

  // Expose for manual use / other pages
  window.CurisTheme = {
    set: setTheme,
    get: current,
    cycle: function () {
      var order = ["dark", "light", "system"];
      var i = order.indexOf(current());
      setTheme(order[(i + 1) % order.length]);
    }
  };
})();
