/*
 * @文件介绍: 菜单获取
 */
import { uniqueId } from 'lodash'
import { request } from '@/api/service'
import XEUtils from 'xe-utils'
import { frameInRoutes } from '@/router/routes'
const _import = require('@/libs/util.import.' + process.env.NODE_ENV)
/**
 * @description 给菜单数据补充上 path 字段
 * @description https://github.com/d2-projects/d2-admin/issues/209
 * @param {Array} menu 原始的菜单数据
 */
function supplementPath (menu) {
  return menu.map(e => ({
    ...e,
    path: e.path || uniqueId('ly-menu-empty-'),
    ...e.children ? {
      children: supplementPath(e.children)
    } : {}
  }))
}

export const menuHeader = supplementPath([])

// export const menuHeader = supplementPath([
//     { path: '/index', title: '首页', icon: 'home' },
//     {
//         title: '页面',
//         icon: 'folder-o',
//         children: [
//             { path: '/page1', title: '页面 1' },
//             { path: '/page2', title: '页面 2' },
//             { path: '/page3', title: '页面 3' }
//         ]
//     }
// ])

export const menuAside = supplementPath([])
// export const menuAside = supplementPath([
//     { path: '/index', title: '首页', icon: 'home' },
//     {
//         title: '系统管理',
//         icon: 'folder-o',
//         children: [
//             // { path: '/page1', title: '页面 1' },
//             // { path: '/page2', title: '页面 2' },
//             // { path: '/page3', title: '页面 3' },
//             { path: '/menu', title: '菜单' },
//             { path: '/user', title: '用户' },
//             { path: '/button', title: '按钮' },
//             { path: '/role', title: '角色' },
//             { path: '/dept', title: '部门' },
//             { path: '/rolePermission', title: '角色权限' },
//             {
//                 title: '日志管理', children: [
//                     { path: '/operationLog', title: '操作日志' },
//                 ]
//             },
//         ]
//     }
// ])

// 请求菜单数据,用于解析路由和侧边栏菜单
export const getMenu = function (self) {
  return request({
    url: '/api/system/web_router/',
    method: 'get',
    params: {}
  }).then((res) => {
    // 设置动态路由
    const menuData = res.data.data
    localStorage.setItem('menuData', JSON.stringify(menuData))
    return menuData
  })
}

/**
 * 将获取到的后端菜单数据,解析为前端路由
 */
export const handleRouter = function (menuData) {
  const result = []
  for (const item of menuData) {
    if (item.path !== '' && item.parent !== null && item.component) {
      const obj = {
        path: item.path,
        name: item.component_name,
        component: _import(item.component),
        meta: {
          title: item.name,
          auth: true,
          cache: item.cache === 1
        }
      }
      result.push(obj)
    } else {
      delete item.path
    }
  }
  frameInRoutes[0].children = [...result]
  return frameInRoutes
}

/**
 * 将前端的侧边菜单进行处理
 */
export const handleAsideMenu = function (menuData) {
  // 将列表数据转换为树形数据
  const data = XEUtils.toArrayTree(menuData, {
    parentKey: 'parent',
    strict: true
  })
  const menu = [
    { path: '/index', title: '首页', icon: 'home' },
    ...data
  ]
  return supplementPath(menu)
}