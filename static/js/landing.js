/**
 * MaricaCity - JavaScript da Página Inicial
 * Gerencia a inicialização do carrossel Swiper
 */

// Função de inicialização
function initializeSwipers() {
  // Inicializar Carrossel Hero
  window.heroSwiperInstance = new Swiper('.hero-swiper', {
    loop: true,
    effect: 'fade',
    speed: 600, // Transição mais rápida
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
    allowTouchMove: true, // Habilitar toque/deslize
    touchRatio: 1,
    threshold: 10, // Limite inferior para deslize mais responsivo
  });

  // Inicializar carrossel Swiper para lugares destacados
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

// Executar inicialização quando o DOM estiver pronto ou imediatamente se já estiver pronto
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeSwipers);
} else {
  initializeSwipers();
}

// Impedir que o dropdown de login feche ao clicar dentro
// e pausar autoplay do carrossel quando o dropdown estiver aberto
document.addEventListener('DOMContentLoaded', function () {
  const loginDropdown = document.querySelector('.login-dropdown');
  const loginDropdownParent = document.querySelector('#loginDropdown');

  if (loginDropdown) {
    // Impedir que o dropdown feche ao clicar dentro
    loginDropdown.addEventListener('click', function (e) {
      e.stopPropagation();
    });
  }

  // Usar um pequeno atraso para garantir que o swiper esteja inicializado
  setTimeout(function () {
    if (loginDropdownParent) {
      // Pausar autoplay quando o dropdown abre
      loginDropdownParent.addEventListener('shown.bs.dropdown', function () {
        if (window.heroSwiperInstance && window.heroSwiperInstance.autoplay) {
          window.heroSwiperInstance.autoplay.stop();
        }

        // Acionar renderização do botão Google Sign-In se disponível
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

      // Retomar autoplay quando o dropdown fecha
      loginDropdownParent.addEventListener('hidden.bs.dropdown', function () {
        if (window.heroSwiperInstance && window.heroSwiperInstance.autoplay) {
          window.heroSwiperInstance.autoplay.start();
        }
      });
    }
  }, 100);
});
