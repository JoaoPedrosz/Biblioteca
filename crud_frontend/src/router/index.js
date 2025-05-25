// src/router/index.js

import Vue from 'vue'
import VueRouter from 'vue-router'

// Layouts
import AuthLayout from '@/layouts/AuthLayout.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import UserLayout from '@/layouts/UserLayout.vue'

// Public/Auth
import Login from '@/components/Login.vue'
import Register from '@/components/Register.vue'
import ForgotPassword from '@/components/ForgotPassword.vue'

// Admin
import LibrarianDashboard from '@/components/LibrarianDashboard.vue'
import BookForm from '@/components/BookForm.vue'
import AccessRequests from '@/components/AccessRequests.vue'
import AdminAcervo from '@/components/AdminAcervo.vue'

// User
import Home from '@/components/Home.vue'
import Acervo from '@/components/Acervo.vue'
import BookDetail from '@/components/BookDetail.vue'

Vue.use(VueRouter)

const routes = [
  // rotas públicas / auth
  {
    path: '/',
    component: AuthLayout,
    children: [
      { path: '', redirect: { name: 'Login' } },
      { path: 'login', name: 'Login', component: Login },
      { path: 'register', name: 'Register', component: Register },
      { path: 'forgot', name: 'ForgotPassword', component: ForgotPassword }
    ]
  },

  // área do bibliotecário (admin)
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      { path: '', name: 'AdminDashboard', component: LibrarianDashboard },
      { path: 'livros/new', name: 'BookForm', component: BookForm },
      { path: 'livros/:id', name: 'BookFormEdit', component: BookForm, props: true },
      { path: 'solicitacoes', name: 'AccessRequests', component: AccessRequests },
      { path: 'acervo', name: 'AdminAcervo', component: AdminAcervo }
    ]
  },

  // área do usuário comum
  {
    path: '/app',
    component: UserLayout,
    children: [
      { path: '', name: 'Home', component: Home },
      { path: 'acervo', name: 'Acervo', component: Acervo },
      { path: 'livro/:isbn', name: 'BookDetail', component: BookDetail, props: true }
    ]
  },

  // catch-all redireciona para login
  {
    path: '*',
    redirect: { name: 'Login' }
  }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router
