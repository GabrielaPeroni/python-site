/**
 * MaricaCity - Landing Page JavaScript
 * Handles Swiper carousel initialization for featured places
 */

document.addEventListener('DOMContentLoaded', function () {
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
});
