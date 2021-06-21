<template>
  <div class="panel is-info">
    <p class="panel-heading has-text-weight-normal ">
      {{ name | capitalize }} Timeline
    </p>
    <div class="has-background-white">
      <b-tabs v-model="activeTab">
        <b-tab-item v-if="daily.data.length" label="Daily">
          <column-chart class="mt-5" :series="daily"></column-chart>
        </b-tab-item>
        <b-tab-item label="Total">
          <area-chart class="mt-5" :series="total"></area-chart>
        </b-tab-item>
      </b-tabs>
    </div>
  </div>
</template>

<script>
import ColumnChart from './ColumnChart'
import AreaChart from './AreaChart'

export default {
  components: {
    ColumnChart,
    AreaChart
  },

  props: {
    name: String,
    timeline: [Array, Object]
  },

  filters: {
    capitalize: (value) => {
      if (!value) return ''

      value = value.toString()
      return value.charAt(0).toUpperCase() + value.slice(1)
    }
  },

  data () {
    return {
      activeTab: 0
    }
  },

  computed: {
    daily () {
      const data = this.timeline.discrete
      const label = 'daily ' + (this.name === 'confirmed' ? 'cases' : this.name)

      return { data, name: label }
    },

    total () {
      const data = this.timeline.cumulative
      const label = 'total ' + (this.name === 'confirmed' ? 'cases' : this.name)

      return { data, name: label }
    }
  }
}
</script>

<style>
.tabs {
  padding: 16px 26px !important;
}
</style>
