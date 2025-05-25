<template>
  <div class="admin-content">
    <h1>{{ isEdit ? 'Editar Livro' : 'Cadastrar Livro' }}</h1>
    <form @submit.prevent="salvarLivro" enctype="multipart/form-data">
      <div class="cadastro-fields">
        <!-- Nome -->
        <div class="form-group">
          <label>Nome do Livro</label>
          <input
            v-model="livro.nome"
            type="text"
            placeholder="Nome do Livro"
            required
          />
        </div>

        <!-- Páginas -->
        <div class="form-group">
          <label>Número de Páginas</label>
          <input
            v-model="livro.paginas"
            type="number"
            placeholder="Número de Páginas"
            required
          />
        </div>

        <!-- Autor -->
        <div class="form-group">
          <label>Nome do Autor</label>
          <input
            v-model="livro.autor"
            type="text"
            placeholder="Nome do Autor"
            required
          />
        </div>

        <!-- Idioma -->
        <div class="form-group">
          <label>Idioma</label>
          <input
            v-model="livro.idioma"
            type="text"
            placeholder="Idioma"
            required
          />
        </div>

        <!-- ISBN -->
        <div class="form-group">
          <label>Código ISBN</label>
          <input
            v-model="livro.isbn"
            :readonly="isEdit"
            type="text"
            maxlength="13"
            placeholder="13 dígitos"
            required
          />
        </div>

        <!-- Categoria -->
        <div class="form-group">
          <label>Categoria(s)</label>
          <input
            v-model="livro.categoria"
            type="text"
            placeholder="Categoria"
          />
        </div>

        <!-- Editora -->
        <div class="form-group">
          <label>Nome da Editora</label>
          <input
            v-model="livro.editora"
            type="text"
            placeholder="Nome da Editora"
          />
        </div>

        <!-- Edição -->
        <div class="form-group">
          <label>Edição</label>
          <input
            v-model="livro.edicao"
            type="text"
            placeholder="Edição"
          />
        </div>

        <!-- Disponível -->
        <div class="form-group">
          <label>
            <input
              type="checkbox"
              v-model="livro.disponivel"
            />
            Disponível para empréstimo
          </label>
        </div>

        <!-- Upload do arquivo -->
        <div class="form-group file-group">
          <label>Upload do Livro (PDF ou imagem)</label>
          <input
            ref="upload"
            type="file"
            @change="onFileChange"
            style="display:none"
            accept=".pdf,image/*"
          />
          <button
            type="button"
            class="file-btn"
            @click="$refs.upload.click()"
          >
            Escolher Arquivo
          </button>
          <span v-if="livro.arquivoNome" class="file-name">
            {{ livro.arquivoNome }}
          </span>
        </div>
      </div>

      <!-- Descrição -->
      <div class="form-group full-width">
        <label>Descrição</label>
        <textarea
          v-model="livro.descricao"
          maxlength="400"
          placeholder="Descrição"
        ></textarea>
        <div class="desc-helper">Deve ter no máximo 400 caracteres</div>
      </div>

      <!-- Botão salvar -->
      <button type="submit" class="btn-primary">
        {{ isEdit ? 'Atualizar' : 'Cadastrar' }}
      </button>
    </form>

    <hr v-if="isEdit" />

    <!-- Seção remover por ISBN (apenas no cadastro, não em edição) -->
    <div class="remove-section" v-if="!isEdit">
      <h2>Remover Livro</h2>
      <form @submit.prevent="removerLivro">
        <div class="form-group">
          <label>Informe o Código ISBN</label>
          <input
            v-model="removerISBN"
            type="text"
            placeholder="Código"
            required
          />
        </div>
        <button type="submit" class="btn-danger">Remover</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BookForm',
  props: {
    id: { type: String, default: null }
  },
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
        descricao: '',
        disponivel: true
      },
      file: null,
      removerISBN: ''
    }
  },
  computed: {
    isEdit() {
      return !!this.id
    }
  },
  created() {
    if (this.isEdit) {
      // Carrega dados existentes para edição
      this.$axios.get(`/livros/${this.id}`)
        .then(res => {
          Object.assign(this.livro, {
            ...res.data,
            arquivoNome: res.data.arquivo_nome || ''
          })
        })
        .catch(() => {
          alert('Erro ao carregar dados do livro.')
          this.$router.back()
        })
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
    async salvarLivro() {
      try {
        const fd = new FormData()
        Object.entries(this.livro).forEach(([k, v]) => {
          fd.append(k, v)
        })
        if (this.file) {
          fd.append('arquivo', this.file)
        }

        if (this.isEdit) {
          await this.$axios.put(`/livros/${this.id}`, fd, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
          alert('Livro atualizado com sucesso!')
        } else {
          await this.$axios.post('/livros', fd, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
          alert('Livro cadastrado com sucesso!')
          this.resetForm()
        }

        this.$router.push({ name: 'AdminAcervo' })
      } catch (err) {
        let msg = 'Erro ao salvar livro.'
        if (
          err.response &&
          err.response.data &&
          err.response.data.erro
        ) {
          msg = err.response.data.erro
        }
        alert(msg)
      }
    },
    resetForm() {
      this.livro = {
        nome: '',
        paginas: '',
        autor: '',
        idioma: '',
        isbn: '',
        categoria: '',
        editora: '',
        edicao: '',
        arquivoNome: '',
        descricao: '',
        disponivel: true
      }
      this.file = null
    },
    async removerLivro() {
      try {
        await this.$axios.delete(`/livros/isbn/${this.removerISBN}`)
        alert('Livro removido com sucesso!')
        this.removerISBN = ''
      } catch (err) {
        let msg = 'Erro ao remover livro.'
        if (
          err.response &&
          err.response.data &&
          err.response.data.erro
        ) {
          msg = err.response.data.erro
        }
        alert(msg)
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
.form-group.full-width {
  flex-basis: 100%;
}
.file-group {
  flex-basis: 45%;
}
.form-group label {
  font-weight: 600;
  margin-bottom: 6px;
}
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
.file-name {
  margin-top: 4px;
  color: #555;
}
.desc-helper {
  font-size: 0.9rem;
  color: #777;
  margin-top: 4px;
}
.btn-primary {
  background: #222;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 12px;
}
.btn-danger {
  background: #c62828;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
.remove-section {
  margin-top: 40px;
}
.remove-section h2 {
  margin-bottom: 12px;
}
</style>
