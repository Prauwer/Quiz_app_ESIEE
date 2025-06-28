<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3>Liste des Questions ({{ questions.length }})</h3>
      <div class="d-flex align-items-center">
        <router-link to="/admin/edit/new" class="btn btn-primary me-3"
          >Ajouter une question</router-link
        >
        <button @click="logout" class="btn btn-outline-danger border-2" title="Déconnexion">
          <i class="bi bi-box-arrow-right"></i>
        </button>
      </div>
    </div>

    <ul class="list-group">
      <li
        v-for="question in questions"
        :key="question.id"
        class="list-group-item d-flex justify-content-between align-items-center"
      >
        <span>{{ question.position }}. {{ question.title }}</span>
        <div class="actions">
          <router-link :to="'/admin/edit/' + question.id" class="btn btn-secondary btn-sm me-2"
            >Modifier</router-link
          >
          <button @click="deleteQuestion(question.id)" class="btn btn-danger btn-sm">
            Supprimer
          </button>
        </div>
      </li>
    </ul>

    <!-- Zone pour les actions dangereuses -->
    <div class="p-4 mt-5 bg-light border rounded-3 text-center">
      <h4>Actions globales</h4>
      <p class="text-muted">Attention, ces actions sont irréversibles.</p>
      <div class="d-flex justify-content-center gap-2 mb-3">
        <button @click="deleteAllQuestions" class="btn btn-danger">Supprimer les questions</button>
        <button @click="deleteAllParticipations" class="btn btn-danger">
          Supprimer les participations
        </button>
      </div>
      <div>
        <button @click="rebuildDatabase" class="btn btn-warning">Réinitialiser la BDD</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import quizApiService from "@/services/QuizApiService.js";
import adminAuthService from "@/services/AdminAuthService.js";

const router = useRouter();
const questions = ref([]);

async function loadQuestions() {
  try {
    const info = await quizApiService.getQuizInfo();
    const promises = [];
    for (let i = 1; i <= info.data.size; i++) {
      promises.push(quizApiService.getQuestionByPosition(i));
    }
    const responses = await Promise.all(promises);
    questions.value = responses.map((res) => res.data).sort((a, b) => a.position - b.position);
  } catch (e) {
    console.error("Erreur chargement questions admin", e);
  }
}

onMounted(loadQuestions);

function logout() {
  adminAuthService.logout();
  router.push("/login");
}

async function deleteQuestion(questionId) {
  if (window.confirm("Êtes-vous sûr de vouloir supprimer cette question ?")) {
    try {
      await quizApiService.deleteQuestion(questionId);
      loadQuestions(); // Recharger la liste
    } catch (error) {
      alert("La suppression a échoué.");
    }
  }
}

async function rebuildDatabase() {
  if (
    window.confirm(
      "ACTION IRRÉVERSIBLE !\nCeci va effacer TOUTES les données (questions, participations, etc.) et recréer une base vide. Êtes-vous sûr de vouloir continuer ?",
    )
  ) {
    try {
      await quizApiService.rebuildDatabase();
      alert("La base de données a été réinitialisée avec succès.");
      loadQuestions(); // Recharger la liste, qui sera maintenant vide.
    } catch (error) {
      alert("La reconstruction de la base de données a échoué.");
    }
  }
}

async function deleteAllQuestions() {
  if (
    window.confirm(
      "ACTION IRRÉVERSIBLE !\nÊtes-vous sûr de vouloir supprimer TOUTES les questions ?",
    )
  ) {
    try {
      await quizApiService.deleteAllQuestions();
      alert("Toutes les questions ont été supprimées.");
      loadQuestions(); // Recharger la liste pour la vider
    } catch (error) {
      alert("La suppression de toutes les questions a échoué.");
    }
  }
}

async function deleteAllParticipations() {
  if (
    window.confirm(
      "ACTION IRRÉVERSIBLE !\nÊtes-vous sûr de vouloir supprimer TOUTES les participations ?",
    )
  ) {
    try {
      await quizApiService.deleteAllParticipations();
      alert("Toutes les participations ont été supprimées.");
    } catch (error) {
      alert("La suppression de toutes les participations a échoué.");
    }
  }
}
</script>

<style scoped>
/* Scoped styles pour des ajustements fins si nécessaire */
</style>
