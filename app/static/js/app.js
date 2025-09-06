document.addEventListener('DOMContentLoaded', function () {
  // Initialize theme system
  initThemeSystem();
  
  // Initialize mobile navigation
  initMobileNavigation();
  
  // Initialize language selector
  initLanguageSelector();
  
  // Initialize modern gallery
  initModernGallery();
});

// Theme System - Performance Optimized
function initThemeSystem() {
  const htmlElement = document.documentElement;
  let isThemeSwitching = false;
  let themeToggleTimeout = null;
  
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
  
  // Apply theme to document with error handling and performance optimization
  function applyTheme(theme, skipTransition = false) {
    try {
      // Performance optimization: Batch DOM updates
      if (skipTransition) {
        document.body.classList.add('theme-switching');
      }
      
      // Use requestAnimationFrame for smooth DOM updates
      requestAnimationFrame(() => {
        htmlElement.setAttribute('data-theme', theme);
        
        // Remove theme-switching class after transition
        if (skipTransition) {
          setTimeout(() => {
            document.body.classList.remove('theme-switching');
          }, 50);
        }
      });
      
      // Store preference asynchronously to avoid blocking
      setTimeout(() => {
        try {
          localStorage.setItem('theme-preference', theme);
        } catch (storageError) {
          console.warn('Failed to save theme preference:', storageError);
        }
      }, 0);
      
      // Dispatch custom event for theme change (debounced)
      clearTimeout(themeToggleTimeout);
      themeToggleTimeout = setTimeout(() => {
        window.dispatchEvent(new CustomEvent('themeChanged', { 
          detail: { theme: theme } 
        }));
      }, 100);
      
    } catch (error) {
      console.warn('Failed to apply theme:', error);
      // Fallback: still apply the theme even if other operations fail
      htmlElement.setAttribute('data-theme', theme);
    }
  }
  
  // Initialize theme on page load
  const initialTheme = getInitialTheme();
  applyTheme(initialTheme, true);
  
  // Listen for system theme changes (debounced)
  if (window.matchMedia) {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    let systemThemeTimeout = null;
    
    mediaQuery.addEventListener('change', (e) => {
      // Debounce system theme changes
      clearTimeout(systemThemeTimeout);
      systemThemeTimeout = setTimeout(() => {
        // Only auto-switch if user hasn't manually set a preference
        const hasManualPreference = localStorage.getItem('theme-preference');
        if (!hasManualPreference) {
          const systemTheme = e.matches ? 'dark' : 'light';
          applyTheme(systemTheme);
          updateThemeToggleButton(systemTheme);
        }
      }, 150);
    });
  }
  
  // Debounced theme toggle function to prevent rapid switching
  let toggleDebounceTimeout = null;
  window.toggleTheme = function() {
    // Prevent rapid theme switching
    if (isThemeSwitching) {
      return;
    }
    
    // Clear any pending toggle
    clearTimeout(toggleDebounceTimeout);
    
    toggleDebounceTimeout = setTimeout(() => {
      isThemeSwitching = true;
      
      const currentTheme = htmlElement.getAttribute('data-theme') || 'light';
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      
      // Apply theme with optimized transition
      applyTheme(newTheme);
      
      // Update theme toggle button if it exists
      updateThemeToggleButton(newTheme);
      
      // Reset switching flag after transition completes
      setTimeout(() => {
        isThemeSwitching = false;
      }, 250);
      
    }, 50); // 50ms debounce delay
  };
  
  // Get current theme function
  window.getCurrentTheme = function() {
    return htmlElement.getAttribute('data-theme') || 'light';
  };
  
  // Update theme toggle button appearance with optimized transitions
  function updateThemeToggleButton(theme) {
    const buttons = [
      document.getElementById('themeToggle'),
      document.getElementById('mobileThemeToggle')
    ].filter(Boolean); // Filter out null elements
    
    // Batch DOM updates for better performance
    requestAnimationFrame(() => {
      buttons.forEach(button => {
        const icon = button.querySelector('i');
        if (!icon) return;
        
        // Use CSS transforms for hardware acceleration
        icon.style.transform = 'rotate3d(0, 0, 1, 180deg)';
        
        // Batch attribute updates
        const updates = theme === 'dark' ? {
          className: 'fas fa-sun',
          title: 'Switch to light mode',
          ariaLabel: 'Switch to light mode'
        } : {
          className: 'fas fa-moon',
          title: 'Switch to dark mode',
          ariaLabel: 'Switch to dark mode'
        };
        
        // Use a single timeout for all updates
        setTimeout(() => {
          // Batch DOM writes
          icon.className = updates.className;
          button.title = updates.title;
          button.setAttribute('aria-label', updates.ariaLabel);
          
          // Reset rotation with hardware acceleration
          requestAnimationFrame(() => {
            icon.style.transform = 'translate3d(0, 0, 0)';
          });
        }, 150);
      });
    });
  }
  
  // Performance monitoring for theme switching (development only)
  function measureThemePerformance(callback) {
    if (typeof performance !== 'undefined' && performance.mark) {
      const startMark = 'theme-switch-start';
      const endMark = 'theme-switch-end';
      
      performance.mark(startMark);
      
      callback();
      
      requestAnimationFrame(() => {
        performance.mark(endMark);
        try {
          performance.measure('theme-switch-duration', startMark, endMark);
          const measure = performance.getEntriesByName('theme-switch-duration')[0];
          if (measure && measure.duration > 100) {
            console.warn(`Theme switch took ${measure.duration.toFixed(2)}ms - consider optimization`);
          }
        } catch (e) {
          // Ignore measurement errors
        }
      });
    } else {
      callback();
    }
  }
  
  // Initialize theme toggle buttons if they exist
  const themeToggle = document.getElementById('themeToggle');
  const mobileThemeToggle = document.getElementById('mobileThemeToggle');
  
  [themeToggle, mobileThemeToggle].forEach(button => {
    if (button) {
      updateThemeToggleButton(initialTheme);
      
      // Add optimized event listener with performance monitoring
      button.addEventListener('click', (e) => {
        e.preventDefault();
        measureThemePerformance(window.toggleTheme);
      }, { passive: false });
    }
  });
}

// Language Selector
function initLanguageSelector() {
  const languageSelector = document.querySelector('.language-selector');
  const languageToggle = document.getElementById('languageToggle');
  const languageMenu = document.getElementById('languageMenu');
  
  if (!languageSelector || !languageToggle || !languageMenu) return;
  
  // Toggle dropdown on click
  languageToggle.addEventListener('click', function(e) {
    e.preventDefault();
    e.stopPropagation();
    toggleLanguageDropdown();
  });
  
  // Close dropdown when clicking outside
  document.addEventListener('click', function(e) {
    if (!languageSelector.contains(e.target)) {
      closeLanguageDropdown();
    }
  });
  
  // Handle keyboard navigation
  languageToggle.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      toggleLanguageDropdown();
    } else if (e.key === 'Escape') {
      closeLanguageDropdown();
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      openLanguageDropdown();
      focusFirstOption();
    }
  });
  
  // Handle option keyboard navigation
  const languageOptions = languageMenu.querySelectorAll('.language-option');
  languageOptions.forEach((option, index) => {
    option.addEventListener('keydown', function(e) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        const nextIndex = (index + 1) % languageOptions.length;
        languageOptions[nextIndex].focus();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        const prevIndex = (index - 1 + languageOptions.length) % languageOptions.length;
        languageOptions[prevIndex].focus();
      } else if (e.key === 'Escape') {
        e.preventDefault();
        closeLanguageDropdown();
        languageToggle.focus();
      } else if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        option.click();
      }
    });
    
    // Add tabindex for keyboard navigation
    option.setAttribute('tabindex', '-1');
  });
  
  function toggleLanguageDropdown() {
    if (languageSelector.classList.contains('active')) {
      closeLanguageDropdown();
    } else {
      openLanguageDropdown();
    }
  }
  
  function openLanguageDropdown() {
    // Close any other open dropdowns first
    document.querySelectorAll('.language-selector.active').forEach(selector => {
      if (selector !== languageSelector) {
        selector.classList.remove('active');
      }
    });
    
    languageSelector.classList.add('active');
    languageToggle.setAttribute('aria-expanded', 'true');
    
    // Focus first option for keyboard users
    setTimeout(() => {
      const firstOption = languageMenu.querySelector('.language-option');
      if (firstOption && document.activeElement === languageToggle) {
        // Only auto-focus if user was using keyboard
        if (document.querySelector(':focus-visible')) {
          firstOption.focus();
        }
      }
    }, 100);
  }
  
  function closeLanguageDropdown() {
    languageSelector.classList.remove('active');
    languageToggle.setAttribute('aria-expanded', 'false');
  }
  
  function focusFirstOption() {
    const firstOption = languageMenu.querySelector('.language-option');
    if (firstOption) {
      firstOption.focus();
    }
  }
  
  // Initialize ARIA attributes
  languageToggle.setAttribute('aria-haspopup', 'true');
  languageToggle.setAttribute('aria-expanded', 'false');
  languageMenu.setAttribute('role', 'menu');
  
  languageOptions.forEach(option => {
    option.setAttribute('role', 'menuitem');
  });
  
  // Handle mobile language options (they don't need dropdown behavior)
  const mobileLanguageOptions = document.querySelectorAll('.mobile-language-option');
  mobileLanguageOptions.forEach(option => {
    option.addEventListener('click', function() {
      // Close mobile menu when language is selected
      const mobileMenu = document.getElementById('mobileMenu');
      const mobileMenuToggle = document.getElementById('mobileMenuToggle');
      const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');
      
      if (mobileMenu && mobileMenuToggle && mobileMenuOverlay) {
        mobileMenuToggle.classList.remove('active');
        mobileMenu.classList.remove('active');
        mobileMenuOverlay.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
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
  
  // Close menu when clicking on language options
  document.querySelectorAll('.mobile-language-option').forEach(option => {
    option.addEventListener('click', closeMobileMenu);
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