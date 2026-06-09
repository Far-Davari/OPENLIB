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
const continueContainer = document.getElementById("continue-reading-container");
const progressBar = document.getElementById("progress-bar");

let searchIndex = [];

// Three-state theme toggle
const THEME_STATES = ["light", "dark", "auto"];
const THEME_ICONS = {
  light: "☀️",
  dark: "🌙",
  auto: "🌗",
};
const THEME_LABELS = {
  light: "Switch to dark mode",
  dark: "Switch to auto (system) mode",
  auto: "Switch to light mode",
};

function applyTheme(state) {
  htmlElement.setAttribute("data-theme", state);
  themeToggle.setAttribute("data-theme-state", state);
  themeToggle.innerHTML = THEME_ICONS[state];
  themeToggle.setAttribute("aria-label", THEME_LABELS[state]);
  localStorage.setItem("theme", state);
}

const systemDarkQuery = window.matchMedia("(prefers-color-scheme: dark)");
systemDarkQuery.addEventListener("change", () => {
  if (htmlElement.getAttribute("data-theme") === "auto") {
  }
});

const savedTheme = localStorage.getItem("theme") || "light";
applyTheme(savedTheme);

themeToggle.addEventListener("click", () => {
  const current = htmlElement.getAttribute("data-theme");
  const currentIndex = THEME_STATES.indexOf(current);
  const nextState = THEME_STATES[(currentIndex + 1) % THEME_STATES.length];
  applyTheme(nextState);
});

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

  if (window.continueLink) {
    window.continueLink.textContent =
      lang === "fa"
        ? "📖 ادامهٔ خواندن از جایی که متوقف شدید"
        : "📖 Continue reading where you left off";

    window.continueLink.setAttribute("lang", lang);
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

// Reading progress bar
if (progressBar) {
  window.addEventListener("scroll", () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight;
    const winHeight = window.innerHeight;
    const scrollableHeight = docHeight - winHeight;

    if (scrollableHeight > 0) {
      const scrollPercent = (scrollTop / scrollableHeight) * 100;
      progressBar.style.width = Math.min(scrollPercent, 100) + "%";
    } else {
      progressBar.style.width = "0%";
    }
  });
}

// Save last read position
if (window.location.pathname.includes("/chapters/")) {
  localStorage.setItem("lastChapter", window.location.href);
}

if (continueContainer && localStorage.getItem("lastChapter")) {
  const lastUrl = localStorage.getItem("lastChapter");
  const link = document.createElement("a");
  link.href = lastUrl;
  link.className = "continue-reading-link";

  const currentLang = localStorage.getItem("lang") || "en";
  link.setAttribute("lang", currentLang);
  link.textContent =
    currentLang === "fa"
      ? "📖 ادامهٔ خواندن از جایی که متوقف شدید"
      : "📖 Continue reading where you left off";

  window.continueLink = link;

  continueContainer.appendChild(link);
}

// Copy link buttons
document.querySelectorAll(".copy-link").forEach((button) => {
  button.addEventListener("click", () => {
    const url = button.getAttribute("data-url");
    const copySpan = button.querySelector(".copy-text");
    const originalHTML = copySpan ? copySpan.innerHTML : button.innerHTML;

    // Get the language from the parent share container
    const shareContainer = button.closest(".share-buttons");
    const lang = shareContainer ? shareContainer.getAttribute("lang") : "en";
    const copiedText = lang === "fa" ? "✅ کپی شد!" : "✅ Copied!";

    navigator.clipboard
      .writeText(url)
      .then(() => {
        if (copySpan) {
          copySpan.textContent = copiedText;
        } else {
          button.innerHTML = copiedText;
        }
        setTimeout(() => {
          if (copySpan) {
            copySpan.innerHTML = originalHTML;
          } else {
            button.innerHTML = originalHTML;
          }
        }, 2000);
      })
      .catch(() => {
        alert("Could not copy link. Please copy it manually.");
      });
  });
});

// Print / PDF buttons
document.querySelectorAll(".print-page").forEach((button) => {
  button.addEventListener("click", () => {
    window.print();
  });
});
