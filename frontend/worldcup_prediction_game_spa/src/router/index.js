import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Home from '@/components/Home'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'Login',
            component: Login,
            beforeEnter(to, from, next) {
                // FIXME: Why does line below not work (always return True after reload)?
                // if (!store.getters.isAuthenticated) {
                if (localStorage.getItem('jwt') == '') {
                    next()
                } else {
                    next('/Home')
                }
            }
        },
        {
            path: '/home',
            name: 'Home',
            component: Home,
            beforeEnter(to, from, next) {
                // FIXME: Why does line below not work (always return True after reload)?
                // if (!store.getters.isAuthenticated) {
                if (localStorage.getItem('jwt') == '') {
                    next('/')
                } else {
                    next()
                }
            }
        }
    ]
})
