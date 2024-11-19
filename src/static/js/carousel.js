document.addEventListener("DOMContentLoaded", () => {
  const track = document.querySelector(".carousel-track");
  const realSlides = Array.from(document.querySelectorAll(".carousel-slide"));
  const prevButton = document.querySelector(".prev");
  const nextButton = document.querySelector(".next");
  const indicatorsContainer = document.querySelector(".carousel-indicators");
  const carousel = document.querySelector(".carousel");

  let currentIndex = 1;
  let autoPlayInterval;

  const autoPlayDelay = 3000; // Time between slides in milliseconds
  const defaultTransition = track.style.transition; // Store the CSS transition effect

  // Clone slides to create infinite loop effect
  const numberOfClonesOnEachSide = 2;
  for (let i = 0; i < numberOfClonesOnEachSide; i++) {
    const cloneFromStart = realSlides[i].cloneNode(true);
    const cloneFromEnd = realSlides[realSlides.length - 1 - i].cloneNode(true);

    track.appendChild(cloneFromStart);
    track.insertBefore(cloneFromEnd, track.firstChild);
  }

  const slidesWithClones = Array.from(track.children);
  const slideWidth = realSlides[0].getBoundingClientRect().width;

  // Generate indicators (from earlier improvement)
  realSlides.forEach((_, i) => {
    const dot = document.createElement("button");
    dot.dataset.index = i + 1;
    indicatorsContainer.appendChild(dot);
  });

  const dots = Array.from(indicatorsContainer.children);
  dots[0].classList.add("active");

  function updateCarousel(instant = false) {
    console.log("currentIndex", currentIndex);
    if (instant) {
      track.style.transition = "none";
    } else {
      track.style.transition = defaultTransition;
    }
    track.style.transform = `translateX(${-slideWidth * currentIndex}px)`;
    updateDots();
  }

  function updateDots() {
    dots.forEach((dot) => dot.classList.remove("active"));
    const equivalentRealSlideIndex = getEquivalentRealSlideIndex(currentIndex);
    for (let i = 0; i < dots.length; i++) {
      if (i === equivalentRealSlideIndex) {
        dots[i].classList.add("active");
      }
    }
  }

  // Function to return a "looped" index value back into the "real" slides range
  function getEquivalentRealSlideIndex(index) {
    return (index - numberOfClonesOnEachSide + realSlides.length) % realSlides.length;
  }

  // Function to return a "looped" index value back into the "real" slides range
  function getIndexLoopedBackIntoRealSlidesRange(index) {
    // return ((index - numberOfClonesOnEachSide) % realSlides.length) + numberOfClonesOnEachSide;
    return getEquivalentRealSlideIndex(index) + numberOfClonesOnEachSide;
  }

  function handleTransitionEnd() {
    // Handle the infinite loop effect, loop back to the equivalent "real" slide
    lastRealSlideIndex = realSlides.length + numberOfClonesOnEachSide - 1;
    if (currentIndex > lastRealSlideIndex) {
      console.log("currentIndex >= slides.length - numberOfClonesOnEachSide");
      // currentIndex = ((currentIndex - numberOfClonesOnEachSide) % realSlides.length) + numberOfClonesOnEachSide;
      currentIndex = getIndexLoopedBackIntoRealSlidesRange(currentIndex);
      updateCarousel(true);
    } else if (currentIndex < numberOfClonesOnEachSide) {
      currentIndex = getIndexLoopedBackIntoRealSlidesRange(currentIndex);
      updateCarousel(true);
    }
  }

  // Auto-play functionality
  function startAutoPlay() {
    autoPlayInterval = setInterval(() => {
      currentIndex = (currentIndex + 1) % slidesWithClones.length;
      updateCarousel();
    }, autoPlayDelay);
  }

  function stopAutoPlay() {
    clearInterval(autoPlayInterval);
  }

  // Attach events for hover pause
  carousel.addEventListener("mouseenter", stopAutoPlay);
  carousel.addEventListener("mouseleave", startAutoPlay);

  // Button dot functionality
  dots.forEach((dot) => {
    dot.addEventListener("click", (e) => {
      const index = Number(e.target.dataset.index);
      currentIndex = index + numberOfClonesOnEachSide - 1;
      updateCarousel();
    });
  });

  // Start auto-play on page load
  startAutoPlay();

  // Initialize position
  currentIndex = numberOfClonesOnEachSide;
  updateCarousel(true);
  track.addEventListener("transitionend", handleTransitionEnd);
  currentIndex = numberOfClonesOnEachSide;
  updateCarousel(true);
});
