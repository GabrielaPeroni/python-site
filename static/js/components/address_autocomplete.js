/**
 * Google Maps Places Autocomplete for Place Form
 * Handles address autocomplete and automatic latitude/longitude capture
 * Uses the new PlaceAutocompleteElement API (recommended by Google as of March 2025)
 */

let autocompleteInput;
let addressTextarea;
let latitudeField;
let longitudeField;

function initAutocomplete() {
  // Get form fields
  addressTextarea = document.getElementById('id_address');
  latitudeField = document.getElementById('id_latitude');
  longitudeField = document.getElementById('id_longitude');

  if (!addressTextarea) {
    console.error('Address field not found');
    return;
  }

  // Hide the original textarea temporarily
  addressTextarea.style.display = 'none';

  // Create a text input for autocomplete
  autocompleteInput = document.createElement('input');
  autocompleteInput.type = 'text';
  autocompleteInput.className = addressTextarea.className;
  autocompleteInput.placeholder = 'Comece a digitar o endereço...';
  autocompleteInput.value = addressTextarea.value;

  // Insert the autocomplete input before the textarea
  addressTextarea.parentNode.insertBefore(autocompleteInput, addressTextarea);

  // Create autocomplete instance using the classic API (still supported)
  const autocomplete = new google.maps.places.Autocomplete(autocompleteInput, {
    types: ['address'],
    componentRestrictions: { country: 'BR' }, // Restrict to Brazil
    fields: ['formatted_address', 'geometry', 'address_components'],
  });

  // Listen for place selection
  autocomplete.addListener('place_changed', () => {
    const place = autocomplete.getPlace();
    onPlaceChanged(place);
  });

  // Sync manual input to hidden textarea
  autocompleteInput.addEventListener('input', function () {
    addressTextarea.value = this.value;
  });

  // Prevent form submission on Enter key in address field
  autocompleteInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      e.preventDefault();
    }
  });
}

function onPlaceChanged(place) {
  if (!place.geometry || !place.geometry.location) {
    console.warn('No geometry data for selected place');
    return;
  }

  // Update both input and textarea with formatted address
  const formattedAddress = place.formatted_address || '';
  autocompleteInput.value = formattedAddress;
  addressTextarea.value = formattedAddress;

  // Update latitude and longitude
  if (latitudeField && longitudeField) {
    const lat = place.geometry.location.lat();
    const lng = place.geometry.location.lng();

    latitudeField.value = lat.toFixed(6);
    longitudeField.value = lng.toFixed(6);
  }

  // Optional: Update city/state fields if they exist
  if (place.address_components) {
    updateAddressComponents(place.address_components);
  }
}

function updateAddressComponents(components) {
  // This function can be extended to auto-fill other fields like city, state, etc.
  // Example: Extract city and state if needed
  components.forEach(component => {
    const types = component.types;
    // Can be used to populate city/state fields if form fields are added
    if (types.includes('locality')) {
      // City: component.long_name
    }
    if (types.includes('administrative_area_level_1')) {
      // State: component.short_name
    }
  });
}

// Initialize when Google Maps script is loaded
window.initAutocomplete = initAutocomplete;
