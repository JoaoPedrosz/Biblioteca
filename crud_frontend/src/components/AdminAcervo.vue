<template>
  <div class="admin-acervo">
    <h1>Acervo de Livros</h1>
    <table class="acervo-table">
      <thead>
        <tr>
          <th>Nome</th>
          <th>Autor</th>
          <th>ISBN</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="livro in livros" :key="livro.id">
          <td>{{ livro.nome }}</td>
          <td>{{ livro.autor }}</td>
          <td>{{ livro.isbn }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminAcervo',
  data() {
    return {
      livros: []
    }
  },
  created() {
    const token = localStorage.getItem('access_token')
    if (!token) {
      this.$router.push({ name: 'Login' })
      return
    }
    axios.defaults.headers.common['Authorization'] = 'Bearer ' + token
    this.carregarAcervo()
  },
  methods: {
    carregarAcervo() {
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
}
</script>

<style scoped>
.admin-acervo {
  padding: 20px;
}

.acervo-table {
  width: 100%;
  border-collapse: collapse;
}

.acervo-table th,
.acervo-table td {
  border: 1px solid #ddd;
  padding: 12px;
}

.acervo-table th {
  background: #f5f5f5;
  text-align: left;
}
</style>
