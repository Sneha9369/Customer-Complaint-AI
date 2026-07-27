/* =========================================================
   SMARTCOMPLAINT AI
   MAIN JAVASCRIPT
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    console.log("SmartComplaint AI loaded successfully 🚀");

    initializeFlashMessages();
    initializeComplaintForm();
    initializeTrackingForm();
    initializeAdminForms();
    initializePasswordValidation();
    initializePasswordToggle();
    initializeNavbar();
    initializeCards();
    initializeBackButtons();
});


/* =========================================================
   FLASH MESSAGE AUTO HIDE
   ========================================================= */

function initializeFlashMessages() {

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        setTimeout(function () {

            alert.style.transition =
                "opacity 0.4s ease, transform 0.4s ease";

            alert.style.opacity = "0";
            alert.style.transform = "translateY(-8px)";

            setTimeout(function () {
                alert.remove();
            }, 400);

        }, 4500);

    });
}


/* =========================================================
   SHOW FRONTEND MESSAGE
   ========================================================= */

function showMessage(message, type = "success") {

    const oldAlert =
        document.querySelector(".javascript-alert");

    if (oldAlert) {
        oldAlert.remove();
    }

    const alert = document.createElement("div");

    alert.className =
        "alert alert-" +
        type +
        " javascript-alert";

    alert.innerText = message;

    const form =
        document.querySelector("form");

    if (form && form.parentNode) {

        form.parentNode.insertBefore(
            alert,
            form
        );

    } else {

        document.body.prepend(alert);
    }


    setTimeout(function () {

        alert.style.transition =
            "opacity .4s ease, transform .4s ease";

        alert.style.opacity = "0";
        alert.style.transform = "translateY(-6px)";

        setTimeout(function () {
            alert.remove();
        }, 400);

    }, 4000);
}


/* =========================================================
   COMPLAINT SUBMISSION FORM
   ========================================================= */

function initializeComplaintForm() {

    const complaintForm =
        document.querySelector(
            'form[action*="submit-complaint"]'
        );

    if (!complaintForm) {
        return;
    }


    complaintForm.addEventListener(
        "submit",
        function (event) {

            const subject =
                complaintForm.querySelector(
                    'input[name="subject"]'
                );

            const description =
                complaintForm.querySelector(
                    'textarea[name="description"]'
                );


            if (!subject || !description) {
                return;
            }


            /* SUBJECT VALIDATION */

            if (subject.value.trim().length < 3) {

                event.preventDefault();

                showMessage(
                    "Please enter a valid complaint subject.",
                    "danger"
                );

                subject.focus();

                return;
            }


            /* DESCRIPTION VALIDATION */

            if (description.value.trim().length < 10) {

                event.preventDefault();

                showMessage(
                    "Complaint description must contain at least 10 characters.",
                    "danger"
                );

                description.focus();

                return;
            }


            /* BUTTON LOADING */

            const button =
                complaintForm.querySelector(
                    'button[type="submit"]'
                );

            if (button) {

                button.disabled = true;

                button.dataset.originalText =
                    button.innerHTML;

                button.innerHTML =
                    '<span class="button-loader"></span> Analyzing Complaint...';
            }

        }
    );
}


/* =========================================================
   COMPLAINT CHARACTER COUNTER
   ========================================================= */

document.addEventListener(
    "input",
    function (event) {

        if (
            event.target.matches(
                'textarea[name="description"]'
            )
        ) {

            const textarea = event.target;

            let counter =
                document.querySelector(
                    ".description-counter"
                );


            if (!counter) {

                counter =
                    document.createElement("small");

                counter.className =
                    "description-counter";

                textarea.insertAdjacentElement(
                    "afterend",
                    counter
                );
            }


            const length =
                textarea.value.length;

            counter.innerText =
                length + " characters";


            if (length < 10) {

                counter.style.color =
                    "#d45b5b";

            } else {

                counter.style.color =
                    "#55a778";
            }

        }

    }
);


/* =========================================================
   TRACK COMPLAINT FORM
   ========================================================= */

function initializeTrackingForm() {

    const trackingForm =
        document.querySelector(
            ".tracking-form"
        );

    if (!trackingForm) {
        return;
    }


    trackingForm.addEventListener(
        "submit",
        function (event) {

            const input =
                trackingForm.querySelector(
                    'input[name="complaint_id"]'
                );

            if (!input) {
                return;
            }


            let complaintId =
                input.value
                    .trim()
                    .toUpperCase();


            input.value =
                complaintId;


            if (!complaintId) {

                event.preventDefault();

                showMessage(
                    "Please enter your Complaint ID.",
                    "danger"
                );

                input.focus();

                return;
            }


            if (
                !complaintId.startsWith("CMP-")
            ) {

                event.preventDefault();

                showMessage(
                    "Complaint ID should start with CMP-",
                    "warning"
                );

                input.focus();

                return;
            }


            const button =
                trackingForm.querySelector(
                    'button[type="submit"]'
                );

            if (button) {

                button.disabled = true;
                button.innerText =
                    "Searching...";
            }

        }
    );
}


/* =========================================================
   ADMIN FORMS
   ========================================================= */

function initializeAdminForms() {

    /* -------------------------
       UPDATE COMPLAINT
       ------------------------- */

    const updateForms =
        document.querySelectorAll(
            ".admin-update-form"
        );


    updateForms.forEach(
        function (form) {

            form.addEventListener(
                "submit",
                function (event) {

                    const status =
                        form.querySelector(
                            'select[name="status"]'
                        );


                    if (!status) {
                        return;
                    }


                    if (
                        status.value ===
                        "Resolved"
                    ) {

                        const confirmed =
                            confirm(
                                "Are you sure you want to mark this complaint as Resolved?"
                            );


                        if (!confirmed) {

                            event.preventDefault();

                            return;
                        }

                    }


                    const button =
                        form.querySelector(
                            'button[type="submit"]'
                        );


                    if (button) {

                        button.disabled =
                            true;

                        button.innerText =
                            "Saving...";
                    }

                }
            );

        }
    );


    /* -------------------------
       ASSIGN EMPLOYEE
       ------------------------- */

    const assignForms =
        document.querySelectorAll(
            ".assign-form"
        );


    assignForms.forEach(
        function (form) {

            form.addEventListener(
                "submit",
                function (event) {

                    const employee =
                        form.querySelector(
                            'select[name="employee_id"]'
                        );


                    if (
                        !employee ||
                        employee.value === ""
                    ) {

                        event.preventDefault();

                        showMessage(
                            "Please select an employee.",
                            "warning"
                        );

                        return;
                    }


                    const selectedEmployee =
                        employee.options[
                            employee.selectedIndex
                        ].text;


                    const confirmed =
                        confirm(
                            "Assign complaint to " +
                            selectedEmployee +
                            "?"
                        );


                    if (!confirmed) {

                        event.preventDefault();

                        return;
                    }


                    const button =
                        form.querySelector(
                            'button[type="submit"]'
                        );


                    if (button) {

                        button.disabled =
                            true;

                        button.innerText =
                            "Assigning...";
                    }

                }
            );

        }
    );
}


/* =========================================================
   REGISTER PASSWORD VALIDATION
   ========================================================= */

function initializePasswordValidation() {

    const password =
        document.querySelector(
            'input[name="password"]'
        );

    const confirmPassword =
        document.querySelector(
            'input[name="confirm_password"]'
        );


    if (
        !password ||
        !confirmPassword
    ) {
        return;
    }


    /* PASSWORD MATCH */

    confirmPassword.addEventListener(
        "input",
        function () {

            if (
                confirmPassword.value !== "" &&
                password.value !==
                confirmPassword.value
            ) {

                confirmPassword.style.borderColor =
                    "#d85a5a";

            } else if (
                confirmPassword.value !== ""
            ) {

                confirmPassword.style.borderColor =
                    "#55a778";

            } else {

                confirmPassword.style.borderColor =
                    "#e1e1e8";
            }

        }
    );


    /* FORM VALIDATION */

    const registerForm =
        confirmPassword.closest(
            "form"
        );


    if (!registerForm) {
        return;
    }


    registerForm.addEventListener(
        "submit",
        function (event) {

            if (
                password.value.length < 6
            ) {

                event.preventDefault();

                showMessage(
                    "Password must contain at least 6 characters.",
                    "warning"
                );

                password.focus();

                return;
            }


            if (
                password.value !==
                confirmPassword.value
            ) {

                event.preventDefault();

                showMessage(
                    "Password and Confirm Password do not match.",
                    "danger"
                );

                confirmPassword.focus();

                return;
            }

        }
    );
}


/* =========================================================
   PASSWORD SHOW / HIDE
   ========================================================= */

function initializePasswordToggle() {

    const toggleButtons =
        document.querySelectorAll(
            ".password-toggle"
        );


    toggleButtons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function (event) {

                    event.preventDefault();

                    const container =
                        button.closest(
                            ".input-container"
                        );


                    let input = null;


                    if (container) {

                        input =
                            container.querySelector(
                                'input[type="password"], input[data-password]'
                            );

                    }


                    /* LOGIN PAGE FALLBACK */

                    if (!input) {

                        input =
                            document.getElementById(
                                "loginPassword"
                            );
                    }


                    if (!input) {
                        return;
                    }


                    if (
                        input.type ===
                        "password"
                    ) {

                        input.type =
                            "text";

                        button.innerText =
                            "Hide";

                    } else {

                        input.type =
                            "password";

                        button.innerText =
                            "Show";
                    }

                }
            );

        }
    );
}


/* =========================================================
   OLD LOGIN FUNCTION SUPPORT
   ========================================================= */

function toggleLoginPassword() {

    const passwordInput =
        document.getElementById(
            "loginPassword"
        );

    const button =
        document.querySelector(
            ".password-toggle"
        );


    if (
        !passwordInput ||
        !button
    ) {
        return;
    }


    if (
        passwordInput.type ===
        "password"
    ) {

        passwordInput.type =
            "text";

        button.innerText =
            "Hide";

    } else {

        passwordInput.type =
            "password";

        button.innerText =
            "Show";
    }
}


/* =========================================================
   NAVBAR SCROLL EFFECT
   ========================================================= */

function initializeNavbar() {

    const navbar =
        document.querySelector(
            ".navbar"
        );


    if (!navbar) {
        return;
    }


    window.addEventListener(
        "scroll",
        function () {

            if (
                window.scrollY > 20
            ) {

                navbar.style.boxShadow =
                    "0 10px 30px rgba(40,40,70,0.08)";

            } else {

                navbar.style.boxShadow =
                    "none";
            }

        }
    );
}


/* =========================================================
   DASHBOARD CARD ANIMATION
   ========================================================= */

function initializeCards() {

    const cards =
        document.querySelectorAll(
            `
            .stat-card,
            .admin-stat-card,
            .action-card,
            .chart-card,
            .admin-complaint-card,
            .recent-complaint-card
            `
        );


    cards.forEach(
        function (card, index) {

            card.style.opacity =
                "0";

            card.style.transform =
                "translateY(10px)";


            setTimeout(
                function () {

                    card.style.transition =
                        "opacity .35s ease, transform .35s ease";

                    card.style.opacity =
                        "1";

                    card.style.transform =
                        "translateY(0)";

                },

                index * 40
            );

        }
    );
}


/* =========================================================
   BACK BUTTON
   ========================================================= */

function initializeBackButtons() {

    const buttons =
        document.querySelectorAll(
            "[data-back-button]"
        );


    buttons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function (event) {

                    event.preventDefault();

                    if (
                        window.history.length > 1
                    ) {

                        window.history.back();

                    } else {

                        window.location.href =
                            "/";
                    }

                }
            );

        }
    );
}


/* =========================================================
   PREVENT MULTIPLE BUTTON CLICKS
   ========================================================= */

document.addEventListener(
    "click",
    function (event) {

        const button =
            event.target.closest(
                "button"
            );


        if (!button) {
            return;
        }


        if (button.disabled) {

            event.preventDefault();

            event.stopPropagation();
        }

    }
);


/* =========================================================
   AUTO UPPERCASE COMPLAINT ID
   ========================================================= */

document.addEventListener(
    "input",
    function (event) {

        if (
            event.target.matches(
                'input[name="complaint_id"]'
            )
        ) {

            event.target.value =
                event.target.value
                    .toUpperCase();
        }

    }
);


/* =========================================================
   SMOOTH SCROLL
   ========================================================= */

document.querySelectorAll(
    'a[href^="#"]'
).forEach(
    function (link) {

        link.addEventListener(
            "click",
            function (event) {

                const target =
                    document.querySelector(
                        this.getAttribute(
                            "href"
                        )
                    );


                if (!target) {
                    return;
                }


                event.preventDefault();


                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            }
        );

    }
);