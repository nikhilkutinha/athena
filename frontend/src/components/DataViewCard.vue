<template>
  <div class="card" :class="colorClass">
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

  filters: {
    humanizeNumber (value) {
      if (!value) return 'NA'

      return value.toLocaleString()
    }
  },

  computed: {
    latest () {
      if (!this.timeline) return
      return this.timeline.slice(-1)[0][1]
    },

    colorClass () {
      return 'has-background-' + {
        recovered: 'success',
        deaths: 'danger',
        confirmed: 'info',
        active: 'warning'
      }[this.name]
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
