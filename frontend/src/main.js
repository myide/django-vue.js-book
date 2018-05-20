import Vue from 'vue'
import iView from 'iview'
import { router } from './router/index'
import { appRouter } from './router/router'
import App from './app.vue'
import '@/locale'
import 'iview/dist/styles/iview.css'
import VueI18n from 'vue-i18n'
import util from './libs/util'
import backendsapi from './libs/backendsapi'
import axios from './http'
import store from './store'

Vue.use(VueI18n)
Vue.use(iView)

Vue.prototype.ajax = axios // 让它在每个组件都可用(重命名axios为ajax)
Vue.prototype.util = util
Vue.prototype.backendsapi = backendsapi

/* 
  为了全局可用：为何有的是Vue.use，有的是Vue.prototype，有的是new Vue注册
*/

new Vue({
    el: '#app',
    router: router,
    store: store,
    render: h => h(App),
    data: {
        currentPageName: ''
    },
    mounted() {
        this.currentPageName = this.$route.name
            // 显示打开的页面的列表
        this.$store.commit('setOpenedList')
        this.$store.commit('initCachepage')
            // 权限菜单过滤相关
        this.$store.commit('updateMenulist')
            // iview-admin检查更新
            // util.checkUpdate(this)
    },
    created() {
        let tagsList = []
        appRouter.map((item) => {
            if (item.children.length <= 1) {
                tagsList.push(item.children[0])
            } else {
                tagsList.push(...item.children)
            }
        })
        this.$store.commit('setTagsList', tagsList)
    }
})