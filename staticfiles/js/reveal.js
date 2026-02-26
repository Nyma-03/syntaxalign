(() => {
    const revealItems = document.querySelectorAll(
        ".product-card, .detail-grid, .hero-panel, .highlight-card, .cta-card"
    );

    if (revealItems.length === 0) {
        return;
    }

    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    if (prefersReducedMotion.matches) {
        revealItems.forEach((item) => item.classList.add("is-visible"));
        return;
    }

    const observer = new IntersectionObserver(
        (entries, obs) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    obs.unobserve(entry.target);
                }
            });
        },
        {
            threshold: 0.15,
            rootMargin: "0px 0px -40px 0px",
        }
    );

    revealItems.forEach((item, index) => {
        item.classList.add("reveal");
        item.style.setProperty("--delay", `${index * 80}ms`);
        observer.observe(item);
    });
})();
