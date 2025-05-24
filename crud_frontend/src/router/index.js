import Vue from 'vue'
import Router from 'vue-router'

// Páginas
import Login from '@/components/Login.vue'
import Register from '@/components/Register.vue'
import CarList from '@/components/CarList.vue'
import CarForm from '@/components/CarForm.vue'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      component: Login
    },
    {
      path: '/register',
      component: Register
    },
    {
      path: '/carros',
      component: CarList,
      meta: { requiresAuth: true }
    },
    {
      path: '/novo',
      component: CarForm,
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/editar/:id',
      component: CarForm,
      props: true,
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '*',
      redirect: '/login'
    }
  ]
})

// Proteção das rotas
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const tipo = localStorage.getItem('tipo')

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      return next('/login')
    }

    if (to.matched.some(record => record.meta.requiresAdmin) && tipo !== 'admin') {
      return next('/carros') // redireciona usuários comuns
    }
  }

  next()
})

export default router
