<template>
  
</template>

<script>
export default {
  name: 'BookForm',
  data() {
    return {
      form: { /* campos do livro */ },
      file: null
    }
  },
  methods: {
    onFileChange(e) { this.file = e.target.files[0] },
    async onSubmit() { /* POST /livros */ }
  }
}
</script>

<style scoped>
  /* cole aqui o CSS original da Tela22 */
</style>
