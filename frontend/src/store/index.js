import { createStore } from 'vuex'
import router from '../router'

export default createStore({
  state: {
        user: false,
        //mutitabs
        tabsPage: [],
        TabsValue: '',
        //控制是否支持多选项卡
        isMultiTabs:false
  },
  mutations: {
        // 登录
        login(state, user) {
            state.user = user;
            sessionStorage.setItem("userInfo", user);
        },
        // 退出
        logout(state, user) {
            state.user = "";
            sessionStorage.setItem("userInfo", "");
        },
        //mutitabs
        editableTabs: (state, obj) => {
          // 浅拷贝 state.tabsPage
          const arr = Array.from(state.tabsPage)
          // 判断数组内是否为空
          if (arr.length !== 0) {
            // 使用 Array.some 去判断是否存在对象信息
            var even = function (obj) {
              return arr.some(item => {
                return item.name === obj.attributes.url
              })
            }
            // even方法 如果对象存在返回true,不存在则返回flase
            // 加！触发 true 代码块
            if (!even(obj)/* 如果不存在将对象push进数组内bing */) {
              // 将tabs所需参数push进arr数组
              arr.push({ title: obj.text, name: obj.attributes.url })
              // 赋值给tabsPage参数
              state.tabsPage = arr
              // 存储sessionStorage -- 解决刷新消失
              window.sessionStorage.setItem('tabsPage', JSON.stringify(arr))
              window.sessionStorage.setItem('TabsValue', obj.attributes.url)
              // 赋值给TabsValue参数
              state.TabsValue = obj.attributes.url
              // 跳转
              router.push({ name: obj.attributes.url })
            } else { // 如果存在 只做跳转选中
              // 赋值给TabsValue参数
              state.TabsValue = obj.attributes.url
              window.sessionStorage.setItem('TabsValue', obj.attributes.url)
              // 跳转
              router.push({ name: obj.attributes.url })
            }
          } else { // 如果为0
            // 将tabs所需参数push进arr数组
            arr.push({
              title: obj.text, name: obj.attributes.url
            })
            // 赋值给tabsPage参数
            state.tabsPage = arr
            // 赋值给TabsValue参数
            state.TabsValue = obj.attributes.url
            // 跳转
            router.push({ name: obj.attributes.url })
          }
        }
  },
  actions: {
     // 注册方法
      editableTabs(context, obj) {
          context.commit('editableTabs', obj)
      }
  },
  modules: {
  }
})
