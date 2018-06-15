import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Home from '@/components/Home'
import Admin from '@/components/Admin'

Vue.use(Router)

const router = new Router({
    routes: [
        {
            path: '/',
            name: 'Login',
            component: Login,
            beforeEnter(to, from, next) {
                // FIXME: Why does line below not work (always return True after reload)?
                // if (!store.getters.isAuthenticated) {
                if (sessionStorage.getItem('jwt') == '') {
                    next()
                } else if (sessionStorage.getItem('user_data') &&
                           JSON.parse(sessionStorage.getItem('user_data'))['role'] &&
                           JSON.parse(sessionStorage.getItem('user_data'))['role'] == 'admin') {
                    next('/admin')
                } else {
                    next('/home')
                }
            }
        },
        {
            path: '/home',
            name: 'Home',
            component: Home,
            beforeEnter(to, from, next) {
                if (sessionStorage.getItem('jwt') == '') {
                    next('/')
                } else if (sessionStorage.getItem('user_data') &&
                           JSON.parse(sessionStorage.getItem('user_data'))['role'] &&
                           JSON.parse(sessionStorage.getItem('user_data'))['role'] == 'admin') {
                    next('/admin')
                } else {
                    next()
                }
            }
        },
        {
            path: '/admin',
            name: 'Admin',
            component: Admin,
            beforeEnter(to, from, next) {
                if (sessionStorage.getItem('jwt') == '') {
                    next('/')
                } else if (sessionStorage.getItem('user_data') &&
                           JSON.parse(sessionStorage.getItem('user_data'))['role'] &&
                           JSON.parse(sessionStorage.getItem('user_data'))['role'] == 'admin') {
                    next()
                } else {
                    next('/home')
                }
            }
        }
    ]
})

export default router
