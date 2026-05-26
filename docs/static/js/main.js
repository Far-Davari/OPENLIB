// Get elements
const themeToggle = document.getElementById("theme-toggle");
const htmlElement = document.documentElement;

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
