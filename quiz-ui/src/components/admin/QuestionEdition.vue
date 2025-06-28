<template>
  <div class="container mt-4 edition-form">
    <h2>{{ isEditing ? "Modifier la question" : "Créer une nouvelle question" }}</h2>

    <form @submit.prevent="saveQuestion" v-if="localQuestion">
      <div class="mb-3">
        <label for="position" class="form-label">Position</label>
        <input
          id="position"
          type="number"
          class="form-control"
          v-model.number="localQuestion.position"
          required
          min="1"
        />
      </div>
      <div class="mb-3">
        <label for="title" class="form-label">Titre</label>
        <input id="title" type="text" class="form-control" v-model="localQuestion.title" required />
      </div>
      <div class="mb-3">
        <label for="text" class="form-label">Texte de la question</label>
        <textarea id="text" class="form-control" v-model="localQuestion.text"></textarea>
      </div>

      <div class="mb-3">
        <ImageUpload @file-change="imageFileChangedHandler" :fileDataUrl="imageAsb64" />
      </div>

      <hr class="my-4" />

      <div class="mb-3">
        <label class="form-label">Réponses Possibles</label>
        <div
          v-for="(answer, index) in localQuestion.possibleAnswers"
          :key="index"
          class="input-group mb-2"
        >
          <input
            type="text"
            class="form-control"
            v-model="answer.text"
            required
            placeholder="Texte de la réponse"
          />
          <div class="input-group-text">
            <input
              class="form-check-input mt-0"
              type="radio"
              :value="index"
              v-model="correctAnswerIndex"
              :name="'correctAnswer' + index"
            />
            <label class="ms-2">Correcte</label>
          </div>
          <button
            type="button"
            @click="removeAnswer(index)"
            class="btn btn-outline-danger"
            v-if="localQuestion.possibleAnswers.length > 2"
          >
            Supprimer
          </button>
        </div>
        <button type="button" @click="addAnswer" class="btn btn-success mt-2">
          Ajouter une réponse
        </button>
      </div>

      <div class="mt-4">
        <button type="submit" class="btn btn-primary">Enregistrer</button>
        <router-link to="/admin" class="btn btn-secondary ms-2">Annuler</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import quizApiService from "@/services/QuizApiService.js";
import ImageUpload from "@/components/admin/ImageUpload.vue";

const route = useRoute();
const router = useRouter();
const localQuestion = ref(null);
const isEditing = computed(() => route.params.id !== "new");
const correctAnswerIndex = ref(0);
const imageAsb64 = ref("");

onMounted(async () => {
  if (isEditing.value) {
    const questionId = parseInt(route.params.id);
    const response = await quizApiService.getQuestionById(questionId);
    localQuestion.value = response.data;
    imageAsb64.value = response.data.image;
    const foundIndex = localQuestion.value.possibleAnswers.findIndex((a) => a.isCorrect);
    correctAnswerIndex.value = foundIndex !== -1 ? foundIndex : 0;
  } else {
    // Mode création : on récupère la taille du quiz pour proposer la bonne position
    const info = await quizApiService.getQuizInfo();
    const newPosition = info.data.size + 1;

    localQuestion.value = {
      position: newPosition,
      title: "",
      text: "",
      image: "",
      possibleAnswers: [
        { text: "", isCorrect: true },
        { text: "", isCorrect: false },
      ],
    };
    correctAnswerIndex.value = 0;
  }
});

watch(correctAnswerIndex, (newIndex) => {
  if (localQuestion.value) {
    localQuestion.value.possibleAnswers.forEach((answer, index) => {
      answer.isCorrect = index === newIndex;
    });
  }
});

function addAnswer() {
  localQuestion.value.possibleAnswers.push({ text: "", isCorrect: false });
}

function removeAnswer(indexToRemove) {
  // Empêche de supprimer s'il ne reste que 2 réponses
  if (localQuestion.value.possibleAnswers.length <= 2) {
    alert("Une question doit avoir au moins deux réponses possibles.");
    return;
  }

  // Si on supprime la réponse actuellement correcte, on met la première comme correcte par défaut
  if (correctAnswerIndex.value === indexToRemove) {
    correctAnswerIndex.value = 0;
  } else if (correctAnswerIndex.value > indexToRemove) {
    // Si on supprime une réponse avant la réponse correcte, on décale l'index
    correctAnswerIndex.value--;
  }

  localQuestion.value.possibleAnswers.splice(indexToRemove, 1);
}

async function saveQuestion() {
  if (!localQuestion.value) return;

  // Assurer que les valeurs isCorrect sont à jour avant l'envoi
  localQuestion.value.possibleAnswers.forEach((answer, index) => {
    answer.isCorrect = index === correctAnswerIndex.value;
  });

  // Assurer que l'image est bien dans l'objet envoyé
  localQuestion.value.image = imageAsb64.value;

  try {
    if (isEditing.value) {
      await quizApiService.updateQuestion(localQuestion.value.id, localQuestion.value);
    } else {
      await quizApiService.createQuestion(localQuestion.value);
    }
    router.push("/admin");
  } catch (error) {
    console.error("Erreur lors de l'enregistrement:", error);
    alert("L'enregistrement a échoué.");
  }
}

function imageFileChangedHandler(b64String) {
  imageAsb64.value = b64String;
}
</script>

<style scoped>
/* Le style est maintenant géré par Bootstrap. Ce bloc peut être gardé pour des ajustements spécifiques. */
.edition-form {
  max-width: 800px;
  margin: auto;
}
</style>
