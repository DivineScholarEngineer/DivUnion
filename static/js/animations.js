// JavaScript to animate elements on scroll.
// Elements with the attribute data-animate will fade in when they
// enter the viewport.  Requires IntersectionObserver (supported in
// modern browsers).
document.addEventListener('DOMContentLoaded', function () {
    const elements = document.querySelectorAll('[data-animate]');
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    elements.forEach(el => observer.observe(el));
});
