<template>
  <div>
    <b-loading
      :is-full-page="true"
      v-model="loading"
      :can-cancel="false"
    ></b-loading>

    <the-header v-if="title" :name="title"></the-header>

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

    <section class="container px-3 py-5">
      <data-view-table :tabulated="tabulated"></data-view-table>
    </section>
  </div>
</template>

<script>
import DataViewCard from '@/components/DataViewCard'
import DataViewTable from '@/components/DataViewTable'
import TheHeader from '@/components/TheHeader'
import AsyncMixin from '@/utils/AsyncMixin'
import TimelineGenMixin from '@/utils/TimelineGenMixin'

import axios from 'axios'
import { API_BASE_URL } from '@/config.js'

export default {
  components: {
    TheHeader,
    DataViewCard,
    DataViewTable
  },

  mixins: [AsyncMixin, TimelineGenMixin],

  data () {
    return {
      title: '',
      reports: [],
      countryLatest: []
    }
  },

  watch: {
    $route: 'fetchData'
  },

  mounted () {
    this.loadAsyncData()
  },

  computed: {
    tabulated () {
      if (!this.countryLatest.length) return

      const latest = this.countryLatest.map((cty) => {
        const latestReport = { ...cty.latest }
        const { confirmed, recovered, deaths } = latestReport

        latestReport.active = confirmed - (recovered + deaths)

        Object.entries(latestReport).forEach(([key, val]) => {
          latestReport[key] = this.fixNegativeNumber(val)
        })

        return { ...latestReport, id: cty.id, name: cty.name, flag: cty.flag }
      })

      return latest
    }
  },

  methods: {
    loadAsyncData () {
      this.isLoading(true)

      const urls = [
        axios.get(`${API_BASE_URL}/global`),
        axios.get(`${API_BASE_URL}/all`)
      ]

      /**
       * Finally we fetch from the above
       * endpoints together.
       */
      axios
        .all(urls)
        .then(
          axios.spread((first, second) => {
            this.reports = first.data
            this.countryLatest = second.data
            this.title = 'World'
          })
        )
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
