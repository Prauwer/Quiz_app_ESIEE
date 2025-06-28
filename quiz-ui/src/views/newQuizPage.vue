<template>
  <div class="new-quiz-page bg-light py-5">
    <div class="container">
      <div class="row justify-content-center align-items-center">
        <div class="col-md-6 col-lg-5">
          <div class="card shadow-sm">
            <div class="card-body p-5">
              <h1 class="card-title text-center mb-2">Prêt pour le Défi ?</h1>
              <p class="card-subtitle text-center text-muted mb-4">
                Saisissez votre nom pour démarrer le quiz
              </p>

              <form @submit.prevent="launchNewQuiz">
                <div class="mb-3">
                  <label for="username" class="form-label">Votre nom</label>
                  <input
                    id="username"
                    type="text"
                    class="form-control form-control-lg"
                    v-model="username"
                    placeholder="Prénom NOM"
                    required
                  />
                </div>
                <button type="submit" class="btn btn-primary w-100 btn-lg mt-4">
                  <i class="bi bi-play-circle me-2"></i>
                  Démarrer le quiz
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from '@/services/ParticipationStorageService.js';

const username = ref('');
const router = useRouter();

function launchNewQuiz() {
  if (username.value.trim() === '') return;
  participationStorageService.savePlayerName(username.value);
  router.push('/questions');
}
</script>

<style lang="scss" scoped>
.new-quiz-page {
  display: flex;
  align-items: center;
  min-height: 100vh;
}
</style>
