<template>
  <div class="admin-page bg-light py-5">
    <div class="container">
      <div class="row justify-content-center">
        <div v-if="!isAuthenticated" class="col-md-6">
          <div class="card shadow-sm">
            <div class="card-body p-5">
              <h2 class="card-title text-center mb-4">Connexion Administrateur</h2>
              <form @submit.prevent="handleLogin">
                <div class="mb-3">
                  <label for="password" class="form-label">Mot de passe</label>
                  <input
                    type="password"
                    id="password"
                    class="form-control"
                    v-model="password"
                    placeholder="••••••••"
                    required
                  />
                </div>
                <button type="submit" class="btn btn-primary w-100">Connexion</button>
                <div v-if="loginError" class="alert alert-danger mt-3">Mot de passe incorrect.</div>
              </form>
            </div>
          </div>
        </div>

        <div v-else class="col-md-10">
          <header class="d-flex justify-content-between align-items-center mb-4">
            <h1 class="h2 mb-0">Tableau de Bord Admin</h1>
            <div>
              <router-link to="/admin/edit/new" class="btn btn-primary me-2">
                <i class="bi bi-plus-circle me-1"></i>
                Ajouter une question
              </router-link>
              <button @click="handleLogout" class="btn btn-secondary" title="Déconnexion">
                <i class="bi bi-box-arrow-right"></i>
              </button>
            </div>
          </header>

          <main>
            <div class="card shadow-sm">
              <div class="card-header">
                <h3 class="h5 mb-0">Liste des Questions ({{ questions.length }})</h3>
              </div>
              <ul class="list-group list-group-flush">
                <li
                  v-for="question in questions"
                  :key="question.id"
                  class="list-group-item d-flex justify-content-between align-items-center"
                >
                  <span>{{ question.position }}. {{ question.title }}</span>
                  <div class="actions">
                    <router-link
                      :to="'/admin/edit/' + question.id"
                      class="btn btn-outline-secondary btn-sm me-2"
                    >
                      <i class="bi bi-pencil"></i> Modifier
                    </router-link>
                    <button
                      @click="deleteQuestion(question.id)"
                      class="btn btn-outline-danger btn-sm"
                    >
                      <i class="bi bi-trash"></i> Supprimer
                    </button>
                  </div>
                </li>
                <li v-if="questions.length === 0" class="list-group-item text-center text-muted">
                  Aucune question dans la base de données.
                </li>
              </ul>
            </div>

            <div class="card shadow-sm mt-5">
              <div class="card-header bg-danger-subtle text-danger-emphasis">
                <h4 class="h6 mb-0">Zone de Danger</h4>
              </div>
              <div class="card-body text-center">
                <p class="text-muted">Attention, les actions suivantes sont irréversibles.</p>
                <div class="d-flex justify-content-center flex-wrap gap-2">
                  <button @click="deleteAllQuestions" class="btn btn-danger">
                    Supprimer toutes les questions
                  </button>
                  <button @click="deleteAllParticipations" class="btn btn-danger">
                    Supprimer toutes les participations
                  </button>
                  <button @click="rebuildDatabase" class="btn btn-warning">
                    Réinitialiser la BDD
                  </button>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService.js';
import AdminAuthService from '@/services/AdminAuthService.js';

// --- Logique de Connexion ---
const password = ref('');
const isAuthenticated = ref(false);
const loginError = ref(false);

onMounted(() => {
  isAuthenticated.value = AdminAuthService.isAuthenticated();
  // Si on est authentifié, on charge les questions
  if (isAuthenticated.value) {
    loadQuestions();
  }
});

async function handleLogin() {
  try {
    const response = await quizApiService.login({ password: password.value });
    const token = response.data.token;
    if (token) {
      AdminAuthService.saveToken(token);
      isAuthenticated.value = true;
      loginError.value = false;
      loadQuestions(); // Charger les questions après une connexion réussie
    }
  } catch (error) {
    loginError.value = true;
    console.error('Erreur de connexion:', error);
  }
}

function handleLogout() {
  AdminAuthService.logout();
  isAuthenticated.value = false;
}

// --- Logique de la Liste de Questions ---
const questions = ref([]);

async function loadQuestions() {
  try {
    const info = await quizApiService.getQuizInfo();
    if (info.data.size === 0) {
      questions.value = [];
      return;
    }
    const promises = [];
    for (let i = 1; i <= info.data.size; i++) {
      promises.push(quizApiService.getQuestionByPosition(i));
    }
    const responses = await Promise.all(promises);
    questions.value = responses.map((res) => res.data).sort((a, b) => a.position - b.position);
  } catch (e) {
    console.error('Erreur chargement questions admin', e);
    questions.value = []; // En cas d'erreur, vider la liste
  }
}

async function deleteQuestion(questionId) {
  if (window.confirm('Êtes-vous sûr de vouloir supprimer cette question ?')) {
    try {
      await quizApiService.deleteQuestion(questionId);
      loadQuestions(); // Recharger la liste
    } catch (error) {
      alert('La suppression a échoué.');
    }
  }
}

async function rebuildDatabase() {
  if (
    window.confirm(
      'ACTION IRRÉVERSIBLE !\nCeci va effacer TOUTES les données (questions, participations, etc.) et recréer une base vide. Êtes-vous sûr de vouloir continuer ?'
    )
  ) {
    try {
      await quizApiService.rebuildDatabase();
      alert('La base de données a été réinitialisée avec succès.');
      loadQuestions(); // Recharger la liste, qui sera maintenant vide.
    } catch (error) {
      alert('La reconstruction de la base de données a échoué.');
    }
  }
}

async function deleteAllQuestions() {
  if (
    window.confirm(
      'ACTION IRRÉVERSIBLE !\nÊtes-vous sûr de vouloir supprimer TOUTES les questions ?'
    )
  ) {
    try {
      await quizApiService.deleteAllQuestions();
      alert('Toutes les questions ont été supprimées.');
      loadQuestions(); // Recharger la liste pour la vider
    } catch (error) {
      alert('La suppression de toutes les questions a échoué.');
    }
  }
}

async function deleteAllParticipations() {
  if (
    window.confirm(
      'ACTION IRRÉVERSIBLE !\nÊtes-vous sûr de vouloir supprimer TOUTES les participations ?'
    )
  ) {
    try {
      await quizApiService.deleteAllParticipations();
      alert('Toutes les participations ont été supprimées.');
    } catch (error) {
      alert('La suppression de toutes les participations a échoué.');
    }
  }
}
</script>

<style scoped>
.admin-page {
  min-height: 100vh;
}
</style>
