// Get elements
const themeToggle = document.getElementById("theme-toggle");
const htmlElement = document.documentElement;
const searchInput = document.getElementById("search-input");
const searchResults = document.getElementById("search-results");
let searchIndex = [];

// Read the saved theme from LocalStorage
const savedTheme = localStorage.getItem("theme");
if (savedTheme) {
  htmlElement.setAttribute("data-theme", savedTheme);
  updateToggleIcon(savedTheme);
} else {
  updateToggleIcon("light");
}

// Toggle function
themeToggle.addEventListener("click", () => {
  const currentTheme = htmlElement.getAttribute("data-theme");
  const newTheme = currentTheme === "dark" ? "light" : "dark";

  htmlElement.setAttribute("data-theme", newTheme);

  localStorage.setItem("theme", newTheme);
  updateToggleIcon(newTheme);
});

// Update the button icon and label
function updateToggleIcon(theme) {
  if (theme === "dark") {
    themeToggle.innerHTML = "☀️";
    themeToggle.setAttribute("aria-label", "Switch to light mode");
  } else {
    themeToggle.innerHTML = "🌙";
    themeToggle.setAttribute("aria-label", "Switch to dark mode");
  }
}

// ==== Search functionality ====
// Load the search index once
fetch(window.BASE_PATH + "search-index.json")
  .then((response) => response.json())
  .then((data) => {
    searchIndex = data;
  })
  .catch((error) => {
    console.error("Failed to load search index:", error);
  });

// Filter and display results
searchInput.addEventListener("input", () => {
  const query = searchInput.value.trim().toLowerCase();
  if (query.length === 0) {
    searchResults.hidden = true;
    return;
  }

  const matches = searchIndex.filter((item) => {
    return (
      item.title.toLowerCase().includes(query) ||
      item.book.toLowerCase().includes(query)
    );
  });

  if (matches.length === 0) {
    searchResults.innerHTML =
      '<div class="search-no-results">No results found</div>';
    searchResults.hidden = false;
    return;
  }

  // Build HTML
  let html = "";
  matches.forEach((item) => {
    const fullUrl = window.BASE_PATH.slice(0, -1) + item.url;
    const typeLabel = item.type === "book" ? "Book" : "Chapter";
    html += `
    <a href="${fullUrl}" class="search-result-item">
      <span class="search-result-title">${escapeHtml(item.title)}</span>
      <span class="search-result-meta">${typeLabel} - ${escapeHtml(item.book)}</span>
      ${item.snippet ? `<span class="search-result-snippet">${escapeHtml(item.snippet)}</span>` : ""}
    </a>`;
  });

  searchResults.innerHTML = html;
  searchResults.hidden = false;
});

// Hide results when clicking outside
document.addEventListener("click", (e) => {
  if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
    searchResults.hidden = true;
  }
});

// Hide on Escape key
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    searchResults.hidden = true;
    searchInput.blur();
  }
});

// Helper to prevent XSS in search results
function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
