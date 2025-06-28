// src/services/ParticipationStorageService.js
const PLAYER_NAME_KEY = 'playerName';

export default {
  savePlayerName(playerName) {
    window.localStorage.setItem(PLAYER_NAME_KEY, playerName);
  },

  getPlayerName() {
    return window.localStorage.getItem(PLAYER_NAME_KEY);
  },

  clear() {
    window.localStorage.removeItem(PLAYER_NAME_KEY);
  },
};
