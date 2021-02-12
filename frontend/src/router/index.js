import Vue from 'vue'
import VueRouter from 'vue-router'
import Regional from '@/views/Regional.vue'
import Global from '@/views/Global.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/region/:id',
    name: 'region',
    component: Regional,
    props: true
  },
  {
    path: '/',
    name: 'global',
    component: Global,
    props: true
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
