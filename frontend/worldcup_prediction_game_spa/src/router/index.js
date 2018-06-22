import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Home from '@/components/Home'
import Admin from '@/components/Admin'
import UserCP from '@/components/UserCP'
import Ranking from '@/components/Ranking'
import { key_jwt, key_user_data } from '@/common'

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
                console.log(localStorage.getItem(key_jwt))
                if (localStorage.getItem(key_jwt) == null ||
                    localStorage.getItem(key_jwt) == undefined ||
                    localStorage.getItem(key_jwt) == '') {
                    next()
                } else if (localStorage.getItem(key_user_data) &&
                           JSON.parse(localStorage.getItem(key_user_data))['role'] &&
                           JSON.parse(localStorage.getItem(key_user_data))['role'] == 'admin') {
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
                if (localStorage.getItem(key_jwt) == null ||
                    localStorage.getItem(key_jwt) == undefined ||
                    localStorage.getItem(key_jwt) == '') {
                    next('/')
                } else if (localStorage.getItem(key_user_data) &&
                           JSON.parse(localStorage.getItem(key_user_data))['role'] &&
                           JSON.parse(localStorage.getItem(key_user_data))['role'] == 'admin') {
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
                if (localStorage.getItem(key_jwt) == null ||
                    localStorage.getItem(key_jwt) == undefined ||
                    localStorage.getItem(key_jwt) == '') {
                    next('/')
                } else if (localStorage.getItem(key_user_data) &&
                           JSON.parse(localStorage.getItem(key_user_data))['role'] &&
                           JSON.parse(localStorage.getItem(key_user_data))['role'] == 'admin') {
                    next()
                } else {
                    next('/home')
                }
            }
        },
        {
            path: '/usercp',
            name: 'UserCP',
            component: UserCP,
            beforeEnter(to, from, next) {
                if (localStorage.getItem(key_jwt) == null ||
                    localStorage.getItem(key_jwt) == undefined ||
                    localStorage.getItem(key_jwt) == '') {
                    next('/')
                } else if (localStorage.getItem(key_user_data)) {
                    next()
                } else {
                    next('/home')
                }
            }
        },
        {
            path: '/ranking',
            name: 'Ranking',
            component: Ranking,
            beforeEnter(to, from, next) {
                if (localStorage.getItem(key_jwt) == null ||
                    localStorage.getItem(key_jwt) == undefined ||
                    localStorage.getItem(key_jwt) == '') {
                    next('/')
                } else if (localStorage.getItem(key_user_data)) {
                    next()
                } else {
                    next('/home')
                }
            }
        }
    ]
})

export default router
