/* ========================================================
   IRRI — Animation Layer
   Uses Motion (formerly Framer Motion) via CDN
   Patterns adapted from 21st.dev hero components
   ======================================================== */

import {
  animate,
  inView,
  scroll,
} from "https://cdn.jsdelivr.net/npm/motion@12.38.0/+esm";

/* ─── stagger — not exported by this CDN bundle, polyfilled ── */
function stagger(duration, { start = 0 } = {}) {
  return (index) => start + index * duration;
}

/* ─── Easing ──────────────────────────────────────────── */
const EASE_OUT  = [0.16, 1, 0.3, 1];   // expo-out — smooth deceleration
const EASE_IN   = [0.7, 0, 0.84, 0];   // expo-in  — for exits

/* ─── Reduced motion ──────────────────────────────────── */
const noMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

/* ══════════════════════════════════════════════════════
   1. NAV — transparent → navy on scroll
   ══════════════════════════════════════════════════════ */
(function initNav() {
  const nav = document.querySelector(".nav");
  if (!nav) return;

  const threshold = 48;

  function update() {
    if (window.scrollY > threshold) {
      nav.classList.add("scrolled");
    } else {
      nav.classList.remove("scrolled");
    }
  }

  window.addEventListener("scroll", update, { passive: true });
  update();
})();

/* ══════════════════════════════════════════════════════
   2. MOBILE MENU — hamburger toggle
   ══════════════════════════════════════════════════════ */
(function initMobileMenu() {
  const toggle = document.querySelector(".mobile-toggle");
  const menu   = document.querySelector(".mobile-menu");
  if (!toggle || !menu) return;

  function open() {
    menu.classList.add("open");
    toggle.classList.add("open");
    toggle.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";

    if (!noMotion) {
      const links = menu.querySelectorAll("a");
      animate(
        links,
        { opacity: [0, 1], y: [20, 0] },
        { delay: stagger(0.07, { start: 0.1 }), duration: 0.45, easing: EASE_OUT }
      );
    }
  }

  function close() {
    menu.classList.remove("open");
    toggle.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  }

  toggle.addEventListener("click", () => {
    if (menu.classList.contains("open")) close(); else open();
  });

  // Close on any menu link click
  menu.querySelectorAll("a").forEach(a => a.addEventListener("click", close));

  // Close on Escape
  document.addEventListener("keydown", e => {
    if (e.key === "Escape" && menu.classList.contains("open")) close();
  });
})();

/* ══════════════════════════════════════════════════════
   3. HERO WORD-BY-WORD ENTRANCE (21st.dev pattern)
      Adapted from animated-hero-section-ui.tsx —
      each word blurs in and rises, staggered 100ms
   ══════════════════════════════════════════════════════ */
(function initHeroWordEntrance() {
  try {
  const h1 = document.querySelector(".hero h1[data-word-animate]");
  if (!h1) return;

  // Split the h1 into word spans, preserving <em> wrappers
  const rawHTML  = h1.innerHTML;
  const fragment = document.createRange().createContextualFragment(rawHTML);
  const words    = [];

  function wrapTextNodes(node) {
    if (node.nodeType === Node.TEXT_NODE) {
      const text = node.textContent;
      const parts = text.split(/(\s+)/);
      const container = document.createDocumentFragment();

      parts.forEach(part => {
        if (/^\s+$/.test(part)) {
          container.appendChild(document.createTextNode(part));
        } else if (part) {
          const span = document.createElement("span");
          span.className = "hero-word";
          span.textContent = part;
          span.style.cssText = "display:inline-block;";
          words.push(span);
          container.appendChild(span);
        }
      });

      node.parentNode.replaceChild(container, node);
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      // Wrap the entire <em> block as one unit
      if (node.tagName === "EM") {
        const span = document.createElement("span");
        span.className = "hero-word";
        span.style.cssText = "display:inline-block;";
        span.appendChild(node.cloneNode(true));
        words.push(span);
        node.parentNode.replaceChild(span, node);
      } else {
        Array.from(node.childNodes).forEach(wrapTextNodes);
      }
    }
  }

  Array.from(fragment.childNodes).forEach(wrapTextNodes);
  h1.innerHTML = "";
  h1.appendChild(fragment);

  if (noMotion) {
    // Instant reveal — CSS handles opacity: 1 via heroFadeUp if motion disabled
    words.forEach(w => { w.style.opacity = "1"; w.style.filter = "none"; });
    return;
  }

  // Set initial state: invisible
  words.forEach(w => {
    w.style.opacity  = "0";
    w.style.filter   = "blur(6px)";
    w.style.transform = "translateY(10px)";
  });

  // Override the CSS animation on h1 — we handle it via JS
  h1.style.opacity   = "1";
  h1.style.animation = "none";

  // Animate in
  animate(
    words,
    {
      opacity: [0, 1],
      filter:  ["blur(6px)", "blur(0px)"],
      y:       [10, 0],
    },
    {
      delay:    stagger(0.08, { start: 0.5 }),
      duration: 0.45,
      easing:   EASE_OUT,
    }
  );
  } catch (e) {
    // If word-splitting fails, fall back to showing the h1 instantly
    const h1 = document.querySelector(".hero h1[data-word-animate]");
    if (h1) { h1.style.opacity = "1"; h1.style.animation = "none"; }
  }
})();

/* ══════════════════════════════════════════════════════
   4. HERO PARALLAX — subtle background depth
   ══════════════════════════════════════════════════════ */
(function initHeroParallax() {
  const bg = document.querySelector(".hero-bg");
  if (!bg || noMotion) return;

  scroll(
    (progress) => {
      bg.style.transform = `translateY(${progress * 200}px)`;
    },
    { target: document.querySelector(".hero"), offset: ["start start", "end start"] }
  );
})();

/* ══════════════════════════════════════════════════════
   5. SCROLL REVEAL — IntersectionObserver via Motion inView
      Activates .reveal → .visible on every section element
   ══════════════════════════════════════════════════════ */
(function initScrollReveal() {
  if (noMotion) {
    document.querySelectorAll(".reveal").forEach(el => {
      el.style.opacity  = "1";
      el.style.transform = "none";
    });
    return;
  }

  inView(
    ".reveal",
    (element) => {
      // This version of inView passes (element, ioEntry) — first arg is the element
      element.classList.add("visible");
      // Don't disconnect — allows re-entry animation if user scrolls back
      return () => {};
    },
    { margin: "-60px 0px -60px 0px", amount: 0.15 }
  );
})();

/* ══════════════════════════════════════════════════════
   6. IMPACT COUNTERS — animate numbers on scroll
      Numbers should be integers in data-count attribute
   ══════════════════════════════════════════════════════ */
(function initCounters() {
  const items = document.querySelectorAll(".impact-num[data-count], .stat-num[data-count]");
  if (!items.length) return;

  items.forEach(el => {
    const target = parseInt(el.getAttribute("data-count"), 10);
    const suffix = el.getAttribute("data-suffix") || "";
    let animated = false;

    inView(
      el,
      () => {
        if (animated) return;
        animated = true;

        if (noMotion) {
          el.textContent = target.toLocaleString() + suffix;
          return;
        }

        animate(
          (progress) => {
            const val = Math.round(progress * target);
            el.textContent = val.toLocaleString() + suffix;
          },
          { duration: 1.8, easing: EASE_OUT }
        );
      },
      { amount: 0.5 }
    );
  });
})();

/* ══════════════════════════════════════════════════════
   7. NAV ACTIVE STATE — highlight current page link
   ══════════════════════════════════════════════════════ */
(function initNavActive() {
  const links = document.querySelectorAll(".nav-links a");
  if (!links.length) return;

  const current = location.pathname.split("/").pop() || "index.html";

  links.forEach(link => {
    const href = link.getAttribute("href") || "";
    const page = href.split("/").pop();
    if (page === current || (current === "" && page === "index.html")) {
      link.classList.add("active");
    }
  });
})();

/* ══════════════════════════════════════════════════════
   8. PARTNER / TRUST STRIP — infinite horizontal scroll
      Adapted from hero-section-5.tsx InfiniteSlider concept
      Works on .trust-track elements if present
   ══════════════════════════════════════════════════════ */
(function initTrustSlider() {
  const track = document.querySelector(".trust-track");
  if (!track || noMotion) return;

  const items = Array.from(track.children);
  if (!items.length) return;

  // Duplicate items for seamless loop
  items.forEach(item => {
    const clone = item.cloneNode(true);
    clone.setAttribute("aria-hidden", "true");
    track.appendChild(clone);
  });

  const totalWidth = track.scrollWidth / 2;

  const sliderAnim = animate(
    track,
    { x: [0, -totalWidth] },
    {
      duration:   28,
      easing:     "linear",
      repeat:     Infinity,
    }
  );

  // Pause on hover — use Motion animation ref, not Web Animations API
  track.addEventListener("mouseenter", () => sliderAnim.pause());
  track.addEventListener("mouseleave", () => sliderAnim.play());
})();
