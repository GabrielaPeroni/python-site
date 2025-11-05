/**
 * Integração do Google Maps para Página de Detalhes do Local
 * Exibe um mapa incorporado com um marcador na localização do local
 */

let map;
let marker;

function initPlaceMap() {
  // Obter contêiner do mapa e dados
  const mapContainer = document.getElementById('place-map');

  if (!mapContainer) {
    return;
  }

  // Obter coordenadas dos atributos de dados
  const latitude = parseFloat(mapContainer.dataset.latitude);
  const longitude = parseFloat(mapContainer.dataset.longitude);
  const placeName = mapContainer.dataset.placeName;

  // Verificar se as coordenadas são válidas
  if (isNaN(latitude) || isNaN(longitude)) {
    mapContainer.parentElement.style.display = 'none';
    return;
  }

  // Criar objeto de localização
  const placeLocation = { lat: latitude, lng: longitude };

  // Inicializar mapa
  map = new google.maps.Map(mapContainer, {
    center: placeLocation,
    zoom: 15,
    mapTypeControl: true,
    mapTypeControlOptions: {
      style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
      position: google.maps.ControlPosition.TOP_RIGHT,
    },
    streetViewControl: true,
    fullscreenControl: true,
    zoomControl: true,
  });

  // Criar marcador
  marker = new google.maps.Marker({
    position: placeLocation,
    map: map,
    title: placeName,
    animation: google.maps.Animation.DROP,
  });

  // Criar janela de informação
  const infoWindow = new google.maps.InfoWindow({
    content: `
      <div style="padding: 8px; max-width: 200px;">
        <h6 style="margin: 0 0 4px 0; font-weight: 600; color: #212529;">${placeName}</h6>
        <p style="margin: 0; font-size: 0.875rem; color: #6c757d;">
          ${latitude.toFixed(6)}, ${longitude.toFixed(6)}
        </p>
      </div>
    `,
  });

  // Mostrar janela de informação ao clicar no marcador
  marker.addListener('click', () => {
    infoWindow.open(map, marker);
  });

  // Abrir janela de informação por padrão
  infoWindow.open(map, marker);

  // Adicionar animação de salto ao passar o mouse sobre o marcador
  marker.addListener('mouseover', () => {
    marker.setAnimation(google.maps.Animation.BOUNCE);
    setTimeout(() => marker.setAnimation(null), 750);
  });
}

// Inicializar quando o script do Google Maps for carregado
window.initPlaceMap = initPlaceMap;
