document.addEventListener('DOMContentLoaded', function () {
  // Initialize theme system
  initThemeSystem();
  
  // Initialize mobile navigation
  initMobileNavigation();
  
  // Initialize modern gallery
  initModernGallery();
});

// Theme System
function initThemeSystem() {
  const htmlElement = document.documentElement;
  
  // Remove preload class to enable transitions after page load
  setTimeout(() => {
    document.body.classList.remove('preload');
  }, 100);
  
  // Get stored theme preference or detect system preference
  function getInitialTheme() {
    const storedTheme = localStorage.getItem('theme-preference');
    if (storedTheme && (storedTheme === 'light' || storedTheme === 'dark')) {
      return storedTheme;
    }
    
    // Check system preference on first visit
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    
    return 'light';
  }
  
  // Apply theme to document with error handling
  function applyTheme(theme) {
    try {
      htmlElement.setAttribute('data-theme', theme);
      localStorage.setItem('theme-preference', theme);
      
      // Dispatch custom event for theme change
      window.dispatchEvent(new CustomEvent('themeChanged', { 
        detail: { theme: theme } 
      }));
    } catch (error) {
      console.warn('Failed to save theme preference:', error);
      // Still apply the theme even if localStorage fails
      htmlElement.setAttribute('data-theme', theme);
    }
  }
  
  // Initialize theme on page load
  const initialTheme = getInitialTheme();
  applyTheme(initialTheme);
  
  // Listen for system theme changes
  if (window.matchMedia) {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addEventListener('change', (e) => {
      // Only auto-switch if user hasn't manually set a preference
      const hasManualPreference = localStorage.getItem('theme-preference');
      if (!hasManualPreference) {
        const systemTheme = e.matches ? 'dark' : 'light';
        applyTheme(systemTheme);
        updateThemeToggleButton(systemTheme);
      }
    });
  }
  
  // Expose theme switching function globally for theme toggle button
  window.toggleTheme = function() {
    const currentTheme = htmlElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
    
    // Update theme toggle button if it exists
    updateThemeToggleButton(newTheme);
    
    // Add smooth transition effect
    htmlElement.style.transition = 'none';
    setTimeout(() => {
      htmlElement.style.transition = '';
    }, 50);
  };
  
  // Get current theme function
  window.getCurrentTheme = function() {
    return htmlElement.getAttribute('data-theme') || 'light';
  };
  
  // Update theme toggle button appearance with smooth transitions
  function updateThemeToggleButton(theme) {
    const themeToggle = document.getElementById('themeToggle');
    const mobileThemeToggle = document.getElementById('mobileThemeToggle');
    
    [themeToggle, mobileThemeToggle].forEach(button => {
      if (button) {
        const icon = button.querySelector('i');
        if (icon) {
          // Add rotation animation during icon change
          icon.style.transform = 'rotate(180deg)';
          
          setTimeout(() => {
            if (theme === 'dark') {
              icon.className = 'fas fa-sun';
              button.title = 'Switch to light mode';
              button.setAttribute('aria-label', 'Switch to light mode');
            } else {
              icon.className = 'fas fa-moon';
              button.title = 'Switch to dark mode';
              button.setAttribute('aria-label', 'Switch to dark mode');
            }
            
            // Reset rotation
            setTimeout(() => {
              icon.style.transform = '';
            }, 150);
          }, 150);
        }
      }
    });
  }
  
  // Initialize theme toggle buttons if they exist
  const themeToggle = document.getElementById('themeToggle');
  const mobileThemeToggle = document.getElementById('mobileThemeToggle');
  
  [themeToggle, mobileThemeToggle].forEach(button => {
    if (button) {
      updateThemeToggleButton(initialTheme);
      button.addEventListener('click', window.toggleTheme);
    }
  });
}

// Mobile Navigation
function initMobileNavigation() {
  const mobileMenuToggle = document.getElementById('mobileMenuToggle');
  const mobileMenu = document.getElementById('mobileMenu');
  const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');
  
  if (!mobileMenuToggle) return;
  
  function toggleMobileMenu() {
    const isActive = mobileMenu.classList.contains('active');
    
    if (isActive) {
      closeMobileMenu();
    } else {
      openMobileMenu();
    }
  }
  
  function openMobileMenu() {
    mobileMenuToggle.classList.add('active');
    mobileMenu.classList.add('active');
    mobileMenuOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
  
  function closeMobileMenu() {
    mobileMenuToggle.classList.remove('active');
    mobileMenu.classList.remove('active');
    mobileMenuOverlay.classList.remove('active');
    document.body.style.overflow = '';
  }
  
  mobileMenuToggle.addEventListener('click', toggleMobileMenu);
  mobileMenuOverlay.addEventListener('click', closeMobileMenu);
  
  // Close menu when clicking on nav links
  document.querySelectorAll('.mobile-nav-link').forEach(link => {
    link.addEventListener('click', closeMobileMenu);
  });
}

// Modern Gallery
function initModernGallery() {
  let currentIndex = 0;
  let images = [];
  let currentItemId = null;
  
  const gallery = document.getElementById('modernGallery');
  const galleryImage = document.getElementById('galleryImage');
  const galleryLoading = document.getElementById('galleryLoading');
  const galleryClose = document.getElementById('galleryClose');
  const galleryPrev = document.getElementById('galleryPrev');
  const galleryNext = document.getElementById('galleryNext');
  const galleryCounter = document.getElementById('galleryCounter');
  const galleryThumbnails = document.getElementById('galleryThumbnails');
  const galleryFullscreen = document.getElementById('galleryFullscreen');
  const galleryOverlay = document.getElementById('galleryOverlay');
  
  if (!gallery) return;
  
  // Touch and pan variables
  let isDragging = false;
  let startX = 0;
  let startY = 0;
  let currentX = 0;
  let currentY = 0;
  let scale = 1;
  let initialDistance = 0;
  
  function openGallery(imageUrls, itemId) {
    images = imageUrls;
    currentItemId = itemId;
    currentIndex = 0;
    scale = 1;
    
    // Track the view
    if (itemId) {
      fetch(`/item/${itemId}/view`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      }).catch(error => {
        console.log('View tracking failed:', error);
      });
    }
    
    createThumbnails();
    showImage(0);
    gallery.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
  
  function closeGallery() {
    gallery.classList.remove('active');
    document.body.style.overflow = '';
    
    // Reset state
    setTimeout(() => {
      galleryImage.src = '';
      images = [];
      currentIndex = 0;
      scale = 1;
      galleryImage.style.transform = '';
    }, 300);
  }
  
  function showImage(index) {
    if (images.length === 0) return;
    
    currentIndex = (index + images.length) % images.length;
    
    // Show loading
    galleryLoading.style.display = 'block';
    
    // Preload image
    const img = new Image();
    img.onload = () => {
      galleryImage.src = images[currentIndex];
      galleryLoading.style.display = 'none';
      scale = 1;
      galleryImage.style.transform = '';
    };
    img.src = images[currentIndex];
    
    // Update counter
    galleryCounter.textContent = `${currentIndex + 1} / ${images.length}`;
    
    // Update thumbnails
    updateThumbnails();
    
    // Update navigation visibility
    galleryPrev.style.display = images.length > 1 ? 'block' : 'none';
    galleryNext.style.display = images.length > 1 ? 'block' : 'none';
  }
  
  function createThumbnails() {
    galleryThumbnails.innerHTML = '';
    
    if (images.length <= 1) {
      galleryThumbnails.style.display = 'none';
      return;
    }
    
    galleryThumbnails.style.display = 'flex';
    
    images.forEach((src, index) => {
      const thumb = document.createElement('img');
      thumb.src = src;
      thumb.className = 'gallery-thumbnail';
      thumb.addEventListener('click', () => showImage(index));
      galleryThumbnails.appendChild(thumb);
    });
  }
  
  function updateThumbnails() {
    const thumbnails = galleryThumbnails.querySelectorAll('.gallery-thumbnail');
    thumbnails.forEach((thumb, index) => {
      thumb.classList.toggle('active', index === currentIndex);
    });
  }
  
  // Event listeners
  galleryClose.addEventListener('click', closeGallery);
  galleryOverlay.addEventListener('click', closeGallery);
  galleryPrev.addEventListener('click', () => showImage(currentIndex - 1));
  galleryNext.addEventListener('click', () => showImage(currentIndex + 1));
  
  // Keyboard navigation
  function handleKeydown(e) {
    if (!gallery.classList.contains('active')) return;
    
    switch(e.key) {
      case 'Escape':
        closeGallery();
        break;
      case 'ArrowLeft':
        showImage(currentIndex - 1);
        break;
      case 'ArrowRight':
        showImage(currentIndex + 1);
        break;
    }
  }
  
  document.addEventListener('keydown', handleKeydown);
  
  // Touch and mouse events for pan and zoom
  function getDistance(touches) {
    const dx = touches[0].clientX - touches[1].clientX;
    const dy = touches[0].clientY - touches[1].clientY;
    return Math.sqrt(dx * dx + dy * dy);
  }
  
  // Touch events
  galleryImage.addEventListener('touchstart', (e) => {
    e.preventDefault();
    
    if (e.touches.length === 1) {
      // Single touch - pan
      isDragging = true;
      startX = e.touches[0].clientX;
      startY = e.touches[0].clientY;
    } else if (e.touches.length === 2) {
      // Two touches - zoom
      initialDistance = getDistance(e.touches);
    }
  });
  
  galleryImage.addEventListener('touchmove', (e) => {
    e.preventDefault();
    
    if (e.touches.length === 1 && isDragging) {
      // Pan
      currentX = e.touches[0].clientX - startX;
      currentY = e.touches[0].clientY - startY;
      
      if (scale > 1) {
        galleryImage.style.transform = `scale(${scale}) translate(${currentX / scale}px, ${currentY / scale}px)`;
      }
    } else if (e.touches.length === 2) {
      // Zoom
      const distance = getDistance(e.touches);
      const newScale = Math.max(1, Math.min(3, scale * (distance / initialDistance)));
      
      if (newScale !== scale) {
        scale = newScale;
        if (scale === 1) {
          galleryImage.style.transform = '';
          currentX = 0;
          currentY = 0;
        } else {
          galleryImage.style.transform = `scale(${scale}) translate(${currentX / scale}px, ${currentY / scale}px)`;
        }
      }
    }
  });
  
  galleryImage.addEventListener('touchend', (e) => {
    if (e.touches.length === 0) {
      isDragging = false;
      
      // Check for swipe gesture
      if (scale === 1 && Math.abs(currentX) > 50 && Math.abs(currentY) < 100) {
        if (currentX > 0) {
          showImage(currentIndex - 1);
        } else {
          showImage(currentIndex + 1);
        }
      }
      
      // Reset position if not zoomed
      if (scale === 1) {
        currentX = 0;
        currentY = 0;
        galleryImage.style.transform = '';
      }
    }
  });
  
  // Double tap to zoom
  let lastTap = 0;
  galleryImage.addEventListener('touchend', (e) => {
    const currentTime = new Date().getTime();
    const tapLength = currentTime - lastTap;
    
    if (tapLength < 500 && tapLength > 0) {
      // Double tap
      if (scale === 1) {
        scale = 2;
        galleryImage.style.transform = `scale(${scale})`;
      } else {
        scale = 1;
        galleryImage.style.transform = '';
        currentX = 0;
        currentY = 0;
      }
    }
    
    lastTap = currentTime;
  });
  
  // Fullscreen toggle
  galleryFullscreen.addEventListener('click', () => {
    if (!document.fullscreenElement) {
      gallery.requestFullscreen().catch(err => {
        console.log('Fullscreen not supported:', err);
      });
    } else {
      document.exitFullscreen();
    }
  });
  
  // Item card click handlers
  document.querySelectorAll('.item-card').forEach((card) => {
    card.addEventListener('click', () => {
      const data = card.getAttribute('data-images');
      const itemId = card.getAttribute('data-item-id');
      
      if (!data) return;
      
      const imageUrls = data.split(',').map(url => url.trim()).filter(url => url);
      openGallery(imageUrls, itemId);
    });
  });
}



// Search and Sort Enhancement
document.addEventListener('DOMContentLoaded', function() {
  initSearchEnhancements();
});

function initSearchEnhancements() {
  const searchInput = document.getElementById('searchInput');
  const searchForm = searchInput?.closest('form');
  
  if (!searchInput || !searchForm) return;
  
  // Auto-submit search after typing stops
  let searchTimeout;
  searchInput.addEventListener('input', function() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      if (searchInput.value.length >= 2 || searchInput.value.length === 0) {
        searchForm.submit();
      }
    }, 500); // Wait 500ms after user stops typing
  });
  
  // Handle Enter key
  searchInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      clearTimeout(searchTimeout);
      searchForm.submit();
    }
  });
  
  // Focus search input with Ctrl+F or Cmd+F
  document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
      e.preventDefault();
      searchInput.focus();
      searchInput.select();
    }
  });
  
  // Add loading state during search
  searchForm.addEventListener('submit', function() {
    const submitBtn = searchForm.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
      submitBtn.disabled = true;
    }
  });
}

// Smooth scroll to results after search
if (window.location.search.includes('search=')) {
  document.addEventListener('DOMContentLoaded', function() {
    const resultsSection = document.getElementById('itemsGrid');
    if (resultsSection) {
      setTimeout(() => {
        resultsSection.scrollIntoView({ 
          behavior: 'smooth', 
          block: 'start' 
        });
      }, 100);
    }
  });
}