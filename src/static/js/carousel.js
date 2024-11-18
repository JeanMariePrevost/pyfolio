document.addEventListener("DOMContentLoaded", () => {
  const track = document.querySelector(".carousel-track");
  const slides = Array.from(document.querySelectorAll(".carousel-slide"));
  const prevButton = document.querySelector(".prev");
  const nextButton = document.querySelector(".next");
  const indicatorsContainer = document.querySelector(".carousel-indicators");
  const carousel = document.querySelector(".carousel");

  let currentIndex = 1;
  let autoPlayInterval;

  const autoPlayDelay = 3000; // Time between slides in milliseconds

  // Initialize clones (from earlier improvement)
  const firstClone = slides[0].cloneNode(true);
  const lastClone = slides[slides.length - 1].cloneNode(true);

  track.appendChild(firstClone);
  track.insertBefore(lastClone, slides[0]);

  const updatedSlides = Array.from(track.children);
  const slideWidth = slides[0].getBoundingClientRect().width;

  // Generate indicators (from earlier improvement)
  slides.forEach((_, i) => {
    const dot = document.createElement("button");
    dot.dataset.index = i + 1;
    indicatorsContainer.appendChild(dot);
  });

  const dots = Array.from(indicatorsContainer.children);
  dots[0].classList.add("active");

  function updateCarousel() {
    track.style.transition = "transform 0.5s ease-in-out";
    track.style.transform = `translateX(${-slideWidth * currentIndex}px)`;
    updateDots();
  }

  function updateDots() {
    dots.forEach((dot) => dot.classList.remove("active"));
    if (currentIndex === 0) {
      dots[dots.length - 1].classList.add("active");
    } else if (currentIndex === updatedSlides.length - 1) {
      dots[0].classList.add("active");
    } else {
      dots[currentIndex - 1].classList.add("active");
    }
  }

  function handleTransitionEnd() {
    if (updatedSlides[currentIndex] === firstClone) {
      track.style.transition = "none";
      currentIndex = 1;
      track.style.transform = `translateX(${-slideWidth * currentIndex}px)`;
    }

    if (updatedSlides[currentIndex] === lastClone) {
      track.style.transition = "none";
      currentIndex = updatedSlides.length - 2;
      track.style.transform = `translateX(${-slideWidth * currentIndex}px)`;
    }
  }

  // Auto-play functionality
  function startAutoPlay() {
    autoPlayInterval = setInterval(() => {
      currentIndex = (currentIndex + 1) % updatedSlides.length;
      updateCarousel();
    }, autoPlayDelay);
  }

  function stopAutoPlay() {
    clearInterval(autoPlayInterval);
  }

  // Attach events for hover pause
  carousel.addEventListener("mouseenter", stopAutoPlay);
  carousel.addEventListener("mouseleave", startAutoPlay);

  // Button and dot functionality
  prevButton.addEventListener("click", () => {
    currentIndex = (currentIndex - 1 + updatedSlides.length) % updatedSlides.length;
    updateCarousel();
  });

  nextButton.addEventListener("click", () => {
    currentIndex = (currentIndex + 1) % updatedSlides.length;
    updateCarousel();
  });

  dots.forEach((dot) => {
    dot.addEventListener("click", (e) => {
      const index = Number(e.target.dataset.index);
      currentIndex = index;
      updateCarousel();
    });
  });

  // Start auto-play on page load
  startAutoPlay();

  // Initialize position
  track.style.transform = `translateX(${-slideWidth * currentIndex}px)`;
  track.addEventListener("transitionend", handleTransitionEnd);
});
