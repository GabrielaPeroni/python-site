/**
 * Google Maps integration for Place Detail Page
 * Displays an embedded map with a marker at the place's location
 */

let map;
let marker;

function initPlaceMap() {
  // Get map container and data
  const mapContainer = document.getElementById('place-map');

  if (!mapContainer) {
    return;
  }

  // Get coordinates from data attributes
  const latitude = parseFloat(mapContainer.dataset.latitude);
  const longitude = parseFloat(mapContainer.dataset.longitude);
  const placeName = mapContainer.dataset.placeName;

  // Check if coordinates are valid
  if (isNaN(latitude) || isNaN(longitude)) {
    mapContainer.parentElement.style.display = 'none';
    return;
  }

  // Create location object
  const placeLocation = { lat: latitude, lng: longitude };

  // Initialize map
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

  // Create marker
  marker = new google.maps.Marker({
    position: placeLocation,
    map: map,
    title: placeName,
    animation: google.maps.Animation.DROP,
  });

  // Create info window
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

  // Show info window on marker click
  marker.addListener('click', () => {
    infoWindow.open(map, marker);
  });

  // Open info window by default
  infoWindow.open(map, marker);

  // Add bounce animation on marker hover
  marker.addListener('mouseover', () => {
    marker.setAnimation(google.maps.Animation.BOUNCE);
    setTimeout(() => marker.setAnimation(null), 750);
  });
}

// Initialize when Google Maps script is loaded
window.initPlaceMap = initPlaceMap;
