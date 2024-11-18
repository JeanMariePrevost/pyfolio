document.addEventListener("DOMContentLoaded", () => {
  const slides = document.querySelectorAll(".carousel-slide");
  const prevButton = document.querySelector(".prev");
  const nextButton = document.querySelector(".next");

  let currentIndex = 0;

  function updateCarousel() {
    slides.forEach((slide) => {
      slide.style.transform = `translateX(${-100 * currentIndex}%)`;
    });
  }

  updateCarousel(); // Initialize the carousel position

  if (prevButton && nextButton) {
    prevButton.addEventListener("click", () => {
      currentIndex = (currentIndex - 1 + slides.length) % slides.length;
      updateCarousel();
    });

    nextButton.addEventListener("click", () => {
      currentIndex = (currentIndex + 1) % slides.length;
      updateCarousel();
    });
  } else {
    console.error("Carousel buttons not found in the DOM!");
  }
});
