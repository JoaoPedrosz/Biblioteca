<template>
  <div id="user-layout">
    <!-- Sidebar Usuário -->
    <aside class="sidebar">
      <div class="sidebar-logo">
        <img :src="logo" alt="Logo Acervo" />
      </div>
      <h2 class="sidebar-title">Home</h2>
      <ul class="sidebar-menu">
        <li :class="{ active: $route.name === 'Home' }">
          <router-link to="/"><i class="fas fa-home"></i><span>Home</span></router-link>
        </li>
        <li :class="{ active: $route.name === 'Acervo' }">
          <router-link to="/acervo"><i class="fas fa-book-open"></i><span>Acervo</span></router-link>
        </li>
      </ul>
    </aside>

    <!-- Header Usuário -->
    <header class="header">
      <div class="search-bar">
        <i class="fas fa-search"></i>
        <input type="text" placeholder="Digite o nome do livro/autor" v-model="search" />
      </div>
      <div class="user-avatar">
        <i class="fas fa-user-circle"></i> Nome do Usuário
      </div>
    </header>

    <!-- Conteúdo dinâmico -->
    <main class="view-container">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'UserLayout',
  data() {
    return { search: '' }
  },
  computed: {
    logo() {
      return require('@/assets/IconeLivro.png')
    }
  }
}
</script>

<style scoped>
/* *** MESMOS ESTILOS do AdminLayout.vue, só trocando o ID *** */
#user-layout {
  display: grid;
  grid-template-columns: 220px 1fr;
  grid-template-rows: 110px 1fr;
  grid-template-areas:
    "sidebar header"
    "sidebar content";
  height: 100vh;
}

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

.header {
  grid-area: header;
  background: #222d36;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 50px 0 58px;
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
  color: #222;
  width: 100%;
}

.user-avatar {
  background: #eef0f2;
  padding: 8px 22px 8px 12px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  font-size: 15px;
  font-weight: 500;
  color: #555;
}
.user-avatar i {
  margin-right: 8px;
}

.view-container {
  grid-area: content;
  overflow-y: auto;
  padding: 20px;
  background: #fff;
}
</style>
