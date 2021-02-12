<template>
  <div class="card" :class="color">
    <div class="card-content">
      <header class="is-uppercase is-size-7">
        {{ name }}
      </header>
      <div class="content has-text-white is-size-3">
        {{ latest | humanizeNumber }}
      </div>
    </div>

    <footer class="card-footer">
      <sparkline-chart :series="timeline"></sparkline-chart>
    </footer>
  </div>
</template>

<script>
import SparklineChart from './SparklineChart'

export default {
  props: {
    name: String,
    timeline: [Array, Object]
  },

  components: {
    SparklineChart
  },

  data () {
    return {}
  },

  // data() {
  //   return {
  //     chartOptions: {
  //       tooltip: {
  //         enabled: false,
  //       },
  //       stroke: {
  //         curve: "smooth",
  //       },
  //       chart: {
  //         id: "sparkline",
  //         sparkline: {
  //           enabled: true,
  //         },
  //       },
  //       fill: {
  //         type: "solid",
  //         colors: ["#fff"],
  //         opacity: 0.3,
  //       },
  //       colors: ["#fff"],
  //     },

  //     series: [
  //       {
  //         name: "timeline",
  //         data: this.timeline,
  //       },
  //     ],
  //   };
  // },

  filters: {
    /**
     * Adds commas to large numbers
     * to make them more readable.
     */

    humanizeNumber (value) {
      if (!value) return 'NA'

      return value.toLocaleString()
    }
  },

  computed: {
    /**
     * Get last report from the timeline
     * array.
     */

    latest () {
      if (!this.timeline) return
      return this.timeline.slice(-1)[0][1]
    },

    /**
     * Determine card color based on
     * name passed in.
     */

    color () {
      const base = 'has-background'
      switch (this.name) {
        case 'recovered':
          return `${base}-success`
        case 'deaths':
          return `${base}-danger`
        case 'confirmed':
          return `${base}-info`
        case 'active':
          return `${base}-warning`
        default:
          return ''
      }
    }
  }
}
</script>

<style>
.card-content header {
  letter-spacing: 0.15em;
  color: rgba(255, 255, 255, 0.65);
}

.card-footer {
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  display: block;
}
</style>
