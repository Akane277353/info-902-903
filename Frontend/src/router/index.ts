import { useUserStore } from '@/stores/user-store/user-store'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('../views/AuthenticationView.vue')
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('../views/DashboardView.vue'),
      beforeEnter: async () => {
        await hasAccess()
      }
    }
  ]
})

async function hasAccess() {
  const userStore = useUserStore()
  if (userStore.getUser.id === 0 || userStore.getUser.pseudo === '') {
    console.log('No user found')
    router.push('/')
  }
}

export default router
