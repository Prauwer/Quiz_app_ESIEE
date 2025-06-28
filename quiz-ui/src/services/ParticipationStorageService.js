const PLAYER_NAME_KEY = 'playerName';
const PLAYER_SCORE_KEY = 'playerScore';

export default {
  savePlayerName(playerName) {
    window.localStorage.setItem(PLAYER_NAME_KEY, playerName);
  },

  getPlayerName() {
    return window.localStorage.getItem(PLAYER_NAME_KEY);
  },

  saveParticipationScore(score) {
    window.localStorage.setItem(PLAYER_SCORE_KEY, score);
  },

  getParticipationScore() {
    return parseInt(window.localStorage.getItem(PLAYER_SCORE_KEY) || '0');
  },

  clear() {
    window.localStorage.removeItem(PLAYER_NAME_KEY);
    window.localStorage.removeItem(PLAYER_SCORE_KEY);
  },
};
