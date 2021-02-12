<template>
  <b-autocomplete
    v-model="name"
    placeholder="e.g. Australia"
    :keep-first="keepFirst"
    :open-on-focus="openOnFocus"
    :data="filteredRegions"
    :clear-on-select="true"
    field="name"
    :clearable="clearable"
    @select="(option) => (selected = option)"
  >
    <template slot-scope="props">
      {{ props.option.name }}
    </template>
  </b-autocomplete>
</template>

<script>
import axios from 'axios'
import { API_BASE_URL } from '@/config.js'

export default {
  data () {
    return {
      regions: [],
      keepFirst: false,
      openOnFocus: false,
      name: '',
      selected: '',
      clearable: false,
      loading: true,
      troubleshooting: false
    }
  },

  mounted () {
    this.loadAsyncData()
  },

  watch: {
    selected: function () {
      if (!this.selected) return

      this.$router.push({ name: 'region', params: { id: this.selected.id } })
    }
  },

  computed: {
    filteredRegions () {
      return this.regions.filter((option) => {
        return (
          option.name
            .toString()
            .toLowerCase()
            .indexOf(this.name.toLowerCase()) >= 0
        )
      })
    }
  },

  methods: {
    loadAsyncData () {
      axios
        .get(`${API_BASE_URL}/countries`)
        .then((res) => {
          this.regions = res.data
        })
        .catch((err) => {
          this.troubleshooting = true
          throw new Error(`Server error. ${err}`)
        })
        .finally(() => {
          this.loading = false
        })
    }
  }
}
</script>

<style>
.autocomplete {
  display: flex;
  align-items: center;
  width: 300px;
}

.autocomplete .control {
  flex: 1
}

.autocomplete .input {
  border: 1px solid #d4d4d4;
  box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075);
}
</style>
