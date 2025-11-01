/**
 * MaricaCity - Favorites Service
 * Manages favorites using localStorage for all users
 * Optional backend sync for logged-in users
 */

class FavoritesService {
  constructor() {
    this.storageKey = 'marica_favorites';
    this.listeners = [];
  }

  /**
   * Get all favorites from localStorage
   * @returns {number[]} Array of place IDs
   */
  getFavorites() {
    try {
      const stored = localStorage.getItem(this.storageKey);
      return stored ? JSON.parse(stored) : [];
    } catch (error) {
      console.error('Error reading favorites from localStorage:', error);
      return [];
    }
  }

  /**
   * Save favorites to localStorage
   * @param {number[]} favorites - Array of place IDs
   */
  saveFavorites(favorites) {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(favorites));
      this.notifyListeners();
    } catch (error) {
      console.error('Error saving favorites to localStorage:', error);
    }
  }

  /**
   * Check if a place is favorited
   * @param {number} placeId - Place ID to check
   * @returns {boolean}
   */
  isFavorited(placeId) {
    const favorites = this.getFavorites();
    return favorites.includes(parseInt(placeId));
  }

  /**
   * Add a place to favorites
   * @param {number} placeId - Place ID to add
   * @returns {boolean} Success status
   */
  addFavorite(placeId) {
    const favorites = this.getFavorites();
    const id = parseInt(placeId);

    if (!favorites.includes(id)) {
      favorites.push(id);
      this.saveFavorites(favorites);
      return true;
    }
    return false;
  }

  /**
   * Remove a place from favorites
   * @param {number} placeId - Place ID to remove
   * @returns {boolean} Success status
   */
  removeFavorite(placeId) {
    const favorites = this.getFavorites();
    const id = parseInt(placeId);
    const index = favorites.indexOf(id);

    if (index > -1) {
      favorites.splice(index, 1);
      this.saveFavorites(favorites);
      return true;
    }
    return false;
  }

  /**
   * Toggle favorite status
   * @param {number} placeId - Place ID to toggle
   * @returns {boolean} New favorited status
   */
  toggleFavorite(placeId) {
    if (this.isFavorited(placeId)) {
      this.removeFavorite(placeId);
      return false;
    } else {
      this.addFavorite(placeId);
      return true;
    }
  }

  /**
   * Get count of favorites
   * @returns {number}
   */
  getCount() {
    return this.getFavorites().length;
  }

  /**
   * Clear all favorites
   */
  clearAll() {
    this.saveFavorites([]);
  }

  /**
   * Register a listener for favorites changes
   * @param {Function} callback - Callback function
   */
  addListener(callback) {
    this.listeners.push(callback);
  }

  /**
   * Notify all listeners of changes
   */
  notifyListeners() {
    const favorites = this.getFavorites();
    this.listeners.forEach(callback => callback(favorites));
  }

  /**
   * Sync favorites with backend (for logged-in users)
   * @param {string} csrfToken - CSRF token for POST requests
   * @returns {Promise<void>}
   */
  async syncWithBackend(csrfToken) {
    try {
      // Get local favorites
      const localFavorites = this.getFavorites();

      // Send to backend to merge
      const response = await fetch('/explore/favorites/sync/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ favorites: localFavorites }),
      });

      if (response.ok) {
        const data = await response.json();
        // Update local storage with merged favorites from backend
        if (data.favorites) {
          this.saveFavorites(data.favorites);
        }
      }
    } catch (error) {
      console.error('Error syncing favorites with backend:', error);
    }
  }

  /**
   * Load favorites from backend (for logged-in users on page load)
   * @returns {Promise<number[]>}
   */
  async loadFromBackend() {
    try {
      const response = await fetch('/explore/favorites/list/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        if (data.favorites) {
          // Merge with local favorites
          const localFavorites = this.getFavorites();
          const merged = [...new Set([...localFavorites, ...data.favorites])];
          this.saveFavorites(merged);
          return merged;
        }
      }
    } catch (error) {
      console.error('Error loading favorites from backend:', error);
    }
    return this.getFavorites();
  }
}

// Create singleton instance
const favoritesService = new FavoritesService();

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = favoritesService;
}
