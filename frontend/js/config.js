/**
 * Configuration Constants
 * Centralized configuration for backend service URLs
 */

const CONFIG = {
  // Auth Service - User registration and login
  AUTH_SERVICE_URL: 'http://localhost:8000',
  
  // Item Service - Lost & Found items
  ITEM_SERVICE_URL: 'http://localhost:8001',
  
  // Local storage keys
  STORAGE_KEYS: {
    USER_ID: 'user_id',
    USER_NAME: 'user_name',
    USER_EMAIL: 'user_email',
    IS_LOGGED_IN: 'is_logged_in'
  }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CONFIG;
}
