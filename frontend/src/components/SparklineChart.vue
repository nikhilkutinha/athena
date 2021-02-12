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

  data () {
    return {
      chartOptions: {
        plotOptions: {
          series: {
            lineColor: '#fff',
            lineWidth: 4,
            color: '#fff',
            fillOpacity: 0.3,
            enableMouseTracking: false
          }
        },
        chart: {
          type: 'area',
          backgroundColor: null,
          height: 100,
          margin: 0
        },

        xAxis: {
          labels: {
            enabled: false
          },
          title: {
            text: null
          },
          startOnTick: false,
          endOnTick: false,
          tickPositions: [],
          maxPadding: 0
        },

        yAxis: {
          endOnTick: false,
          startOnTick: false,
          labels: {
            enabled: false
          },
          title: {
            text: null
          },
          tickPositions: [0]
        },
        series: [{ data: this.series }]
      }
    }
  }
}
</script>
