<template>
  <div class="admin-content">
    <h1>Acervo de Livros</h1>
    <table v-if="livros.length" class="acervo-table">
      <thead>
        <tr>
          <th>Nome</th>
          <th>Autor</th>
          <th>ISBN</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="livro in livros" :key="livro.id">
          <td>{{ livro.nome }}</td>
          <td>{{ livro.autor }}</td>
          <td>{{ livro.isbn }}</td>
          <td>
            <button @click="editar(livro)" class="btn-edit">✏️</button>
            <button @click="remover(livro.id)" class="btn-delete">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>Não há livros cadastrados.</p>
  </div>
</template>

<script>
import livrosService from '@/services/livros'

export default {
  name: 'AdminAcervo',
  data() {
    return {
      livros: []
    }
  },
  created() {
    this.carregar()
  },
  methods: {
    carregar() {
      livrosService.listar()
        .then(res => {
          this.livros = res.data
        })
        .catch(() => {
          alert('Erro ao carregar livros.')
        })
    },
    editar(livro) {
      // Passa o objeto livro como parametro para o BookForm
      this.$router.push({ name: 'BookForm', params: { livro } })
    },
    remover(id) {
      if (!confirm('Confirmar remoção desse livro?')) return
      livrosService.remover(id)
        .then(() => this.carregar())
        .catch(() => {
          alert('Erro ao remover livro.')
        })
    }
  }
}
</script>

<style scoped>
.admin-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}
.acervo-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}
.acervo-table th,
.acervo-table td {
  border: 1px solid #ccc;
  padding: 8px;
}
.btn-edit {
  background: #ffeb3b;
  border: none;
  padding: 4px 8px;
  cursor: pointer;
  margin-right: 4px;
}
.btn-delete {
  background: #f44336;
  border: none;
  padding: 4px 8px;
  cursor: pointer;
  color: white;
}
</style>
