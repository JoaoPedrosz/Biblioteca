// src/services/livros.js
import axios from 'axios'

const base = '/livros'

export default {
  // GET /livros
  listar() {
    return axios.get(base)
  },

  // POST /livros  (com FormData para upload de arquivo)
  criar(formData) {
    return axios.post(base, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // PUT /livros/:id
  atualizar(id, dados) {
    return axios.put(`${base}/${id}`, dados)
  },

  // DELETE /livros/:id
  remover(id) {
    return axios.delete(`${base}/${id}`)
  },

  // DELETE /livros/isbn/:isbn
  removerPorIsbn(isbn) {
    return axios.delete(`${base}/isbn/${isbn}`)
  }
}
