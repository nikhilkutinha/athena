<script>
import _ from 'lodash'

export default {
  data () {
    return {
      reports: []
    }
  },

  methods: {
    genKeys () {
      const graphTypes = { cumulative: [], discrete: [] }
      const figures = { confirmed: {}, deaths: {}, recovered: {}, active: {} }

      /**
       * The following are keys that represent data
       * we will be plotting on an area chart. To
       * obtain column chart keys exclude "active".
       *
       */

      Object.keys(figures).forEach((key) => {
        figures[key] = _.cloneDeep(graphTypes)
      })

      return figures
    },

    findActive ({ confirmed, deaths, recovered }) {
      return confirmed - (recovered + deaths)
    },

    fixNegativeNumber: (val) => (val < 0 ? 0 : val)
  },

  computed: {
    timeline () {
      if (!this.reports.length) return

      const figures = this.genKeys()

      this.reports.forEach((report, i) => {
        const date = Date.parse(report.date)

        report.active = this.findActive(report)

        Object.entries(report).forEach(([key, val]) => {
          report[key] = this.fixNegativeNumber(val)
        })

        Object.keys(figures).forEach((key) => {
          figures[key].cumulative.push([date, report[key]])

          if (key !== 'active') {
            if (i > 0) {
              const prev = this.reports[i - 1][key]
              let diff = report[key] - prev
              diff = this.fixNegativeNumber(diff)
              figures[key].discrete.push([date, diff])
            }
          }
        })
      })

      return figures
    }
  }
}
</script>
