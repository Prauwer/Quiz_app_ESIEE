<template>
  <div class="container mt-4">
    <div class="row justify-content-center">
      <div class="col-lg-8 col-md-10">
        <div class="card shadow-sm">
          <div class="card-header bg-light">
            <h2 class="h4 mb-0">
              {{ isEditing ? "Modifier la question" : "Créer une nouvelle question" }}
            </h2>
          </div>
          <div class="card-body p-4">
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
                <input
                  id="title"
                  type="text"
                  class="form-control"
                  v-model="localQuestion.title"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="text" class="form-label">Texte de la question</label>
                <textarea
                  id="text"
                  class="form-control"
                  v-model="localQuestion.text"
                  rows="3"
                ></textarea>
              </div>

              <div class="mb-3">
                <label class="form-label">Image</label>
                <ImageUpload @file-change="imageFileChangedHandler" :fileDataUrl="imageAsb64" />
                <div v-if="imageAsb64" class="mt-3 text-center">
                  <p class="mb-1 text-muted small">Aperçu :</p>
                  <img :src="imageAsb64" alt="Aperçu de l'image" class="question-image-preview" />
                </div>
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
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
                <button
                  type="button"
                  @click="addAnswer"
                  class="btn btn-outline-success btn-sm mt-2"
                >
                  Ajouter une réponse
                </button>
              </div>

              <hr class="my-4" />

              <div class="d-flex justify-content-end">
                <router-link to="/admin" class="btn btn-secondary me-2">Annuler</router-link>
                <button type="submit" class="btn btn-primary">Enregistrer</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
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
        { text: "", isCorrect: false },
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
  if (localQuestion.value.possibleAnswers.length <= 2) {
    alert("Une question doit avoir au moins deux réponses possibles.");
    return;
  }

  if (correctAnswerIndex.value === indexToRemove) {
    correctAnswerIndex.value = 0;
  } else if (correctAnswerIndex.value > indexToRemove) {
    correctAnswerIndex.value--;
  }

  localQuestion.value.possibleAnswers.splice(indexToRemove, 1);
}

async function saveQuestion() {
  if (!localQuestion.value) return;

  localQuestion.value.possibleAnswers.forEach((answer, index) => {
    answer.isCorrect = index === correctAnswerIndex.value;
  });

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
.question-image-preview {
  width: 20%;
  max-width: 200px;
  height: auto;
  margin: 0 auto;
  border: 1px solid #ddd;
  border-radius: 0.25rem;
  padding: 0.25rem;
}
</style>
