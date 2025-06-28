<template>
  <div class="admin-container">
    <div v-if="!isAuthenticated" class="login-form">
      <h2>Connexion Administrateur</h2>
      <form @submit.prevent="handleLogin">
        <input type="password" v-model="password" placeholder="Mot de passe" />
        <button type="submit">Connexion</button>
        <p v-if="loginError" class="error">Mot de passe incorrect.</p>
      </form>
    </div>
    <div v-else class="admin-dashboard">
      <header>
        <h1>Tableau de Bord Admin</h1>
        <button @click="handleLogout">Déconnexion</button>
      </header>
      <main>
        <QuestionsList />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import AdminAuthService from '@/services/AdminAuthService.js';
import quizApiService from '@/services/QuizApiService.js';
import QuestionsList from '@/components/admin/QuestionsList.vue';

const password = ref('');
const isAuthenticated = ref(false);
const loginError = ref(false);

onMounted(() => {
  isAuthenticated.value = AdminAuthService.isAuthenticated();
});

async function handleLogin() {
  try {
    const response = await quizApiService.login({ password: password.value });
    const token = response.data.token;
    if (token) {
      AdminAuthService.saveToken(token);
      isAuthenticated.value = true;
      loginError.value = false;
    }
  } catch (error) {
    loginError.value = true;
  }
}

function handleLogout() {
  AdminAuthService.logout();
  isAuthenticated.value = false;
}
</script>
