const PLAYER_NAME_KEY = 'playerName';
const SCORE_KEY = 'playerScore';

export default {
  savePlayerName(playerName) {
    window.localStorage.setItem(PLAYER_NAME_KEY, playerName);
  },
  getPlayerName() {
    // todo : implement
    return window.localStorage.getItem(PLAYER_NAME_KEY);
  },

  saveParticipationScore(participationScore) {
    // todo : implement
    window.localStorage.setItem(SCORE_KEY, participationScore);
  },
  getParticipationScore() {
    // todo : implement
    return window.localStorage.getItem(SCORE_KEY);
  },

  clear() {
    window.localStorage.removeItem(PLAYER_NAME_KEY);
    window.localStorage.removeItem(SCORE_KEY);
  },
};
