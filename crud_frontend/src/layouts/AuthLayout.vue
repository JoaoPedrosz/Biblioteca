<!-- src/layouts/AuthLayout.vue -->
<template>
  <div class="auth‐layout">
    <router-view/>
  </div>
</template>
<script>
export default {
  name: 'AuthLayout'
}
</script>
<style>
/* Se quiser, centralize o conteúdo verticalmente */
.auth‐layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
