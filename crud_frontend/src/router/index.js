import { createRouter, createWebHistory } from 'vue-router'
import Home        from '@/views/Home.vue'        // lista de livros
import Login       from '@/components/Login.vue'
import Register    from '@/components/Register.vue'
import BookForm    from '@/components/BookForm.vue' // Tela22.html
import BookList    from '@/components/BookList.vue' // Tela10.html
// … importe outras telas conforme for criando …

const routes = [
  { path: '/login',    name: 'Login',    component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/',         name: 'Home',     component: Home,      meta: { requiresAuth: true } },
  { path: '/livros/new',name: 'BookForm', component: BookForm, meta: { requiresAuth: true } },
  { path: '/livros',   name: 'BookList', component: BookList,  meta: { requiresAuth: true } },
  // …
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuth = !!localStorage.getItem('usuario')
  if (to.meta.requiresAuth && !isAuth) return next({ name: 'Login' })
  next()
})

export default router
