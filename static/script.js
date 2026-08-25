/* =========================================================
   Hybrid QCNN Brain Tumor Detection
   Main JavaScript
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    // ---------------------------------------------------------
    // MRI image preview
    // ---------------------------------------------------------
    const imageInput = document.getElementById("imageInput");
    const preview = document.getElementById("preview");

    if (imageInput && preview) {
        imageInput.addEventListener("change", function (event) {
            const file = event.target.files && event.target.files[0];

            if (!file) {
                preview.src = "";
                preview.style.display = "none";
                return;
            }

            if (!file.type.startsWith("image/")) {
                alert("Please select a valid image file.");
                imageInput.value = "";
                preview.src = "";
                preview.style.display = "none";
                return;
            }

            const reader = new FileReader();

            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = "block";
            };

            reader.readAsDataURL(file);
        });
    }

    // ---------------------------------------------------------
    // Prevent accidental double submission
    // ---------------------------------------------------------
    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {
        form.addEventListener("submit", function () {
            const submitButton = form.querySelector(
                'button[type="submit"], input[type="submit"]'
            );

            if (submitButton) {
                submitButton.disabled = true;

                if (submitButton.tagName === "BUTTON") {
                    submitButton.dataset.originalText =
                        submitButton.innerHTML;

                    submitButton.innerHTML =
                        '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Analyzing...';
                }
            }
        });
    });

    // ---------------------------------------------------------
    // Smooth navigation
    // ---------------------------------------------------------
    document.querySelectorAll('a[href^="#"]').forEach(function (link) {
        link.addEventListener("click", function (event) {
            const targetId = this.getAttribute("href");

            if (!targetId || targetId === "#") {
                return;
            }

            const target = document.querySelector(targetId);

            if (target) {
                event.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });
            }
        });
    });

    // ---------------------------------------------------------
    // Auto-hide Bootstrap alerts
    // ---------------------------------------------------------
    setTimeout(function () {
        document.querySelectorAll(".alert").forEach(function (alert) {
            if (alert.classList.contains("alert-dismissible")) {
                alert.style.transition = "opacity 0.5s ease";
                alert.style.opacity = "0";

                setTimeout(function () {
                    alert.remove();
                }, 500);
            }
        });
    }, 5000);

});