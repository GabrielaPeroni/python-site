/**
 * MaricaCity - Landing Page JavaScript
 * Handles Swiper carousel initialization
 */

// Initialize function
function initializeSwipers() {
  // Initialize Hero Carousel
  window.heroSwiperInstance = new Swiper('.hero-swiper', {
    loop: true,
    effect: 'fade',
    speed: 600, // Faster transition
    autoplay: {
      delay: 5000,
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: '.swiper-button-next-custom',
      prevEl: '.swiper-button-prev-custom',
    },
    pagination: {
      el: '.hero-pagination-custom',
      clickable: true,
      type: 'bullets',
    },
    allowTouchMove: true, // Enable touch/swipe
    touchRatio: 1,
    threshold: 10, // Lower threshold for more responsive swipe
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

// Prevent login dropdown from closing when clicking inside
// and pause carousel autoplay when dropdown is open
document.addEventListener('DOMContentLoaded', function () {
  const loginDropdown = document.querySelector('.login-dropdown');
  const loginDropdownParent = document.querySelector('#loginDropdown');

  if (loginDropdown) {
    // Prevent dropdown from closing when clicking inside
    loginDropdown.addEventListener('click', function (e) {
      e.stopPropagation();
    });
  }

  // Use a slight delay to ensure swiper is initialized
  setTimeout(function () {
    if (loginDropdownParent) {
      // Pause autoplay when dropdown opens
      loginDropdownParent.addEventListener('shown.bs.dropdown', function () {
        if (window.heroSwiperInstance && window.heroSwiperInstance.autoplay) {
          window.heroSwiperInstance.autoplay.stop();
        }

        // Trigger Google Sign-In button rendering if available
        if (typeof google !== 'undefined' && google.accounts && google.accounts.id) {
          google.accounts.id.renderButton(
            document.getElementById('google-signin-button-dropdown'),
            {
              theme: 'outline',
              size: 'medium',
              text: 'signin_with',
              shape: 'rectangular',
              logo_alignment: 'left',
              width: 300,
            }
          );
        }
      });

      // Resume autoplay when dropdown closes
      loginDropdownParent.addEventListener('hidden.bs.dropdown', function () {
        if (window.heroSwiperInstance && window.heroSwiperInstance.autoplay) {
          window.heroSwiperInstance.autoplay.start();
        }
      });
    }
  }, 100);
});
