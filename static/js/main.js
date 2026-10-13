/**
 * FinSakhi - Main Client-Side JavaScript
 * Mobile menu toggle, notification auto-dismiss, and form helpers.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Menu Toggle
    const toggleBtn = document.querySelector('.mobile-nav-toggle');
    const navWrapper = document.querySelector('.nav-links-wrapper');

    if (toggleBtn && navWrapper) {
        toggleBtn.addEventListener('click', () => {
            navWrapper.classList.toggle('show');
            const isExpanded = navWrapper.classList.contains('show');
            toggleBtn.setAttribute('aria-expanded', isExpanded);
        });

        // Close nav when a link inside it is clicked (SPA-style navigation)
        navWrapper.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navWrapper.classList.remove('show');
                toggleBtn.setAttribute('aria-expanded', 'false');
            });
        });
    }

    // 2. Auto Dismiss Flash Alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // 3. Indian Mobile Number Filter (Allows only digits, max 10)
    const mobileInputs = document.querySelectorAll('input[name="mobile_number"]');
    mobileInputs.forEach(input => {
        input.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '').slice(0, 10);
        });
    });
});
