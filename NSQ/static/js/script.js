const slides = [
  {
    title: "Khu Rừng Sinh Tồn",
    desc: "Người chơi thu thập tài nguyên và bảo vệ khu rừng khỏi quái vật tấn công.",
    tags: ["Survival", "Resource"],
    img: "/photo/anh/game1.jpg"
  },
  {
    title: "Nông Trại Xanh",
    desc: "Trồng cây, chăm sóc mùa màng và phát triển nông trại theo phong cách riêng.",
    tags: ["Farming", "Build"],
    img: "/photo/anh/game2.jpg"
  },
  {
    title: "Chiến Đấu FPS",
    desc: "Sử dụng nhiều loại vũ khí để tiêu diệt sinh vật nguy hiểm quanh thung lũng.",
    tags: ["FPS", "Combat"],
    img: "/photo/anh/game3.jpg"
  },
  {
    title: "Bảo Vệ Thung Lũng",
    desc: "Bảo vệ GREEN VALLEY khỏi các đợt xâm chiếm và những boss mạnh.",
    tags: ["Defense", "Boss"],
    img: "/photo/anh/game.jpg"
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
  const prevButton = slider.querySelector("[data-slider-prev]");
  const nextButton = slider.querySelector("[data-slider-next]");

  if (!image || !number || !title || !desc || !tags || !dots || !prevButton || !nextButton) return;

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

  prevButton.addEventListener("click", () => showSlide(current - 1));
  nextButton.addEventListener("click", () => showSlide(current + 1));
  const firstSlide = slides[0];
  image.style.backgroundImage = `url("${firstSlide.img}")`;
  tags.innerHTML = firstSlide.tags.map((tag) => `<span>${tag}</span>`).join("");
  dots.querySelector(".gv-dot").classList.add("active");
}

// ĐÃ SỬA: Dùng cho trang loaicay.html (class .gv-crop-card)
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
            card.style.display = "none"; // Ẩn hoàn toàn khỏi layout sau khi mờ dần
          }, 220); // Khớp chuẩn với thời gian transition .22s trong CSS
          hideTimers.set(card, timer);
        } else {
          card.style.display = ""; // Hiển thị lại thẻ card trước
          card.hidden = false;
          void card.offsetHeight; // Ép trình duyệt tính toán lại layout để kích hoạt hiệu ứng fade-in mượt mà
          card.classList.remove("is-hiding");
        }
      });
    });
  });
}

// ĐÃ SỬA: Dùng cho trang dungcu.html (class .gv-tool-card)
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
            card.style.display = "none";
          }, 220);
          hideTimers.set(card, timer);
        } else {
          card.style.display = "";
          card.hidden = false;
          void card.offsetHeight;
          card.classList.remove("is-hiding");
        }
      });
    });
  });
}

// ĐÃ SỬA: Dùng cho trang thú nuôi/động vật nếu có
function initAnimalFilters() {
  const buttons = document.querySelectorAll(".gv-filter-btn");
  if (!buttons.length) return;
  const cards = document.querySelectorAll(".gv-animal-card");
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
            card.style.display = "none";
          }, 220);
          hideTimers.set(card, timer);
        } else {
          card.style.display = "";
          card.hidden = false;
          void card.offsetHeight;
          card.classList.remove("is-hiding");
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

function initContactForm() {
  const form = document.querySelector("[data-contact-form]");
  if (!form) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const note = form.querySelector("[data-form-note]");
    const formData = new FormData(form);
    const payload = {
      name: String(formData.get("name") || "").trim(),
      email: String(formData.get("email") || "").trim(),
      subject: String(formData.get("subject") || "").trim(),
      message: String(formData.get("message") || "").trim()
    };

    if (!payload.name || !payload.email || !payload.subject || !payload.message) {
      note.textContent = "Vui lòng nhập đầy đủ thông tin trước khi gửi.";
      return;
    }

    try {
      note.textContent = "Đang gửi tin nhắn...";
      const response = await fetch("/api/contact", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      const result = await response.json();
      if (!response.ok || !result.success) {
        throw new Error(result.message || "Không thể gửi tin nhắn");
      }

      note.textContent = result.message || "Cảm ơn bạn! Tin nhắn đã được gửi.";
      form.reset();
    } catch (error) {
      console.error(error);
      note.textContent = error.message || "Gửi thất bại. Vui lòng thử lại sau.";
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

function initLogoutButton() {
  document.querySelectorAll(".gv-nav-links").forEach((links) => {
    let link = links.querySelector('a[href="/logout"], [data-logout]');

    if (!link) {
      const item = document.createElement("li");
      link = document.createElement("a");
      link.href = "/logout";
      link.innerHTML = '<i class="ti ti-logout" aria-hidden="true"></i><span>Đăng xuất</span>';
      item.appendChild(link);
      links.appendChild(item);
    }

    link.classList.add("gv-logout-link");
    link.dataset.logout = "true";
    if (!link.querySelector("span")) {
      link.innerHTML = '<i class="ti ti-logout" aria-hidden="true"></i><span>Đăng xuất</span>';
    }

    if (link.dataset.logoutBound === "true") return;
    link.dataset.logoutBound = "true";

    link.addEventListener("click", (event) => {
      event.preventDefault();
      localStorage.removeItem("auth_user");
      sessionStorage.removeItem("auth_user");
      window.location.href = "/logout";
    });
  });
}

function initBackButtonAuthGuard() {
  window.addEventListener("pageshow", (event) => {
    if (event.persisted) {
      window.location.reload();
    }
  });
}

function initDownload() {
  const downloadBtn = document.querySelector("[data-download]");
  if (!downloadBtn) return;

  downloadBtn.addEventListener("click", () => {
    const link = document.createElement("a");
    link.href = "/downloads/Game.rar";
    link.download = "Game.rar";
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
  initBackButtonAuthGuard();
  initLogoutButton();
  initMobileMenu();
  initNotices();
  initSlider();
  initCropFilters();  // cho loaicay.html
  initToolFilters();  // cho dungcu.html — FIX
  initAnimalFilters();
  initContactForm();
  initDownload();
});
