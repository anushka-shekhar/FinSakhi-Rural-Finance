/**
 * FinSakhi - Main Client-Side JavaScript
 * Mobile menu toggle, notification auto-dismiss, and form helpers.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Menu Toggle
    const toggleBtn = document.querySelector('.mobile-nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (toggleBtn && navLinks) {
        toggleBtn.addEventListener('click', () => {
            navLinks.classList.toggle('show');
            const isExpanded = navLinks.classList.contains('show');
            toggleBtn.setAttribute('aria-expanded', isExpanded);
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
