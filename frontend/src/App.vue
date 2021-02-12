<template>
  <div id="app" class="has-background-light">
    <div class="has-background-white">
      <TheNavbar />
    </div>

    <router-view />
  </div>
</template>

<script>
import TheNavbar from '@/components/TheNavbar'
export default {
  components: {
    TheNavbar
  },

  data () {
    return {
      loading: true,
      troubleshooting: false
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/app.scss";

#app {
  min-height: 100vh;
}
</style>
