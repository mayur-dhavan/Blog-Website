
 document.addEventListener("DOMContentLoaded", () => {
const toggleButton = document.getElementById("darkModeToggle");
const body = document.body;
const navbar = document.getElementById("navbar");

// Check Local Storage for saved theme
const savedTheme = localStorage.getItem("theme");

if (savedTheme === "dark") {
  body.classList.add("dark-mode");
  body.classList.remove("light-mode");
} else {
  body.classList.add("light-mode");
  body.classList.remove("dark-mode");
}

// Toggle Dark Mode
toggleButton.addEventListener("click", () => {
  if (body.classList.contains("dark-mode")) {
    body.classList.remove("dark-mode");
    body.classList.add("light-mode");
    localStorage.setItem("theme", "light");
  } else {
    body.classList.remove("light-mode");
    body.classList.add("dark-mode");
    localStorage.setItem("theme", "dark");
  }
});

// Change Navbar Background on Scroll
window.addEventListener("scroll", () => {
  if (window.scrollY > 50) {
    navbar.classList.add("scrolled");
  } else {
    navbar.classList.remove("scrolled");
  }
});
});
