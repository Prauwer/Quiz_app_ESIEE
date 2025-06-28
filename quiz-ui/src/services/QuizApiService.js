import axios from 'axios';
import AdminAuthService from './AdminAuthService';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:5000', // Adaptez le port si nécessaire
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token aux requêtes admin
apiClient.interceptors.request.use(
  (config) => {
    const token = AdminAuthService.getToken();
    if (token) {
      // Votre backend attend le token directement, pas avec "Bearer"
      config.headers.Authorization = token;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default {
  // --- PARTIE PUBLIQUE ---

  /**
   * Récupère les informations générales du quiz (taille et scores)
   * GET /quiz-info
   */
  getQuizInfo() {
    return apiClient.get('/quiz-info');
  },

  /**
   * Récupère une question par sa position dans le quiz
   * GET /questions?position={position}
   * @param {number} position
   */
  getQuestionByPosition(position) {
    return apiClient.get(`/questions?position=${position}`);
  },

  /**
   * Sauvegarde une participation à la fin du quiz
   * POST /participations
   * @param {object} participationData - ex: { playerName: 'John', answers: [1, 2, 0, ...] }
   */
  saveParticipation(participationData) {
    return apiClient.post('/participations', participationData);
  },

  // --- PARTIE ADMIN ---

  /**
   * Connecte un administrateur
   * POST /login
   * @param {object} credentials - ex: { password: 'password123' }
   */
  login(credentials) {
    return apiClient.post('/login', credentials);
  },

  /**
   * Récupère les informations générales du quiz (taille et scores)
   * GET /quiz-info
   */
  getQuestionById(questionId) {
    return apiClient.get(`/questions/${questionId}`);
  },

  /**
   * Crée une nouvelle question
   * POST /questions
   */
  createQuestion(questionData) {
    return apiClient.post('/questions', questionData);
  },

  /**
   * Met à jour une question existante
   * PUT /questions/:id
   */
  updateQuestion(questionId, questionData) {
    return apiClient.put(`/questions/${questionId}`, questionData);
  },

  /**
   * Supprime une question
   * DELETE /questions/:id
   */
  deleteQuestion(questionId) {
    return apiClient.delete(`/questions/${questionId}`);
  },
};
