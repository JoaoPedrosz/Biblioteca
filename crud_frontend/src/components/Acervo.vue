<template>
  <div class="acervo-container">
    <h1>Sugestões de Leitura</h1>
    <div class="book-grid">
      <router-link
        v-for="livro in livros"
        :key="livro.id"
        :to="{ name: 'BookDetail', params: { isbn: livro.isbn } }"
        class="book-card"
      >
        <img
          class="book-cover"
          :src="livro.arquivo
            ? `${apiBase}/static/uploads/${livro.arquivo}`
            : placeholder"
          :alt="`Capa de ${livro.nome}`"
        />
        <div class="book-title">{{ livro.nome }}</div>
      </router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
const placeholder = require('@/assets/IconeLivro.png')

export default {
  name: 'Acervo',
  data() {
    return {
      livros: [],
      placeholder,
      apiBase: axios.defaults.baseURL
    }
  },
  created() {
    const token = localStorage.getItem('access_token')
    if (!token) {
      this.$router.push({ name: 'Login' })
      return
    }
    axios.defaults.headers.common['Authorization'] = 'Bearer ' + token

    axios
      .get('/livros')
      .then(res => {
        this.livros = res.data
      })
      .catch(() => {
        alert('Erro ao carregar acervo.')
      })
  }
}
</script>

<style scoped>
.acervo-container {
  padding: 20px;
}
.book-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
}
.book-card {
  width: 150px;
  text-decoration: none;
  color: inherit;
}
.book-cover {
  width: 150px;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
  background: #f0f0f0;
}
.book-title {
  margin-top: 8px;
  font-size: 0.9rem;
  text-align: center;
}
.book-card:hover .book-cover {
  transform: scale(1.05);
  transition: transform 0.2s;
}
</style>
