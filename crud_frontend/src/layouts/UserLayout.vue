<!-- src/layouts/UserLayout.vue -->
<template>
  <div id="user-layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-logo">
        <img :src="logo" alt="Logo Acervo" />
      </div>
      <h2 class="sidebar-title">Home</h2>
      <ul class="sidebar-menu">
        <li :class="{ active: $route.name === 'Home' }">
          <router-link to="/app">
            <i class="fas fa-home"></i>
            <span>Home</span>
          </router-link>
        </li>
        <li :class="{ active: $route.name === 'Acervo' }">
          <router-link to="/app/acervo">
            <i class="fas fa-book-open"></i>
            <span>Acervo</span>
          </router-link>
        </li>
      </ul>
    </aside>

    <!-- Cabeçalho -->
    <header class="header">
      <div class="search-bar">
        <i class="fas fa-search"></i>
        <input
          type="text"
          placeholder="Digite o nome do livro/autor"
          v-model="search"
        />
      </div>
      <div class="user-avatar">
        <i class="fas fa-user-circle"></i>
        <span class="user-name">{{ userNome }} {{ userSobrenome }}</span>
        <button class="btn-logout" @click="logout">
          <i class="fas fa-sign-out-alt"></i>
          Sair
        </button>
      </div>
    </header>

    <!-- Conteúdo dinâmico -->
    <main class="view-container">
      <router-view />
    </main>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'UserLayout',
  data() {
    return {
      search: '',
      userNome: '',
      userSobrenome: ''
    }
  },
  computed: {
    logo() {
      return require('@/assets/IconeLivro.png')
    }
  },
  created() {
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    this.userNome = user.nome || ''
    this.userSobrenome = user.sobrenome || ''
  },
  methods: {
    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      delete axios.defaults.headers.common['Authorization']
      this.$router.push({ name: 'Login' })
    }
  }
}
</script>

<style scoped>
#user-layout {
  display: grid;
  grid-template-columns: 220px 1fr;
  grid-template-rows: 110px 1fr;
  grid-template-areas:
    "sidebar header"
    "sidebar content";
  height: 100vh;
  overflow: hidden;
}

/* Sidebar */
.sidebar {
  grid-area: sidebar;
  background: #eeeeee;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-right: 1px solid #e0e0e0;
  padding: 32px 0;
}
.sidebar-logo {
  width: 90px;
  height: 90px;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 16px;
}
.sidebar-logo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.sidebar-title {
  font-size: 18px;
  margin-bottom: 36px;
  color: #333;
  font-weight: 500;
}
.sidebar-menu {
  list-style: none;
  width: 100%;
  padding-left: 36px;
}
.sidebar-menu li {
  margin-bottom: 22px;
  font-size: 17px;
  transition: color 0.2s;
}
.sidebar-menu li.active,
.sidebar-menu li:hover {
  color: #3751fe;
  font-weight: 600;
}
.sidebar-menu li i {
  margin-right: 8px;
}
.sidebar-menu a {
  text-decoration: none;
  color: inherit;
  display: flex;
  align-items: center;
}

/* Header */
.header {
  grid-area: header;
  background: #222d36;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 58px;
}
.search-bar {
  background: #eef0f2;
  border-radius: 32px;
  padding: 8px 24px;
  display: flex;
  align-items: center;
  width: 480px;
}
.search-bar input {
  background: transparent;
  border: none;
  font-size: 18px;
  margin-left: 6px;
  outline: none;
  width: 100%;
  color: #222;
}
.user-avatar {
  background: #eef0f2;
  padding: 8px 16px;
  border-radius: 20px;
  display: flex;
  align-items: center;
}
.user-avatar i {
  margin-right: 8px;
  font-size: 18px;
  color: #555;
}
.user-name {
  margin-right: 12px;
  font-size: 15px;
  font-weight: 500;
  color: #555;
}
/* Botão Sair */
.btn-logout {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #555;
  display: flex;
  align-items: center;
}
.btn-logout i {
  margin-right: 4px;
}
.btn-logout:hover {
  color: #000;
}

/* Conteúdo */
.view-container {
  grid-area: content;
  background: #fff;
  overflow-y: auto;
  padding: 20px;
}
</style>
