import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Home from '@/components/Home'
import store from '@/store'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'Login',
            component: Login
        },
        {
            path: '/home',
            name: 'Home',
            component: Home,
            beforeEnter(to, from, next) {
                if (!store.getters.isAuthenticated) {
                    next('/')
                } else {
                    next()
                }
            }
        }
    ]
})
