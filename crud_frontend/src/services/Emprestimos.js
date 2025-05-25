// src/services/emprestimos.js
import axios from 'axios'

export default {
  listarMeus() {
    return axios.get('/meus-livros')
  }
}
