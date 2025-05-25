<template>
  <div class="user-content">
    <h1>Meus Livros</h1>
    <div v-if="meusLivros.length" class="books-grid">
      <div v-for="livro in meusLivros" :key="livro.id" class="book-card">
        <img
          :src="`http://localhost:5000/static/${livro.arquivo}`"
          alt="Capa do livro"
        />
        <p>{{ livro.nome }}</p>
      </div>
    </div>
    <p v-else>Você não tem livros no momento.</p>
  </div>
</template>

<script>
import emprestimosService from '@/services/emprestimos'

export default {
  name: 'Home',
  data() {
    return {
      meusLivros: []
    }
  },
  created() {
    const token = localStorage.getItem('access_token')
    if (!token) {
      this.$router.push({ name: 'Login' })
      return
    }
    this.$axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    this.carregarMeusLivros()
  },
  methods: {
    carregarMeusLivros() {
      emprestimosService.listarMeus()
        .then(res => {
          this.meusLivros = res.data
        })
        .catch(err => {
          console.error(err)
          alert('Erro ao carregar seus livros.')
        })
    }
  }
}
</script>

<style scoped>
.user-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}
.books-grid {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
.book-card {
  width: 150px;
  text-align: center;
}
.book-card img {
  width: 100%;
  border-radius: 8px;
}
</style>
