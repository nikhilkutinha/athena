<template>
  <section
    class="hero has-background-image overlay"
    :style="{ backgroundImage: 'url(' + require('@/assets/img/header.jpg') + ')' }"
  >
    <div class="hero-body">
      <div class="container px-3">
        <h2 class="title has-text-weight-medium has-text-white">{{ name }}</h2>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  props: {
    name: String
  },

  data () {
    return {
      backdrop: ''
    }
  },

  watch: {
    name: function () {
      /**
       *  Pull backdrop image for page header
       *  from unsplash. Disabled for now.
       */
      const res = '1920x200'
      const url = new URL(`https://source.unsplash.com/${res}/`)
      url.searchParams.set('q', this.name)

      this.backdrop = url
    }
  }
}
</script>

<style>
.has-background-image {
  background-position: center center;
  background-size: cover;
}

.has-background-image.overlay {
  position: relative;
  z-index: 1;
}

.has-background-image.overlay .hero-body {
  z-index: 3;
}

.has-background-image.overlay:before {
  content: "";
  width: 100%;
  height: 100%;
  position: absolute;
  z-index: 2;
  top: 0;
  left: 0;
  background: transparent linear-gradient(270deg, #00000000 0%, #000000f2 100%)
    0% 0% no-repeat padding-box;
}
</style>
