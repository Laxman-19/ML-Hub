/* ML Hub — theme toggle, live search, category filtering. */
(function () {
  "use strict";

  // ---------- Dark mode (persisted, system-default) ----------
  var root = document.documentElement;
  var KEY = "mlhub-theme";

  function applyTheme(theme) {
    root.setAttribute("data-bs-theme", theme);
    var icon = document.querySelector("#theme-toggle .bi");
    if (icon) {
      icon.className = theme === "dark" ? "bi bi-sun" : "bi bi-moon-stars";
    }
  }

  var saved = localStorage.getItem(KEY);
  var prefersDark = window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches;
  applyTheme(saved || (prefersDark ? "dark" : "light"));

  var toggle = document.getElementById("theme-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = root.getAttribute("data-bs-theme") === "dark" ? "light" : "dark";
      localStorage.setItem(KEY, next);
      applyTheme(next);
    });
  }

  // ---------- Homepage search + category filter ----------
  var search = document.getElementById("project-search");
  var grid = document.getElementById("project-grid");
  if (!grid) return;

  var cols = Array.prototype.slice.call(grid.querySelectorAll(".project-col"));
  var noResults = document.getElementById("no-results");
  var filters = document.getElementById("category-filters");
  var activeCategory = "all";

  function refresh() {
    var q = (search && search.value ? search.value : "").trim().toLowerCase();
    var visible = 0;
    cols.forEach(function (col) {
      var matchesText = !q || col.dataset.name.indexOf(q) !== -1;
      var matchesCat = activeCategory === "all" ||
        col.dataset.category === activeCategory;
      var show = matchesText && matchesCat;
      col.classList.toggle("d-none", !show);
      if (show) visible++;
    });
    if (noResults) noResults.classList.toggle("d-none", visible !== 0);
  }

  if (search) search.addEventListener("input", refresh);

  if (filters) {
    filters.addEventListener("click", function (e) {
      var btn = e.target.closest(".chip");
      if (!btn) return;
      filters.querySelectorAll(".chip").forEach(function (c) {
        c.classList.remove("chip-active");
      });
      btn.classList.add("chip-active");
      activeCategory = btn.dataset.category;
      refresh();
    });
  }
})();
