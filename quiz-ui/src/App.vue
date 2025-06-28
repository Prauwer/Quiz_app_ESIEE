<template>
  <div id="app">
    <nav class="navbar">
      <router-link to="/" class="nav-item">Home</router-link>
      <router-link to="/admin" class="nav-item">Log In</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script setup>
// Pas de script spécifique nécessaire ici pour la navigation simple
</script>

<style lang="scss">
#app {
  display: block;
  width: 100%;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px; // Pour laisser de la place à la barre de navigation
}

.navbar {
  display: flex;
  justify-content: center;
  gap: 20px;
  background-color: #333;
  padding: 15px;
  position: fixed; // Fixe la barre de navigation en haut
  top: 0;
  left: 0;
  width: 100%;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  z-index: 1000; // Assure que la barre de navigation est au-dessus des autres éléments

  .nav-item {
    color: white;
    text-decoration: none;
    font-weight: bold;
    padding: 5px 10px;
    border-radius: 5px;
    transition: background-color 0.3s ease;

    &:hover {
      background-color: #555;
    }

    &.router-link-active {
      background-color: #007bff; // Couleur pour le lien actif
    }

    &.disabled {
      color: #aaa;
      cursor: not-allowed;
      pointer-events: none; // Empêche les clics
    }
  }
}
</style>
