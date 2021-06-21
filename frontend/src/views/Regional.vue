<template>
  <div>
    <b-loading
      :is-full-page="true"
      v-model="loading"
      :can-cancel="false"
    ></b-loading>

    <the-header v-if="name" :name="name"></the-header>

    <section class="container px-3 py-5">
      <div v-if="timeline" class="columns is-multiline">
        <div
          v-for="(figures, name) in timeline"
          :key="name"
          class="column is-6-tablet is-3-widescreen"
        >
          <data-view-card
            :name="name"
            :timeline="figures.cumulative"
          ></data-view-card>
        </div>
      </div>
    </section>

    <section v-if="timeline" class="container px-3 py-5">
      <data-view-panel
        v-for="(figures, name) in timeline"
        :key="name"
        :name="name"
        :timeline="figures"
      ></data-view-panel>
    </section>
  </div>
</template>

<script>
import DataViewCard from '@/components/DataViewCard'
import DataViewPanel from '@/components/DataViewPanel'
import TheHeader from '@/components/TheHeader'

import AsyncMixin from '@/utils/AsyncMixin'
import TimelineMixin from '@/utils/TimelineMixin'

import axios from 'axios'
import { API_BASE_URL } from '@/config.js'

export default {
  props: {
    id: [String, Number]
  },

  mixins: [AsyncMixin, TimelineMixin],

  components: {
    TheHeader,
    DataViewCard,
    DataViewPanel
  },

  data () {
    return {
      name: '',
      reports: []
    }
  },

  watch: {
    $route: 'loadAsyncData'
  },

  computed: {},

  mounted () {
    this.loadAsyncData()
  },

  methods: {
    fixNegativeNumber (value) {
      if (value < 0) return 0
      return value
    },

    loadAsyncData () {
      this.isLoading(true)
      this.$emit('loading')

      axios
        .get(`${API_BASE_URL}/countries/${this.id}`)
        .then((res) => {
          const data = res.data
          this.name = data.name
          this.reports = data.reports
        })
        .catch((err) => {
          this.isTroubleshooting(true)
          throw new Error(`Server error. ${err}`)
        })
        .finally(() => {
          this.isLoading(false)
        })
    }
  }
}
</script>
