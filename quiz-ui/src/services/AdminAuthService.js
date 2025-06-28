const TOKEN_KEY = 'admin-auth-token';

export default {
  /**
   * Sauvegarde le token reçu de l'API dans le localStorage.
   * @param {string} token
   */
  saveToken(token) {
    window.localStorage.setItem(TOKEN_KEY, token);
  },

  /**
   * Déconnecte l'administrateur en supprimant le token.
   */
  logout() {
    window.localStorage.removeItem(TOKEN_KEY);
  },

  /**
   * Récupère le token depuis le localStorage.
   * @returns {string|null}
   */
  getToken() {
    return window.localStorage.getItem(TOKEN_KEY);
  },

  /**
   * Vérifie si l'administrateur est authentifié (si un token existe).
   * @returns {boolean}
   */
  isAuthenticated() {
    const token = this.getToken();
    return !!token;
  },
};
