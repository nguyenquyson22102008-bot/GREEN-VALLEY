const slides = [
  {
    title: "Khu Rừng Sinh Tồn",
    desc: "Người chơi thu thập tài nguyên và bảo vệ khu rừng khỏi quái vật tấn công.",
    tags: ["Survival", "Resource"],
    img: "photo/anh/game1.jpg"
  },
  {
    title: "Nông Trại Xanh",
    desc: "Trồng cây, chăm sóc mùa màng và phát triển nông trại theo phong cách riêng.",
    tags: ["Farming", "Build"],
    img: "photo/anh/game2.jpg"
  },
  {
    title: "Chiến Đấu FPS",
    desc: "Sử dụng nhiều loại vũ khí để tiêu diệt sinh vật nguy hiểm quanh thung lũng.",
    tags: ["FPS", "Combat"],
    img: "photo/anh/game3.jpg"
  },
  {
    title: "Bảo Vệ Thung Lũng",
    desc: "Bảo vệ GREEN VALLEY khỏi các đợt xâm chiếm và những boss mạnh.",
    tags: ["Defense", "Boss"],
    img: "photo/anh/game.jpg"
  }
];

function initSlider() {
  const slider = document.querySelector("[data-slider]");
  if (!slider) return;

  const image = document.getElementById("gv-slide-img");
  const number = document.getElementById("gv-num");
  const title = document.getElementById("gv-title");
  const desc = document.getElementById("gv-desc");
  const tags = document.getElementById("gv-tags");
  const dots = document.getElementById("gv-dots");
  let current = 0;
  let isChanging = false;

  function showSlide(index) {
    if (isChanging) return;
    isChanging = true;
    const next = (index + slides.length) % slides.length;
    image.classList.add("is-changing");

    window.setTimeout(() => {
      current = next;
      const slide = slides[current];
      image.style.backgroundImage = `url("${slide.img}")`;
      number.textContent = `${String(current + 1).padStart(2, "0")} / ${String(slides.length).padStart(2, "0")}`;
      title.textContent = slide.title;
      desc.textContent = slide.desc;
      tags.innerHTML = slide.tags.map((tag) => `<span>${tag}</span>`).join("");
      dots.querySelectorAll(".gv-dot").forEach((dot, dotIndex) => {
        dot.classList.toggle("active", dotIndex === current);
      });
      image.classList.remove("is-changing");
      isChanging = false;
    }, 140);
  }

  slides.forEach((_, index) => {
    const dot = document.createElement("button");
    dot.className = "gv-dot";
    dot.type = "button";
    dot.setAttribute("aria-label", `Xem ảnh ${index + 1}`);
    dot.addEventListener("click", () => showSlide(index));
    dots.appendChild(dot);
  });

  slider.querySelector("[data-slider-prev]").addEventListener("click", () => showSlide(current - 1));
  slider.querySelector("[data-slider-next]").addEventListener("click", () => showSlide(current + 1));
  const firstSlide = slides[0];
  image.style.backgroundImage = `url("${firstSlide.img}")`;
  tags.innerHTML = firstSlide.tags.map((tag) => `<span>${tag}</span>`).join("");
  dots.querySelector(".gv-dot").classList.add("active");
}

// Dùng cho trang loaicay.html (class .gv-crop-card)
function initCropFilters() {
  const buttons = document.querySelectorAll(".gv-filter-btn");
  if (!buttons.length) return;
  const cards = document.querySelectorAll(".gv-crop-card");
  if (!cards.length) return;

  const hideTimers = new WeakMap();

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.dataset.filter;
      buttons.forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      cards.forEach((card) => {
        const shouldHide = filter !== "all" && card.dataset.type !== filter;
        window.clearTimeout(hideTimers.get(card));
        if (shouldHide) {
          card.classList.add("is-hiding");
          const timer = window.setTimeout(() => {
            card.hidden = true;
          }, 180);
          hideTimers.set(card, timer);
        } else {
          card.hidden = false;
          window.requestAnimationFrame(() => {
            card.classList.remove("is-hiding");
          });
        }
      });
    });
  });
}

// FIX: Dùng cho trang dungcu.html (class .gv-tool-card)
function initToolFilters() {
  const buttons = document.querySelectorAll(".gv-filter-btn");
  if (!buttons.length) return;
  const cards = document.querySelectorAll(".gv-tool-card");
  if (!cards.length) return;

  const hideTimers = new WeakMap();

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.dataset.filter;
      buttons.forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      cards.forEach((card) => {
        const shouldHide = filter !== "all" && card.dataset.type !== filter;
        window.clearTimeout(hideTimers.get(card));
        if (shouldHide) {
          card.classList.add("is-hiding");
          const timer = window.setTimeout(() => {
            card.hidden = true;
          }, 180);
          hideTimers.set(card, timer);
        } else {
          card.hidden = false;
          window.requestAnimationFrame(() => {
            card.classList.remove("is-hiding");
          });
        }
      });
    });
  });
}

function initNotices() {
  const buttons = document.querySelectorAll("[data-notice]");
  if (!buttons.length) return;

  const toast = document.createElement("div");
  toast.className = "gv-toast";
  toast.setAttribute("role", "status");
  toast.setAttribute("aria-live", "polite");
  document.body.appendChild(toast);
  let timer;

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      window.clearTimeout(timer);
      toast.textContent = button.dataset.notice;
      toast.classList.add("is-visible");
      timer = window.setTimeout(() => {
        toast.classList.remove("is-visible");
      }, 2600);
    });
  });
}

const GOOGLE_SHEET_WEBHOOK_URL = "https://script.google.com/macros/s/YOUR_DEPLOYED_SCRIPT_ID/exec";

function initContactForm() {
  const form = document.querySelector("[data-contact-form]");
  if (!form) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const note = form.querySelector("[data-form-note]");
    const payload = {
      name: form.name.value.trim(),
      email: form.email.value.trim(),
      subject: form.subject.value.trim(),
      message: form.message.value.trim(),
      submittedAt: new Date().toISOString(),
      source: "lienhe"
    };

    if (GOOGLE_SHEET_WEBHOOK_URL.includes("YOUR_DEPLOYED_SCRIPT_ID")) {
      note.textContent = "Vui lòng cấu hình URL Google Sheets webhook trước khi lưu.";
      return;
    }

    try {
      const response = await fetch(GOOGLE_SHEET_WEBHOOK_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error("Không thể lưu dữ liệu vào Google Sheets");
      }

      const result = await response.json();
      if (result.status !== "success") {
        throw new Error(result.error || "Lỗi từ Google Apps Script");
      }

      note.textContent = "Cảm ơn bạn! Tin nhắn đã được lưu vào Google Sheets.";
      form.reset();
    } catch (error) {
      console.error(error);
      note.textContent = "Lưu thất bại. Vui lòng thử lại sau.";
    }
  });
}

function initMobileMenu() {
  document.querySelectorAll(".gv-nav").forEach((nav) => {
    const button = nav.querySelector(".gv-menu-toggle");
    if (!button) return;

    const closeMenu = () => {
      nav.classList.remove("menu-open");
      document.body.classList.remove("no-scroll");
      button.setAttribute("aria-expanded", "false");
      button.setAttribute("aria-label", "Mở menu");
    };

    button.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("menu-open");
      document.body.classList.toggle("no-scroll", isOpen && window.innerWidth <= 640);
      button.setAttribute("aria-expanded", String(isOpen));
      button.setAttribute("aria-label", isOpen ? "Đóng menu" : "Mở menu");
    });

    nav.querySelectorAll(".gv-nav-links a").forEach((link) => {
      link.addEventListener("click", closeMenu);
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > 640) closeMenu();
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeMenu();
    });

    document.addEventListener("click", (event) => {
      if (!nav.contains(event.target)) closeMenu();
    });
  });
}

function initDownload() {
  const downloadBtn = document.querySelector("[data-download]");
  if (!downloadBtn) return;

  downloadBtn.addEventListener("click", () => {
    const link = document.createElement("a");
    link.href = "downloads/1.jpg";
    link.download = "1.jpg";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    const toast = document.querySelector(".gv-toast") || document.createElement("div");
    if (!document.querySelector(".gv-toast")) {
      toast.className = "gv-toast";
      toast.setAttribute("role", "status");
      toast.setAttribute("aria-live", "polite");
      document.body.appendChild(toast);
    }
    toast.textContent = "Đang tải xuống...";
    toast.classList.add("is-visible");
    setTimeout(() => {
      toast.classList.remove("is-visible");
    }, 2600);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initMobileMenu();
  initNotices();
  initSlider();
  initCropFilters();  // cho loaicay.html
  initToolFilters();  // cho dungcu.html — FIX
  initContactForm();
  initDownload();
});