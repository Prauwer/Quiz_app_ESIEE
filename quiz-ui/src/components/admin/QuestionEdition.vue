<template>
  <div class="edition-form">
    <h2>{{ isEditing ? 'Modifier la question' : 'Créer une nouvelle question' }}</h2>

    <form @submit.prevent="saveQuestion" v-if="localQuestion">
      <div class="form-group">
        <label>Titre de la question</label>
        <input type="text" v-model="localQuestion.title" required />
      </div>

      <div class="form-group">
        <label>Propositions de réponse</label>
        <div
          v-for="(proposition, index) in localQuestion.propositions"
          :key="index"
          class="proposition-group"
        >
          <input type="text" v-model="localQuestion.propositions[index]" />
          <input
            type="radio"
            :name="'correct-answer'"
            :value="index"
            v-model="localQuestion.réponse"
          />
        </div>
      </div>

      <!-- Image à gérer plus tard -->
      <ImageUpload @file-change="imageFileChangedHandler" :fileDataUrl="imageAsb64" />

      <div class="form-actions">
        <button type="submit">Enregistrer</button>
        <router-link to="/admin" class="button-cancel">Annuler</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import quizData from '@/data/questions.json';
import ImageUpload from '@/components/admin/ImageUpload.vue';

const route = useRoute();
const router = useRouter();

// "Copie locale" de la question pour pouvoir la modifier dans le formulaire
const localQuestion = ref(null);

// Détermine si on est en mode édition ou création
const isEditing = computed(() => route.params.id !== 'new');

// Variable pour stocker l'image en base64
const imageAsb64 = ref('');

onMounted(() => {
  const questionId = parseInt(route.params.id);

  if (isEditing.value) {
    const originalQuestion = quizData.questions.find((q) => q.id === questionId);
    if (originalQuestion) {
      // COPIE LOCALE : Très important car les props/données importées sont en lecture seule.
      // On crée une copie pour pouvoir la modifier sans affecter l'original.
      localQuestion.value = JSON.parse(JSON.stringify(originalQuestion));
    }
  } else {
    // Mode création : on initialise un objet question vide
    localQuestion.value = {
      id: Date.now(), // ID temporaire
      title: '',
      propositions: ['', '', '', ''], // 4 propositions vides par défaut
      réponse: 0, // La première réponse est correcte par défaut
      image: '',
    };
  }
});

function saveQuestion() {
  if (isEditing.value) {
    console.log(
      'SIMULATION : Enregistrement des modifications pour la question',
      localQuestion.value
    );
  } else {
    console.log('SIMULATION : Création de la nouvelle question', localQuestion.value);
  }
  alert('Modifications enregistrées (simulation). Redirection vers la liste.');
  router.push('/admin');
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
