const TOKEN_KEY = 'admin-auth-token';

export default {
  /**
   * Simule une connexion. Dans une vraie app, vous appelleriez votre API ici.
   * @param {string} password
   * @returns {boolean} - True si le mot de passe est correct, sinon false.
   */
  login(password) {
    // MOT DE PASSE EN DUR POUR LA SIMULATION
    if (password === 'password123') {
      const fakeToken = 'fake-jwt-token-' + Date.now();
      window.localStorage.setItem(TOKEN_KEY, fakeToken);
      return true;
    }
    return false;
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
   * Vérifie si l'administrateur est authentifié (si un token "truthy" existe).
   * @returns {boolean}
   */
  isAuthenticated() {
    const token = this.getToken();
    return !!token; // Le !! transforme la valeur en booléen (null/undefined -> false, string -> true)
  },
};
