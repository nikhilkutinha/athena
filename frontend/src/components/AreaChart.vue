<template>
  <Chart :options="chartOptions" />
</template>

<script>
import { Chart } from 'highcharts-vue'
import ChartMixin from '@/utils/ChartMixin'

export default {
  mixins: [ChartMixin],

  components: {
    Chart
  },

  props: {
    series: Object
  },

  data () {
    return {
      chartOptions: {
        chart: {
          type: 'area'
        },
        series: [this.series]
      }
    }
  }
}
</script>
