import { createRouter, createWebHistory ,createWebHashHistory } from 'vue-router'
// 进度条
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
// 简单配置
NProgress.inc(0.4)
NProgress.configure({ easing: 'ease', speed: 500, showSpinner: true })

const routes = [
  {
    path: '/',
    name: '',
    component: () => import('../views/login.vue'),
    hidden: true,
    meta: {
      requireAuth: false,
      index: '/',
    }
  },
    {
    path: '/login',
    name: '登录',
    component: () => import('../views/login.vue'),
    hidden: true,
    meta: {
      requireAuth: false,
      index: '/login',
    }
  }, {
    path: '/index',
    name: '首页',
    component: () => import('../views/index.vue'),
    iconCls: 'el-icon-tickets',
    meta: {
      requireAuth: false,
      index: '/index',
    },
    children: [
      // 超管
      {
        path: '/adminManage',
        name: 'adminManage',
        component: () => import('../views/adminManage/adminManage.vue'),
        meta: {
          requireAuth: true,
          index: '/adminManage',
        }
      },
      {
        path: '/userManage',
        name: 'userManage',
        component: () => import('../views/userManage/userManage.vue'),
        meta: {
          requireAuth: true,
          index: '/userManage',
        }
      },
        {
            path: '/carouselSettingsimg',
            name: 'carouselSettingsimg',
            component: () => import('../views/platformSettings/carouselSettingsimg.vue'),
            meta: {
                requireAuth: true,
                index: '/carouselSettingsimg',
            }
        },
        {
            path: '/platformSettingsother',
            name: 'platformSettingsother',
            component: () => import('../views/platformSettings/platformSettingsother.vue'),
            meta: {
                requireAuth: true,
                index: '/platformSettingsother',
            }
        },

      {
        path: '/userFeekback',
        name: 'userFeekback',
        component: () => import('../views/userFeekback/userFeekback.vue'),
        meta: {
          requireAuth: true,
          index: '/userFeekback',
        }
      },

      // 系统管理
      {
        path: '/departmentManage',
        name: 'departmentManage',
        component: () => import('../views/systemManage/departmentManage/departmentManage.vue'),
        meta: {
          requireAuth: true,
          index: '/departmentManage',
        }
      },
      {
        path: '/menuManage',
        name: 'menuManage',
        component: () => import('../views/systemManage/menuManage/menuManage.vue'),
        meta: {
          requireAuth: true,
          index: '/menuManage',
        }
      },

      {
        path: '/roleManage',
        name: 'roleManage',
        component: () => import('../views/systemManage/roleManage/roleManage.vue'),
        meta: {
          requireAuth: true,
          index: '/roleManage',
        }
      },


      {
        path: '/authorityManage',
        name: 'authorityManage',
        component: () => import('../views/systemManage/authorityManage/authorityManage.vue'),
        meta: {
          requireAuth: true,
          index: '/authorityManage',
        }
      },
      {
        path: 'buttonConfig/:id/:name',
        name: 'buttonConfig',
        component: () => import('../views/systemManage/buttonConfig/buttonConfig.vue'),
        meta: {
          requireAuth: true,
          index: '/buttonConfig',
        }
      },
        {
        path: '/buttonManage',
        name: 'buttonManage',
        component: () => import('../views/systemManage/button/buttonManage.vue'),
        meta: {
          requireAuth: true,
          index: '/buttonManage',
        }
      },
      {
        path: '/messagTemplate',
        name: 'messagTemplate',
        component: () => import('../views/messageCenter/messagTemplate.vue'),
        meta: {
          requireAuth: true,
          index: '/messagTemplate',
        }
      },
      {
        path: '/messagNotice',
        name: 'messagNotice',
        component: () => import('../views/messageCenter/messagNotice.vue'),
        meta: {
          requireAuth: true,
          index: '/messagNotice',
        }
      },
      {
        path: '/personalCenter',
        name: 'personalCenter',
        component: () => import('../views/personalCenter/personalCenter.vue'),
        meta: {
          requireAuth: true,
          index: '/personalCenter',
        }
      },
      {
        path: '/journalManage',
        name: 'journalManage',
        component: () => import('../views/journalManage/journalManage.vue'),
        meta: {
          requireAuth: true,
          index: '/journalManage',
        }
      },

    ]
  }
]

const router = createRouter({
  //history模式
  // history: createWebHistory(process.env.BASE_URL),
  //hash模式
  history: createWebHashHistory(),
  routes
})

/**
 * 路由拦截
 * 权限验证
 */
let to={},from={}
router.beforeEach((to, from, next) => {
  // 进度条
  NProgress.start()
  let userId = sessionStorage.getItem('userId') ? sessionStorage.getItem('userId') : false
  if (to.meta.requireAuth) { // 判断该路由是否需要登录权限
    if (userId) { // 通过vuex state获取当前的token是否存在
      let menuList = JSON.parse(sessionStorage.getItem('menuList'))
      if(menuList.filter(item=>item.url == to.name).length > 0 || (to.name =='buttonConfig' &&  menuList.filter(item=>item.url=='menuManage').length >0) || (to.name =='buttonManage' &&  menuList.filter(item=>item.url=='menuManage').length >0)) {
        next()
      } else {
        next({
          path: '/login'
        })
      }
    } else {
      // console.info("进入登陆")
        next({
          path: '/login'
        })
    }
  } else {
    if(to.path=="/login" ||to.path=="/"){
      if(userId){
        next({
          path: '/adminManage'
        })
      }else{
        next()
      }
    }else{
      next()
    }
  }
})
//在路由跳转后用NProgress.done()标记下结束
router.afterEach(() => {
  NProgress.done()
})
export default router
