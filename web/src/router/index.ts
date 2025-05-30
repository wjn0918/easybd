import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/tools',
    component: () => import('@/components/tools/index.vue'),
    children: [
      {
        path: 'database-tool',
        name: 'DatabaseTool',
        component: () => import("@/components/tools/dbTools/excel2sql.vue")
      },
      {
        path: 'excel2datax',
        name: 'excel2datax',
        component: () => import("@/components/tools/dbTools/excel2datax.vue")
      },
    ]
  },
  // {
  //   path: '/company',
  //   component: () => import('@/components/shingi/index.vue'),
  //   children: [
  //     {
  //       path: 'source',
  //       name: 'CompanySource',
  //       component: () => import("@/components/shingi/source.vue")
  //     },
  //     {
  //       path: 'hik',
  //       name: 'CompanySource',
  //       component: () => import("@/components/shingi/hik/index.vue")
  //     },
  //     {
  //       path: 'jz',
  //       name: 'CompanySource',
  //       component: () => import("@/components/shingi/jz/index.vue")
  //     },
  //   ]
  // },
  // {
  //   path: '/dbCenter',
  //   component: () => import('@/components/dbCenter/index.vue'),
    
  // },
  {
    path: '/configCenter',
    component: () => import('@/components/configCenter/index.vue'),
    children: [
      {
        path: 'datax',
        name: 'datax',
        component: () => import("@/components/configCenter/datax/index.vue")
      },
      {
        path: 'dolphinscheduler',
        name: 'dolphinscheduler',
        component: () => import("@/components/configCenter/dolphinscheduler/index.vue")
      },
      {
        path: 'common',
        name: 'common',
        component: () => import("@/components/configCenter/common/index.vue")
      },
      {
        path: 'jdbc',
        name: 'jdbc',
        component: () => import("@/components/configCenter/jdbc/index.vue")
      },
      {
        path: 'hikapi',
        name: 'hikapi',
        component: () => import("@/components/configCenter/hikapi/index.vue")
      },
      {
        path: 'excel',
        name: 'excel',
        component: () => import("@/components/configCenter/excel/index.vue")
      }
    ]
    
  },
  {
    path: '/test',
    component: () => import('@/components/test/index.vue'),
    
  },

]

const router = createRouter({
  history: createWebHistory('/'),
  routes
})

export default router
