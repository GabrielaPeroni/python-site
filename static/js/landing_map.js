/**
 * Interactive Google Maps for Landing Page
 * Shows all places with clickable markers and info windows
 */

let landingMap;
let markers = [];
let infoWindow;
let markerCluster;

async function initLandingMap() {
  const mapContainer = document.getElementById('landing-map');

  if (!mapContainer) {
    console.log('Landing map container not found');
    return;
  }

  // Default center (Maricá, Brazil)
  const defaultCenter = { lat: -22.9194, lng: -42.8186 };

  // Initialize map
  landingMap = new google.maps.Map(mapContainer, {
    center: defaultCenter,
    zoom: 12,
    mapTypeControl: true,
    mapTypeControlOptions: {
      style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
      position: google.maps.ControlPosition.TOP_RIGHT,
    },
    streetViewControl: true,
    fullscreenControl: true,
    zoomControl: true,
  });

  // Create single info window instance (reused for all markers)
  infoWindow = new google.maps.InfoWindow();

  // Fetch places data
  try {
    const response = await fetch('/explorar/api/map-data/');
    const data = await response.json();

    if (data.places && data.places.length > 0) {
      // Create markers for all places
      createMarkers(data.places);

      // Fit map to show all markers
      fitMapToMarkers();
    } else {
      console.log('No places with coordinates found');
    }

    // Update place count
    updatePlaceCount(data.count);
  } catch (error) {
    console.error('Error fetching places data:', error);
  }
}

function createMarkers(places) {
  places.forEach(place => {
    const marker = new google.maps.Marker({
      position: { lat: place.latitude, lng: place.longitude },
      map: landingMap,
      title: place.name,
      animation: google.maps.Animation.DROP,
    });

    // Store place data with marker
    marker.placeData = place;

    // Add click listener to show info window
    marker.addListener('click', () => {
      showInfoWindow(marker);
    });

    markers.push(marker);
  });

  console.log(`Created ${markers.length} markers on landing map`);
}

function showInfoWindow(marker) {
  const place = marker.placeData;

  // Build info window content
  let content = `
    <div style="max-width: 280px; padding: 8px;">
      ${
        place.image_url
          ? `
        <img src="${place.image_url}" alt="${place.name}"
             style="width: 100%; height: 150px; object-fit: cover; border-radius: 8px; margin-bottom: 12px;">
      `
          : ''
      }

      <h6 style="margin: 0 0 8px 0; font-weight: 600; color: #212529;">
        ${place.category_icon} ${place.name}
      </h6>

      ${
        place.rating
          ? `
        <div style="margin-bottom: 8px;">
          <span style="color: #ffc107; font-size: 14px;">★</span>
          <span style="font-weight: 600; font-size: 14px;">${place.rating.toFixed(
            1
          )}</span>
          <span style="color: #6c757d; font-size: 13px;">(${
            place.review_count
          } avaliações)</span>
        </div>
      `
          : ''
      }

      <p style="margin: 0 0 12px 0; font-size: 14px; color: #6c757d; line-height: 1.4;">
        ${place.description}
      </p>

      <a href="${place.url}"
         style="display: inline-block; padding: 8px 16px; background: #212529; color: white;
                text-decoration: none; border-radius: 4px; font-size: 14px; font-weight: 500;">
        Ver Detalhes →
      </a>
    </div>
  `;

  infoWindow.setContent(content);
  infoWindow.open(landingMap, marker);
}

function fitMapToMarkers() {
  if (markers.length === 0) return;

  const bounds = new google.maps.LatLngBounds();
  markers.forEach(marker => {
    bounds.extend(marker.getPosition());
  });

  landingMap.fitBounds(bounds);

  // Don't zoom in too much if there's only one marker
  if (markers.length === 1) {
    landingMap.setZoom(15);
  }
}

function updatePlaceCount(count) {
  const countElement = document.getElementById('map-place-count');
  if (countElement) {
    countElement.textContent = count;
  }
}

// Make function globally available for Google Maps callback
window.initLandingMap = initLandingMap;
