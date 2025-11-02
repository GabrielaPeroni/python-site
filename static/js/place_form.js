/**
 * MaricaCity - Place Form JavaScript
 * Handles image upload preview and management for place creation/editing
 */

document.addEventListener('DOMContentLoaded', function () {
  const previewGrid = document.getElementById('image-preview-grid');
  const addImageBtn = document.getElementById('add-image-btn');
  const formsetContainer = document.getElementById('formset-container');
  const formsetForms = formsetContainer.querySelectorAll('.formset-form');
  let imageCount = 0;
  const MAX_IMAGES = 3;

  // Count existing images on page load
  formsetForms.forEach((formDiv, index) => {
    const imageInput = formDiv.querySelector('input[type="file"]');
    const deleteInput = formDiv.querySelector('input[name*="DELETE"]');
    const existingImageUrl = formDiv.dataset.existingImageUrl;

    // Check if there's an existing image (from database) and it's not marked for deletion
    if (existingImageUrl && !deleteInput.checked) {
      imageCount++;
      createPreviewCard(existingImageUrl, index, true);
    }
  });

  // Handle add image button click
  addImageBtn.addEventListener('click', function () {
    if (imageCount >= MAX_IMAGES) {
      alert(`Você pode adicionar no máximo ${MAX_IMAGES} imagens.`);
      return;
    }

    // Find first available form slot
    let targetFormIndex = -1;
    formsetForms.forEach((formDiv, index) => {
      if (targetFormIndex === -1) {
        const deleteInput = formDiv.querySelector('input[name*="DELETE"]');
        const imageInput = formDiv.querySelector('input[type="file"]');
        const existingImageUrl = formDiv.dataset.existingImageUrl;

        // Available if not deleted, has no new file, and has no existing image
        if (!deleteInput.checked && !imageInput.files.length && !existingImageUrl) {
          targetFormIndex = index;
        }
      }
    });

    if (targetFormIndex === -1) {
      alert('Não há mais espaço para novas imagens.');
      return;
    }

    // Trigger file input click
    const formDiv = formsetForms[targetFormIndex];
    const imageInput = formDiv.querySelector('input[type="file"]');
    imageInput.click();

    // Handle file selection
    imageInput.onchange = function (e) {
      const file = e.target.files[0];
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function (event) {
          createPreviewCard(event.target.result, targetFormIndex, false);
          imageCount++;
          updateButtonState();
        };
        reader.readAsDataURL(file);
      }
    };
  });

  /**
   * Create a preview card for an image
   * @param {string} imageSrc - Image source URL or data URL
   * @param {number} formIndex - Index of the form in formset
   * @param {boolean} isExisting - Whether this is an existing image
   */
  function createPreviewCard(imageSrc, formIndex, isExisting) {
    const col = document.createElement('div');
    col.className = 'col-6 col-md-4';
    col.dataset.formIndex = formIndex;

    col.innerHTML = `
      <div class="card position-relative">
        <img src="${imageSrc}" class="card-img-top" style="height: 150px; object-fit: cover;" loading="lazy">
        <button type="button" class="btn btn-danger btn-sm position-absolute top-0 end-0 m-2 remove-image" data-form-index="${formIndex}">
          <i class="bi bi-trash"></i>
        </button>
        ${
          formIndex === 0
            ? '<span class="badge bg-primary position-absolute top-0 start-0 m-2">Principal</span>'
            : ''
        }
      </div>
    `;

    previewGrid.appendChild(col);

    const removeBtn = col.querySelector('.remove-image');
    removeBtn.addEventListener('click', function () {
      removeImage(formIndex, col);
    });
  }

  /**
   * Remove an image from the preview and mark for deletion
   * @param {number} formIndex - Index of the form in formset
   * @param {HTMLElement} cardElement - The card element to remove
   */
  function removeImage(formIndex, cardElement) {
    const formDiv = formsetForms[formIndex];
    const deleteInput = formDiv.querySelector('input[name*="DELETE"]');
    const imageInput = formDiv.querySelector('input[type="file"]');

    if (deleteInput) {
      deleteInput.checked = true;
    }

    if (imageInput) {
      imageInput.value = '';
    }

    // Clear the existing image URL data attribute
    if (formDiv.dataset.existingImageUrl) {
      delete formDiv.dataset.existingImageUrl;
    }

    cardElement.remove();
    imageCount--;
    updateButtonState();
  }

  /**
   * Update the add button state based on image count
   */
  function updateButtonState() {
    if (imageCount >= MAX_IMAGES) {
      addImageBtn.disabled = true;
      addImageBtn.classList.add('disabled');
      addImageBtn.querySelector('span').textContent = 'Limite de fotos atingido';
    } else {
      addImageBtn.disabled = false;
      addImageBtn.classList.remove('disabled');
      addImageBtn.querySelector('span').textContent = 'Adicionar Fotos';
    }
  }

  // Initial button state update
  updateButtonState();

  // Set display order and primary automatically on form submit
  document.getElementById('place-form').addEventListener('submit', function (e) {
    const previewCards = previewGrid.querySelectorAll('[data-form-index]');
    previewCards.forEach((card, index) => {
      const formIndex = card.dataset.formIndex;
      const formDiv = formsetForms[formIndex];
      const orderInput = formDiv.querySelector('input[name*="display_order"]');
      const primaryInput = formDiv.querySelector('input[name*="is_primary"]');

      if (orderInput) orderInput.value = index;
      if (primaryInput) primaryInput.checked = index === 0;
    });
  });
});
