// ==========================
//  Global App UI Scripts
// ==========================

document.addEventListener("DOMContentLoaded", function () {

    // =======================
    // Toast Notification System
    // =======================
    window.showToast = function (message, type = "info") {
        const container = document.querySelector(".toast-container");
        if (!container) return;

        const toast = document.createElement("div");
        toast.className = `toast align-items-center text-bg-${type} border-0`;
        toast.role = "alert";

        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>`;

        container.appendChild(toast);

        const bootstrapToast = new bootstrap.Toast(toast, { delay: 3000 });
        bootstrapToast.show();

        // Remove after hidden
        toast.addEventListener("hidden.bs.toast", () => toast.remove());
    };


    // =======================
    // Theme Toggle System
    // =======================
    const icon = document.getElementById("themeIcon");
    const themeToggle = document.getElementById("themeToggle");

    function applyTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        localStorage.setItem("theme", theme);

        if (icon) {
            icon.className = theme === "dark"
                ? "bi bi-sun-fill"
                : "bi bi-moon-stars-fill";
        }
    }

    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            const nextTheme =
                document.documentElement.getAttribute("data-theme") === "light"
                    ? "dark"
                    : "light";
            applyTheme(nextTheme);
        });
    }

    // Set initial theme from localStorage
    applyTheme(localStorage.getItem("theme") || "light");


    // =======================
    // Sticky Navbar on Scroll
    // =======================
    const nav = document.getElementById("mainNav");

    if (nav) {
        window.addEventListener("scroll", () => {
            if (window.scrollY > 10) {
                nav.classList.add("sticky-nav-active");
            } else {
                nav.classList.remove("sticky-nav-active");
            }
        });
    }


    // =======================
    // Floating Cart Button (pulse animation)
    // =======================
    const cartFab = document.querySelector(".floating-cart-btn");
    if (cartFab) {
        cartFab.addEventListener("mouseenter", () => {
            cartFab.style.transform = "scale(1.12)";
        });
        cartFab.addEventListener("mouseleave", () => {
            cartFab.style.transform = "scale(1)";
        });
    }

});
