<template>
  <b-table
    class="panel"
    v-if="tabulated"
    :data="tabulated"
    striped
    sort-icon="arrow-up"
    sort-icon-size="is-small"
    icon-pack="mdi"
    default-sort="confirmed"
    default-sort-direction="desc"
  >
    <b-table-column
      cell-class="flag-wrap"
      field="flag"
      label="#"
      v-slot="props"
    >
      <figure class="flag">
        <img
          :src="props.row.flag"
          @error="$event.target.src=require('@/assets/img/default_flag.svg')"
        />
      </figure>
    </b-table-column>

    <b-table-column field="name" label="Name" sortable v-slot="props">
      <router-link
        class="has-text-black"
        :to="{ name: 'region', params: { id: props.row.id } }"
      >
        {{ props.row.name }}
      </router-link>
    </b-table-column>

    <b-table-column
      field="confirmed"
      label="confirmed"
      numeric
      sortable
      v-slot="props"
    >
      {{ props.row.confirmed || "NA" }}
    </b-table-column>

    <b-table-column
      field="recovered"
      label="recovered"
      numeric
      sortable
      v-slot="props"
    >
      {{ props.row.recovered || "NA" }}
    </b-table-column>

    <b-table-column
      field="active"
      label="active"
      numeric
      sortable
      v-slot="props"
    >
      {{ props.row.active || "NA" }}
    </b-table-column>

    <b-table-column
      field="deaths"
      label="deaths"
      numeric
      sortable
      v-slot="props"
    >
      {{ props.row.deaths || "NA" }}
    </b-table-column>
  </b-table>
</template>

<script>
export default {
  props: {
    tabulated: Array
  }
}
</script>

<style>
.table th {
  padding: 0.7em 0.75em !important;
  color: hsl(0, 0%, 30%) !important;
  font-weight: 500 !important;
  text-transform: uppercase;
  font-size: 0.9em;
}

.is-current-sort > .th-wrap.is-numeric > span {
  transform: translateX(-18px);
  transition: transform 150ms ease-out, opacity 86ms ease-out;
}

.is-current-sort > .th-wrap.is-numeric .sort-icon {
  left: 110%;
}

.flag > img {
  display: block;
  min-width: 32px;
  height: 24px;
}

.flag-wrap {
  width: 0.1%;
  white-space: nowrap;
}
</style>
