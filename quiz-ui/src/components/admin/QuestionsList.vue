<template>
  <div class="questions-list">
    <div class="list-header">
      <h3>Liste des Questions ({{ questions.length }})</h3>
      <div class="main-actions">
        <router-link to="/admin/edit/new" class="button">Ajouter une question</router-link>
      </div>
    </div>

    <ul>
      <li v-for="question in questions" :key="question.id">
        <span>{{ question.position }}. {{ question.title }}</span>
        <div class="actions">
          <router-link :to="'/admin/edit/' + question.id" class="button-edit">Modifier</router-link>
          <button @click="deleteQuestion(question.id)" class="button-delete">Supprimer</button>
        </div>
      </li>
    </ul>

    <!-- Zone pour les actions dangereuses (déplacée en bas) -->
    <div class="danger-zone">
      <h4>Actions globales</h4>
      <button @click="deleteAllQuestions" class="button-delete">
        Supprimer toutes les questions
      </button>
      <button @click="deleteAllParticipations" class="button-delete">
        Supprimer toutes les participations
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import quizApiService from "@/services/QuizApiService.js";

const questions = ref([]);

async function loadQuestions() {
  // Note: l'admin a aussi besoin de toutes les questions.
  // En attendant, on utilise la même logique de boucle que pour les participants.
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
      // Pas besoin de recharger les données de cette page, mais on pourrait
      // par exemple mettre à jour une autre partie de l'état de l'application si nécessaire.
    } catch (error) {
      alert("La suppression de toutes les participations a échoué.");
    }
  }
}
</script>

<style scoped>
.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.danger-zone {
  background-color: #fff5f5;
  border: 1px solid #e53e3e;
  border-radius: 8px;
  padding: 15px;
  margin-top: 30px; /* Ajout d'un espace en haut */
}
.danger-zone h4 {
  margin-top: 0;
  color: #c53030;
}
.danger-zone .button-delete {
  margin-right: 10px;
}

ul {
  list-style: none;
  padding: 0;
}
li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ccc;
}
.actions {
  display: flex;
  gap: 10px;
}

/* Style de base pour les boutons, à adapter à votre design system */
.button,
.button-edit,
.button-delete {
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-decoration: none;
  color: white;
  font-weight: bold;
}
.button {
  background-color: #42b983;
}
.button-edit {
  background-color: #f0ad4e;
}
.button-delete {
  background-color: #d9534f;
}
</style>
