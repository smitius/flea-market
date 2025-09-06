# Design Document

## Overview

This design document outlines the implementation of two key user interface enhancements: a user-accessible language selector and a light/dark mode toggle. Both features will be integrated into the existing navigation system and provide seamless user experience across all devices.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client-Side Layer                        │
├─────────────────────────────────────────────────────────────┤
│ • Language Selector Component                               │
│ • Theme Toggle Component                                    │
│ • Local Storage Management                                  │
│ • CSS Theme Variables                                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Server-Side Layer                        │
├─────────────────────────────────────────────────────────────┤
│ • Language Route Handler                                    │
│ • Session Management                                        │
│ • Flask-Babel Integration                                   │
│ • Template Context Updates                                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Persistence Layer                        │
├─────────────────────────────────────────────────────────────┤
│ • Browser Local Storage (Theme)                             │
│ • Flask Session (Language)                                  │
│ • Admin Settings (Default Language)                         │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Language Selector Component

**Location:** Top navigation bar (desktop and mobile)

**Visual Design:**
- Compact dropdown with current language flag/code
- Dropdown menu showing available languages with flags
- Smooth transition animations
- Consistent styling with existing navigation

**Interface:**
```html
<div class="language-selector">
  <button class="language-toggle" data-current-lang="sv">
    <i class="flag-icon flag-icon-se"></i>
    <span>SV</span>
    <i class="fas fa-chevron-down"></i>
  </button>
  <div class="language-menu">
    <a href="/set-language/sv" class="language-option">
      <i class="flag-icon flag-icon-se"></i>
      <span>Svenska</span>
    </a>
    <a href="/set-language/en" class="language-option">
      <i class="flag-icon flag-icon-us"></i>
      <span>English</span>
    </a>
  </div>
</div>
```

### 2. Theme Toggle Component

**Location:** Top navigation bar, next to language selector

**Visual Design:**
- Single button with icon (sun/moon)
- Smooth icon transition on toggle
- Consistent with navigation button styling
- Tooltip showing current mode

**Interface:**
```html
<button class="theme-toggle" id="themeToggle" title="Switch to dark mode">
  <i class="fas fa-moon"></i>
</button>
```

### 3. CSS Theme System

**Implementation:** CSS custom properties (variables) for theme switching

**Light Theme Variables:**
```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f8f9fa;
  --text-primary: #212529;
  --text-secondary: #6c757d;
  --border-color: #dee2e6;
  --shadow: rgba(0, 0, 0, 0.1);
}
```

**Dark Theme Variables:**
```css
[data-theme="dark"] {
  --bg-primary: #1a1a1a;
  --bg-secondary: #2d2d2d;
  --text-primary: #ffffff;
  --text-secondary: #b0b0b0;
  --border-color: #404040;
  --shadow: rgba(0, 0, 0, 0.3);
}
```

## Data Models

### Language Preference Storage

**Client-Side (Session):**
```python
# Flask session storage
session['user_language'] = 'sv'  # or 'en'
```

**Server-Side (Admin Default):**
```python
# Existing SiteSettings model
class SiteSettings:
    language = db.Column(db.String(5), default='sv')
```

### Theme Preference Storage

**Client-Side (Local Storage):**
```javascript
// Browser local storage
localStorage.setItem('theme-preference', 'dark');
```

**System Preference Detection:**
```javascript
// CSS media query
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
```

## Error Handling

### Language Selector Error Handling

1. **Invalid Language Code:**
   - Fallback to admin-configured default language
   - Log warning for debugging

2. **Translation Loading Failure:**
   - Use fallback translation system
   - Display error message to user if critical

3. **Server Communication Failure:**
   - Maintain current language selection
   - Retry mechanism for language switching

### Theme Toggle Error Handling

1. **Local Storage Unavailable:**
   - Fallback to light theme
   - Use session storage as backup

2. **CSS Loading Issues:**
   - Ensure base styles always load
   - Graceful degradation to light theme

3. **JavaScript Disabled:**
   - Default to light theme
   - Language selector still functional via server-side

## Testing Strategy

### Unit Tests

1. **Language Switching Logic:**
   - Test language route handler
   - Verify session storage
   - Test fallback mechanisms

2. **Theme Toggle Functionality:**
   - Test local storage operations
   - Verify CSS class application
   - Test system preference detection

### Integration Tests

1. **Cross-Feature Compatibility:**
   - Language + theme combinations
   - Persistence across page navigation
   - Mobile navigation integration

2. **Existing Feature Compatibility:**
   - Search/sort with language changes
   - Admin panel theme application
   - Image gallery theme support

### User Experience Tests

1. **Accessibility Testing:**
   - Screen reader compatibility
   - Keyboard navigation
   - Color contrast ratios (dark mode)

2. **Performance Testing:**
   - Theme switching speed
   - Language switching response time
   - Mobile device performance

3. **Cross-Browser Testing:**
   - Modern browser support
   - Fallback behavior
   - Local storage compatibility

## Implementation Phases

### Phase 1: Theme Toggle System
1. CSS variable system setup
2. Dark theme color scheme
3. JavaScript toggle functionality
4. Local storage persistence

### Phase 2: Language Selector
1. Navigation UI components
2. Server-side language routes
3. Session management
4. Currency auto-switching

### Phase 3: Integration & Polish
1. Mobile navigation integration
2. Admin panel theme support
3. Accessibility improvements
4. Performance optimizations

### Phase 4: Testing & Documentation
1. Comprehensive testing
2. User documentation
3. Developer documentation
4. Translation updates

## Security Considerations

1. **Language Selection:**
   - Validate language codes server-side
   - Prevent injection attacks via language parameter
   - Rate limiting on language switching

2. **Theme Preference:**
   - Client-side only (no security implications)
   - Sanitize any user-provided theme data

3. **Session Management:**
   - Secure session handling for language preference
   - Proper session cleanup

## Performance Considerations

1. **CSS Loading:**
   - Minimize CSS bundle size
   - Use efficient CSS selectors
   - Avoid layout thrashing during theme switch

2. **JavaScript Execution:**
   - Debounce rapid theme toggles
   - Efficient DOM manipulation
   - Minimal JavaScript bundle impact

3. **Server Requests:**
   - Cache language switching responses
   - Minimize server round-trips
   - Efficient session storage