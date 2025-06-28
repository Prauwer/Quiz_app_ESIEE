<template>
  <div class="edition-form">
    <h2>{{ isEditing ? 'Modifier la question' : 'Créer une nouvelle question' }}</h2>

    <form @submit.prevent="saveQuestion" v-if="localQuestion">
      <div class="form-group">
        <label>Position</label>
        <input type="number" v-model="localQuestion.position" required />
      </div>
      <div class="form-group">
        <label>Titre</label>
        <input type="text" v-model="localQuestion.title" required />
      </div>
      <div class="form-group">
        <label>Texte de la question</label>
        <textarea v-model="localQuestion.text"></textarea>
      </div>
      <ImageUpload @file-change="imageFileChangedHandler" :fileDataUrl="imageAsb64" />
      <!-- <div class="form-group">
        <label>Image (URL)</label>
        <input type="text" v-model="localQuestion.image" />
      </div> -->

      <div class="form-group">
        <label>Réponses Possibles</label>
        <div v-for="(answer, index) in localQuestion.possibleAnswers" :key="index">
          <input type="text" v-model="answer.text" required />
          <label>
            <input type="radio" :value="index" v-model="correctAnswerIndex" name="correctAnswer" />
            Correcte
          </label>
        </div>
      </div>

      <div class="form-actions">
        <button type="submit">Enregistrer</button>
        <router-link to="/admin" class="button-cancel">Annuler</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import quizApiService from '@/services/QuizApiService.js';
import ImageUpload from '@/components/admin/ImageUpload.vue';

const route = useRoute();
const router = useRouter();
// "Copie locale" de la question pour pouvoir la modifier dans le formulaire
const localQuestion = ref(null);
// Détermine si on est en mode édition ou création
const isEditing = computed(() => route.params.id !== 'new');
const correctAnswerIndex = ref(0);

// Variable pour stocker l'image en base64
const imageAsb64 = ref('');

onMounted(async () => {
  if (isEditing.value) {
    const questionId = parseInt(route.params.id);
    const response = await quizApiService.getQuestionById(questionId);
    localQuestion.value = response.data;
    correctAnswerIndex.value = localQuestion.value.possibleAnswers.findIndex((a) => a.isCorrect);
  } else {
    // Mode création : on initialise un objet question vide
    localQuestion.value = {
      position: 1,
      title: '',
      text: '',
      image: '',
      possibleAnswers: [{ text: '' }, { text: '' }, { text: '' }, { text: '' }],
    };
  }
});

watch(correctAnswerIndex, (newIndex) => {
  if (localQuestion.value) {
    localQuestion.value.possibleAnswers.forEach((answer, index) => {
      answer.isCorrect = index === newIndex;
    });
  }
});

async function saveQuestion() {
  try {
    // Met à jour la propriété isCorrect avant l'envoi
    localQuestion.value.possibleAnswers.forEach((answer, index) => {
      answer.isCorrect = index === correctAnswerIndex.value;
    });

    if (isEditing.value) {
      await quizApiService.updateQuestion(localQuestion.value.id, localQuestion.value);
    } else {
      await quizApiService.createQuestion(localQuestion.value);
    }
    router.push('/admin');
  } catch (error) {
    alert("L'enregistrement a échoué.");
  }
}

function imageFileChangedHandler(b64String) {
  imageAsb64.value = b64String;
}
</script>

<style scoped>
.edition-form {
  max-width: 600px;
  margin: auto;
}
.form-group {
  margin-bottom: 15px;
}
.proposition-group {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 5px;
}
.form-actions {
  margin-top: 20px;
}
</style>
