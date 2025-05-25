// src/router/index.js
import Vue from 'vue'
import VueRouter from 'vue-router'

import AuthLayout from '@/layouts/AuthLayout.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import UserLayout from '@/layouts/UserLayout.vue'

import Login from '@/components/Login.vue'
import ForgotPassword from '@/components/ForgotPassword.vue'
import Register from '@/components/Register.vue'

import LibrarianDashboard from '@/components/LibrarianDashboard.vue'
import BookForm from '@/components/BookForm.vue'
import AccessRequests from '@/components/AccessRequests.vue'
import AdminAcervo from '@/components/AdminAcervo.vue'

import Home from '@/components/Home.vue'
import Acervo from '@/components/Acervo.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: AuthLayout,
    children: [
      { path: '', redirect: { name: 'Login' } },
      { path: 'login', name: 'Login', component: Login },
      { path: 'forgot', name: 'ForgotPassword', component: ForgotPassword },
      { path: 'register', name: 'Register', component: Register }
    ]
  },
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      { path: '', name: 'AdminDashboard', component: LibrarianDashboard },
      { path: 'livros/new', name: 'BookForm', component: BookForm },
      { path: 'solicitacoes', name: 'AccessRequests', component: AccessRequests },
      { path: 'acervo', name: 'AdminAcervo', component: AdminAcervo }
    ]
  },
  {
    path: '/app',
    component: UserLayout,
    children: [
      { path: '', name: 'Home', component: Home },
      { path: 'acervo', name: 'Acervo', component: Acervo }
    ]
  },
  { path: '*', redirect: { name: 'Login' } }
]

const router = new VueRouter({
  mode: 'hash',
  routes
})

export default router
