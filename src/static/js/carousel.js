document.addEventListener("DOMContentLoaded", () => {
  const track = document.querySelector(".carousel-track");
  const slides = Array.from(document.querySelectorAll(".carousel-slide"));
  const prevButton = document.querySelector(".prev");
  const nextButton = document.querySelector(".next");

  let currentIndex = 1;

  // Clone first and last slides, letting you loop through seamlessly
  const firstClone = slides[0].cloneNode(true);
  const lastClone = slides[slides.length - 1].cloneNode(true);

  track.appendChild(firstClone);
  track.insertBefore(lastClone, slides[0]);

  const updatedSlides = Array.from(track.children);
  const slideWidth = slides[0].getBoundingClientRect().width;

  // Initialize track position
  track.style.transform = `translateX(${-slideWidth * currentIndex}px)`;

  function updateCarousel() {
    track.style.transition = "transform 0.5s ease-in-out";
    track.style.transform = `translateX(${-slideWidth * currentIndex}px)`;
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

  track.addEventListener("transitionend", handleTransitionEnd);

  prevButton.addEventListener("click", () => {
    currentIndex = (currentIndex - 1 + updatedSlides.length) % updatedSlides.length;
    updateCarousel();
  });

  nextButton.addEventListener("click", () => {
    currentIndex = (currentIndex + 1) % updatedSlides.length;
    updateCarousel();
  });
});
