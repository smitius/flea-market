document.addEventListener('DOMContentLoaded', function () {
  const adminLoginBtn = document.getElementById('adminLoginBtn');
  const logoutBtn = document.getElementById('logoutBtn');
  const adminDashboardBtn = document.getElementById('adminDashboardBtn');

  adminLoginBtn && adminLoginBtn.addEventListener('click', () => {
    window.location.href = '/auth/login';
  });

  logoutBtn && logoutBtn.addEventListener('click', () => {
    window.location.href = '/auth/logout';
  });

  adminDashboardBtn && adminDashboardBtn.addEventListener('click', () => {
    window.location.href = '/admin/dashboard';
  });
});

document.addEventListener('DOMContentLoaded', () => {
  let currentIndex = 0;
  let images = [];

  const galleryModalElem = document.getElementById('imageGalleryModal');
  const galleryModal = new bootstrap.Modal(galleryModalElem);
  const galleryImage = document.getElementById('galleryImage');
  const prevBtn = document.getElementById('prevImage');
  const nextBtn = document.getElementById('nextImage');

  function showImage(index) {
    if (images.length === 0) return;
    currentIndex = (index + images.length) % images.length;
    galleryImage.src = images[currentIndex];
  }

  document.querySelectorAll('.item-card').forEach((card) => {
    card.addEventListener('click', () => {
      const data = card.getAttribute('data-images');
      if (!data) return;
      images = data.split(',');
      showImage(0);
      galleryModal.show();
    });
  });

  prevBtn.addEventListener('click', () => {
    showImage(currentIndex - 1);
  });

  nextBtn.addEventListener('click', () => {
    showImage(currentIndex + 1);
  });

  // Touch swipe navigation (for mobile)
  let touchStartX = null;
  galleryModalElem.addEventListener('touchstart', function(e) {
    if (e.touches.length === 1) {
      touchStartX = e.touches[0].clientX;
    }
  });
  galleryModalElem.addEventListener('touchend', function(e) {
    if (touchStartX === null) return;
    const touchEndX = e.changedTouches[0].clientX;
    const diffX = touchEndX - touchStartX;
    // Adjust threshold as desired (here: 50px)
    if (diffX > 50) {
      showImage(currentIndex - 1);
    } else if (diffX < -50) {
      showImage(currentIndex + 1);
    }
    touchStartX = null;
  });

    // Explicitly handle close button click to avoid focus issues
  const closeButton = galleryModalElem.querySelector('.btn-close');
  if (closeButton) {
    closeButton.addEventListener('click', (e) => {
      e.preventDefault();
      galleryModal.hide();
      document.body.focus();
    });
  }
  
  // Reset modal content when closed to ensure clean state
  galleryModalElem.addEventListener('hidden.bs.modal', () => {
    galleryImage.src = '';
    images = [];
    currentIndex = 0;
  });
  // Keyboard navigation (left/right arrow support)
  function modalKeyHandler(e) {
    if (e.key === "ArrowLeft") {
      showImage(currentIndex - 1);
    } else if (e.key === "ArrowRight") {
      showImage(currentIndex + 1);
    }
  }

  // Attach/detach keyboard navigation when modal is shown/hidden
  galleryModalElem.addEventListener('shown.bs.modal', () => {
    document.addEventListener('keydown', modalKeyHandler);
  });
  galleryModalElem.addEventListener('hidden.bs.modal', () => {
    document.removeEventListener('keydown', modalKeyHandler);
  });


});


