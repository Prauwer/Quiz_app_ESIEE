import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import NewQuizPage from '../views/newQuizPage.vue';
import QuestionManager from '../views/QuestionManager.vue';
import scorePage from '../views/scorePage.vue';
import AdminPage from '../views/adminPage.vue';
import QuestionEdition from '../components/admin/QuestionEdition.vue'; // On anticipe

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomePage,
    },
    {
      path: '/new-quiz',
      name: 'NewQuiz',
      component: NewQuizPage,
    },
    {
      path: '/questions',
      name: 'Question',
      component: QuestionManager,
    },
    {
      path: '/score',
      name: 'Score',
      component: scorePage,
    },
    {
      path: '/admin',
      name: 'Admin',
      component: AdminPage,
    },
    {
      path: '/admin/edit/:id',
      name: 'QuestionEdit',
      component: QuestionEdition,
    },
  ],
});

export default router;
