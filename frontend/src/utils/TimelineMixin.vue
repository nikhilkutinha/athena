<script>
import _ from 'lodash'

export default {
  data () {
    return {
      reports: []
    }
  },

  methods: {
    prepareFigures () {
      const graphTypes = { cumulative: [], discrete: [] }
      const figures = {
        confirmed: {},
        deaths: {},
        recovered: {},
        active: {}
      }

      /**
       * The following are keys that represent data
       * we will be plotting on an area chart. To
       * obtain column chart keys exclude "active".
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

      const figures = this.prepareFigures()

      this.reports.forEach((report, i) => {
        const date = Date.parse(report.date)

        report.active = this.findActive(report)

        Object.entries(report).forEach(([name, figure]) => {
          report[name] = this.fixNegativeNumber(figure)
        })

        Object.keys(figures).forEach((name) => {
          figures[name].cumulative.push([date, report[name]])

          if (name !== 'active') {
            if (i > 0) {
              const prev = this.reports[i - 1][name]
              let diff = report[name] - prev
              diff = this.fixNegativeNumber(diff)
              figures[name].discrete.push([date, diff])
            }
          }
        })
      })

      return figures
    }
  }
}
</script>
