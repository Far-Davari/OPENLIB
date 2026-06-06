// Get elements
const themeToggle = document.getElementById("theme-toggle");
const htmlElement = document.documentElement;
const searchInput = document.getElementById("search-input");
const searchResults = document.getElementById("search-results");
const langToggle = document.getElementById("lang-toggle");
const enBlock = document.querySelector(".hero-en");
const faBlock = document.querySelector(".hero-fa");
const feedbackToggle = document.getElementById("feedback-toggle");
const feedbackForm = document.getElementById("feedback-form");
const feedbackPageField = document.getElementById("feedback-page");
const backToTopButton = document.getElementById("back-to-top");

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

// Hero & language toggle
if (langToggle && enBlock && faBlock) {
  const savedLang = localStorage.getItem("lang") || "en";
  setLanguage(savedLang);

  langToggle.addEventListener("click", () => {
    const currentLang = faBlock.hidden ? "en" : "fa";
    const newLang = currentLang === "en" ? "fa" : "en";
    setLanguage(newLang);
    localStorage.setItem("lang", newLang);
  });
}

function setLanguage(lang) {
  if (lang === "fa") {
    enBlock.hidden = true;
    faBlock.hidden = false;
    langToggle.textContent = "English";
  } else {
    enBlock.hidden = false;
    faBlock.hidden = true;
    langToggle.textContent = "فارسی";
  }
}

// Feedback form toggle
if (feedbackToggle && feedbackForm) {
  feedbackToggle.addEventListener("click", () => {
    const isHidden = feedbackForm.hidden;
    feedbackForm.hidden = !isHidden;
    feedbackToggle.textContent = isHidden ? "💬 Close" : "💬 Feedback";
    if (!feedbackForm.hidden && feedbackPageField) {
      feedbackPageField.value = window.location.href;
    }
  });
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

// Back-to-top button
if (backToTopButton) {
  window.addEventListener("scroll", () => {
    const scrollY = window.scrollY;
    if (scrollY < 200) {
      backToTopButton.style.opacity = "0";
      backToTopButton.style.visibility = "hidden";
      backToTopButton.classList.remove("visible");
    } else if (scrollY > 500) {
      backToTopButton.style.opacity = "1";
      backToTopButton.style.visibility = "visible";
      backToTopButton.classList.add("visible");
    } else {
      const opacity = (scrollY - 200) / 300;
      backToTopButton.style.opacity = opacity;
      backToTopButton.style.visibility = "visible";
      backToTopButton.classList.remove("visible");
    }
  });

  backToTopButton.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}
