<script>
export default {
  props: {
    series: Array
  },

  watch: {
    series: function () {
      this.chartOptions.series = this.series
    }
  },

  data () {
    return {
      chartOptions: {
        credits: {
          enabled: false
        },
        xAxis: {
          type: 'datetime'
        },

        yAxis: {
          title: {
            enabled: false
          }
        },

        legend: {
          enabled: false
        },

        title: {
          text: null
        },

        series: {
          name: '',
          data: []
        },

        chart: {
          type: '',
          style: {
            fontFamily: 'Roboto, sans-serif'
          }
        }
      }
    }
  }
}
</script>
