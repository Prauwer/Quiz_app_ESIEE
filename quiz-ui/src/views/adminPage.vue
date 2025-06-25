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
import { useRouter } from 'vue-router';
import AdminAuthService from '@/services/AdminAuthService.js';
import QuestionsList from '@/components/admin/QuestionsList.vue'; // On va le créer

const password = ref('');
const isAuthenticated = ref(false);
const loginError = ref(false);
const router = useRouter();

// Vérifier l'état de connexion au montage du composant
onMounted(() => {
  isAuthenticated.value = AdminAuthService.isAuthenticated();
});

function handleLogin() {
  if (AdminAuthService.login(password.value)) {
    isAuthenticated.value = true;
    loginError.value = false;
  } else {
    loginError.value = true;
  }
}

function handleLogout() {
  AdminAuthService.logout();
  isAuthenticated.value = false;
  // Optionnel : rediriger ou simplement afficher le formulaire de connexion
  router.push('/');
}
</script>

<style scoped>
.admin-container {
  padding: 20px;
}
.login-form {
  max-width: 300px;
  margin: auto;
}
.error {
  color: red;
}
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
