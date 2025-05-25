<!-- src/components/BookForm.vue -->
<template>
  <div class="admin-content">
    <h1>Cadastrar Livro</h1>
    <form @submit.prevent="cadastrarLivro" enctype="multipart/form-data">
      <div class="cadastro-fields">
        <div class="form-group">
          <label>Nome do Livro</label>
          <input v-model="livro.nome" type="text" placeholder="Nome do Livro" required />
        </div>
        <div class="form-group">
          <label>Número de Páginas</label>
          <input v-model="livro.paginas" type="number" placeholder="Número de Páginas" required />
        </div>
        <div class="form-group">
          <label>Nome do Autor</label>
          <input v-model="livro.autor" type="text" placeholder="Nome do Autor" required />
        </div>
        <div class="form-group">
          <label>Idioma</label>
          <input v-model="livro.idioma" type="text" placeholder="Idioma" required />
        </div>
        <div class="form-group">
          <label>Código ISBN</label>
          <input v-model="livro.isbn" type="text" maxlength="13" placeholder="13 dígitos" required />
        </div>
        <div class="form-group">
          <label>Categoria(s)</label>
          <input v-model="livro.categoria" type="text" placeholder="Categoria" />
        </div>
        <div class="form-group">
          <label>Nome da Editora</label>
          <input v-model="livro.editora" type="text" placeholder="Nome da Editora" />
        </div>
        <div class="form-group">
          <label>Edição</label>
          <input v-model="livro.edicao" type="text" placeholder="Edição" />
        </div>
        <div class="form-group file-group">
          <label>Upload do Livro</label>
          <input
            ref="upload"
            type="file"
            @change="onFileChange"
            style="display:none"
          />
          <button type="button" class="file-btn" @click="$refs.upload.click()">
            Escolher Arquivo
          </button>
          <span v-if="livro.arquivoNome" class="file-name">{{ livro.arquivoNome }}</span>
        </div>
      </div>

      <div class="form-group full-width">
        <label>Descrição</label>
        <textarea
          v-model="livro.descricao"
          maxlength="400"
          placeholder="Descrição"
        ></textarea>
        <div class="desc-helper">Deve ter no máximo 400 caracteres</div>
      </div>

      <button type="submit" class="btn-primary">Cadastrar</button>
    </form>

    <hr />

    <div class="remove-section">
      <h2>Remover Livro</h2>
      <form @submit.prevent="removerLivro">
        <div class="form-group">
          <label>Informe o Código ISBN</label>
          <input v-model="removerISBN" type="text" placeholder="Código" required />
        </div>
        <button type="submit" class="btn-danger">Remover</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BookForm',
  data() {
    return {
      livro: {
        nome: '',
        paginas: '',
        autor: '',
        idioma: '',
        isbn: '',
        categoria: '',
        editora: '',
        edicao: '',
        arquivoNome: '',
        descricao: ''
      },
      file: null,
      removerISBN: ''
    }
  },
  methods: {
    onFileChange(e) {
      const f = e.target.files[0]
      if (f) {
        this.file = f
        this.livro.arquivoNome = f.name
      }
    },
    async cadastrarLivro() {
      try {
        const fd = new FormData()
        Object.entries(this.livro).forEach(([k, v]) => fd.append(k, v))
        if (this.file) fd.append('arquivo', this.file)
        await this.$axios.post('/livros', fd)
        alert('Livro cadastrado com sucesso!')
        Object.keys(this.livro).forEach(k => (this.livro[k] = ''))
        this.file = null
      } catch (err) {
        alert('Erro ao cadastrar livro.')
      }
    },
    async removerLivro() {
      try {
        await this.$axios.delete(`/livros/${this.removerISBN}`)
        alert('Livro removido com sucesso!')
        this.removerISBN = ''
      } catch (err) {
        alert('Erro ao remover livro.')
      }
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
.cadastro-fields {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}
.form-group {
  flex: 1 1 300px;
  display: flex;
  flex-direction: column;
}
.form-group.full-width { flex-basis: 100%; }
.file-group { flex-basis: 45%; }
.form-group label { font-weight: 600; margin-bottom: 6px; }
.form-group input,
.form-group textarea {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.file-btn {
  background: #efefef;
  border: 1px solid #ccc;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
}
.file-name { margin-top: 4px; color: #555; }
.desc-helper { font-size: 0.9rem; color: #777; margin-top: 4px; }
.btn-primary {
  background: #222;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 12px;
}
hr { margin: 30px 0; }
.remove-section h2 { margin-bottom: 12px; }
.btn-danger {
  background: #c62828;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
</style>
