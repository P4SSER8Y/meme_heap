
const routes = [
  {
    path: '/',
    component: () => import('pages/Gallery.vue'),
    props: route => {
      t: route.query.token ? route.query.token : ""
    }
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
