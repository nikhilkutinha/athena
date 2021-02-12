<script>
export default {
  data () {
    return {
      loading: true,
      troubleshooting: false
    }
  },

  methods: {
    isLoading (value) {
      this.loading = value
      this.$emit('loading', value)
    },

    isTroubleshooting (value) {
      this.troubleshooting = value
      this.$emit('error', value)
    }
  }
}
</script>
