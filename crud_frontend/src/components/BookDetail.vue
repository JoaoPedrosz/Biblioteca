<!-- src/components/BookDetail.vue -->
<template>
  <div class="book-detail-view">
    <!-- Book Area -->
    <section class="book-area">
      <img
        class="book-cover"
        :src="book.arquivo
          ? `${apiBase}/static/uploads/${book.arquivo}`
          : placeholder"
        :alt="`Capa de ${book.nome}`"
      />
      <div class="book-details">
        <h1 class="book-title">{{ book.nome }}</h1>
        <div class="book-meta">
          {{ book.edicao }} | Por {{ book.autor }}<br />
          <span v-if="book.categoria">Categoria: {{ book.categoria }}</span>
        </div>
        <div class="book-actions">
          <button class="btn-primary" @click="reservar">Reservar</button>
          <button class="btn-secondary" @click="showModal = true">
            Gerar QR Code
          </button>
        </div>
        <span
          class="book-status"
          :class="{ unavailable: !book.disponivel }"
        >
          {{ book.disponivel ? 'Disponível' : 'Indisponível' }}
        </span>
      </div>
    </section>

    <!-- Details Content -->
    <section class="details-content">
      <h2>Visão Geral</h2>
      <h3>Descrição</h3>
      <p>{{ book.descricao }}</p>
      <h3>Informações Sobre O Livro</h3>
      <ul>
        <li>Páginas: {{ book.paginas }}</li>
        <li>Editora: {{ book.editora }}</li>
        <li>Edição: {{ book.edicao }}</li>
        <li>Idioma: {{ book.idioma }}</li>
        <li>ISBN: {{ book.isbn }}</li>
        <li v-if="book.categoria">Categoria(s): {{ book.categoria }}</li>
      </ul>
    </section>

    <!-- Modal QR Code -->
    <div v-if="showModal" class="modal-bg" @click.self="showModal = false">
      <div class="modal">
        <button class="modal-close" @click="showModal = false">&times;</button>
        <h3 class="modal-title">QR CODE</h3>
        <p class="modal-info">
          Apresente esse QR Code para retirar o livro na biblioteca.
        </p>
        <div class="qr-code-block">
          <canvas ref="qrCanvas"></canvas>
        </div>
        <button class="btn-save" @click="saveQR">Salvar</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import QRious from 'qrious'
const placeholder = require('@/assets/IconeLivro.png')

export default {
  name: 'BookDetail',
  props: ['isbn'],
  data() {
    return {
      book: {},
      placeholder,
      apiBase: axios.defaults.baseURL,
      showModal: false,
      qrText: ''
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
      .get(`/livros/isbn/${this.isbn}`)
      .then(({ data }) => {
        this.book = data
      })
      .catch(() => {
        alert('Não foi possível carregar os detalhes do livro.')
        this.$router.back()
      })
  },
  methods: {
    reservar() {
      axios
        .post(`/reservar/${this.book.isbn}`)
        .then(({ data }) => {
          this.qrText = data.qr_text
          this.showModal = true
        })
        .catch(err => {
          let msg = 'Erro ao reservar.'
          if (err.response && err.response.data && err.response.data.erro) {
            msg = err.response.data.erro
          }
          alert(msg)
        })
    },
    drawQR() {
      /* eslint-disable-next-line no-new */
      new QRious({
        element: this.$refs.qrCanvas,
        value: this.qrText,
        size: 180,
        level: 'H'
      })
    },
    saveQR() {
      const link = document.createElement('a')
      link.href = this.$refs.qrCanvas.toDataURL('image/png')
      link.download = 'qrcode.png'
      link.click()
    }
  },
  watch: {
    showModal(val) {
      if (val) this.$nextTick(this.drawQR)
    }
  }
}
</script>

<style scoped>
.book-detail-view {
  padding: 20px;
  background: #fff;
}
/* Book Area */
.book-area {
  display: flex;
  background: #202b36;
  color: #fff;
  padding: 40px;
  border-radius: 8px;
  position: relative;
}
.book-cover {
  width: 200px;
  height: 280px;
  object-fit: cover;
  margin-right: 24px;
  border-radius: 4px;
}
.book-details {
  flex: 1;
}
.book-title {
  font-size: 2rem;
  margin: 0 0 8px;
}
.book-meta {
  color: #ccc;
  margin-bottom: 16px;
}
.book-actions button {
  margin-right: 12px;
  padding: 8px 24px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.btn-primary { background: #f28b4b; color: #fff; }
.btn-secondary { background: #35d48c; color: #fff; }
.book-status {
  position: absolute;
  top: 16px; right: 16px;
  padding: 4px 12px; border-radius: 12px;
  background: #30e492; color: #fff;
}
.book-status.unavailable {
  background: #d9534f;
}
/* Details */
.details-content {
  margin-top: 24px;
}
.details-content h2 { margin-bottom: 16px; }
.details-content ul { list-style: disc inside; }
/* Modal */
.modal-bg {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.3);
  display: flex; justify-content: center; align-items: center;
}
.modal {
  background: #fff; padding: 24px;
  border-radius: 8px; width: 300px; position: relative;
  text-align: center;
}
.modal-close {
  position: absolute; top: 8px; right: 8px;
  border: none; background: none; font-size: 1.2rem; cursor: pointer;
}
.qr-code-block { margin: 16px 0; }
.btn-save {
  background: #222; color: #fff;
  padding: 8px 24px; border: none; border-radius: 4px;
  cursor: pointer;
}
</style>
