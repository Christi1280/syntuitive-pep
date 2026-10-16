document.addEventListener("DOMContentLoaded", () => {
  const menuButton = document.querySelector("#mobile-menu");
  const sidebar = document.querySelector("#sidebar");

  if (menuButton && sidebar) {
    menuButton.addEventListener("click", () => {
      const isOpen = sidebar.classList.toggle("show");
      menuButton.setAttribute("aria-expanded", String(isOpen));
    });
  }

  const attempts = Number(localStorage.getItem("pep_attempts") || 0);
  const correct = Number(localStorage.getItem("pep_correct") || 0);
  document.querySelectorAll('[data-progress="attempts"]').forEach((element) => {
    element.textContent = String(attempts);
  });
  document.querySelectorAll('[data-progress="accuracy"]').forEach((element) => {
    element.textContent = `${attempts ? Math.round((correct / attempts) * 100) : 0}%`;
  });
});
