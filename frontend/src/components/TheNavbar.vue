<template>
  <b-navbar class="container">
    <template slot="brand">
      <b-navbar-item tag="router-link" class="mr-2" :to="{ path: '/' }">
        <img src="@/assets/img/logo.svg" alt="Athena Logo" />
      </b-navbar-item>

      <searchbox class="is-hidden-desktop"></searchbox>

    </template>

    <template slot="start">
      <b-navbar-item tag="router-link" :to="{ path: '/' }">
        Home
      </b-navbar-item>
      <b-navbar-item tag="a" target="_blank" :href="about_href">
        About
      </b-navbar-item>
    </template>

    <template slot="end">
      <searchbox class="pr-3 is-hidden-touch"></searchbox>
    </template>
  </b-navbar>
</template>

<script>
import Searchbox from '@/components/Searchbox'
import { homepage } from '@/../package.json'

export default {
  components: {
    Searchbox
  },
  data() {
    return {
      about_href: homepage
    }
  }
}
</script>

<style>
.navbar-brand {
  justify-content: space-between;
}

.navbar-burger {
  margin-left: 0px !important;
}
</style>
