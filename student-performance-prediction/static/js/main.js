// main.js
// Handles dark mode toggle, form validation, and small UI animations.
// Kept everything in one file since the project is small.

// ---------- Dark mode ----------
const darkModeBtn = document.getElementById("darkModeBtn");

// check if user had dark mode on before (using localStorage)
if (localStorage.getItem("darkMode") === "on") {
    document.body.classList.add("dark");
}

if (darkModeBtn) {
    darkModeBtn.addEventListener("click", function () {
        document.body.classList.toggle("dark");

        if (document.body.classList.contains("dark")) {
            localStorage.setItem("darkMode", "on");
        } else {
            localStorage.setItem("darkMode", "off");
        }
    });
}

// ---------- Predict form validation ----------
const predictForm = document.getElementById("predictForm");

if (predictForm) {
    predictForm.addEventListener("submit", function (e) {
        let valid = true;

        // simple helper to show/hide error text under a field
        function showError(fieldId, show) {
            const errorEl = document.getElementById(fieldId + "Error");
            if (errorEl) {
                errorEl.style.display = show ? "block" : "none";
            }
        }

        const name = document.getElementById("student_name").value.trim();
        const studyHours = parseFloat(document.getElementById("study_hours").value);
        const attendance = parseFloat(document.getElementById("attendance").value);
        const previousMarks = parseFloat(document.getElementById("previous_marks").value);
        const assignments = parseFloat(document.getElementById("assignments").value);
        const sleepHours = parseFloat(document.getElementById("sleep_hours").value);
        const internetStudy = parseFloat(document.getElementById("internet_study").value);

        if (name === "") {
            showError("student_name", true);
            valid = false;
        } else {
            showError("student_name", false);
        }

        if (isNaN(studyHours) || studyHours < 0 || studyHours > 24) {
            showError("study_hours", true);
            valid = false;
        } else {
            showError("study_hours", false);
        }

        if (isNaN(attendance) || attendance < 0 || attendance > 100) {
            showError("attendance", true);
            valid = false;
        } else {
            showError("attendance", false);
        }

        if (isNaN(previousMarks) || previousMarks < 0 || previousMarks > 100) {
            showError("previous_marks", true);
            valid = false;
        } else {
            showError("previous_marks", false);
        }

        if (isNaN(assignments) || assignments < 0 || assignments > 10) {
            showError("assignments", true);
            valid = false;
        } else {
            showError("assignments", false);
        }

        if (isNaN(sleepHours) || sleepHours < 0 || sleepHours > 24) {
            showError("sleep_hours", true);
            valid = false;
        } else {
            showError("sleep_hours", false);
        }

        if (isNaN(internetStudy) || internetStudy < 0 || internetStudy > 24) {
            showError("internet_study", true);
            valid = false;
        } else {
            showError("internet_study", false);
        }

        if (!valid) {
            e.preventDefault();
            return;
        }

        // show loading spinner while the form submits
        const spinner = document.getElementById("loadingSpinner");
        const submitBtn = document.getElementById("submitBtn");
        if (spinner) spinner.style.display = "block";
        if (submitBtn) submitBtn.innerText = "Predicting...";
    });
}

// ---------- Reset button ----------
const resetBtn = document.getElementById("resetBtn");
if (resetBtn) {
    resetBtn.addEventListener("click", function () {
        predictForm.reset();
    });
}

// ---------- Simple fade-in animation for cards ----------
window.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll(".card");
    cards.forEach(function (card, index) {
        card.style.opacity = "0";
        card.style.transform = "translateY(15px)";
        setTimeout(function () {
            card.style.transition = "opacity 0.5s ease, transform 0.5s ease";
            card.style.opacity = "1";
            card.style.transform = "translateY(0)";
        }, index * 80);
    });
});

// ---------- Download result as PDF ----------
// Using the browser's built-in print dialog as a simple "download as PDF" option.
function downloadResultAsPDF() {
    window.print();
}
