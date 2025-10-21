/**
 * MaricaCity - Landing Page JavaScript
 * Handles Swiper carousel initialization
 */

// Initialize function
function initializeSwipers() {
  // Initialize Hero Carousel
  const heroSwiper = new Swiper('.hero-swiper', {
    loop: true,
    effect: 'fade',
    speed: 1000,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
  });

  // Initialize Swiper carousel for featured places
  const featuredSwiper = document.querySelector('.featured-swiper');

  if (featuredSwiper) {
    new Swiper('.featured-swiper', {
      slidesPerView: 'auto',
      spaceBetween: 16,
      grabCursor: true,
      freeMode: true,
      mousewheel: {
        forceToAxis: true,
      },
    });
  }
}

// Run initialization when DOM is ready or immediately if already ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeSwipers);
} else {
  initializeSwipers();
}
