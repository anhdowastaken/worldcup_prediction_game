<template>
    <div class="container">
        <div class="header clearfix">
            <nav>
                <ul class="nav nav-pills pull-right">
                    <li role="presentation"><logout></logout></li>
                </ul>
            </nav>
            <div>
                <h3 class="text-muted">{{ this.userData['username'] }}</h3>
                <p>Last login: {{ this.userData['last_login_at'] }}</p>
            </div>
        </div>

        <form id="form-register" class="form-inline">
            <h3>Register</h3>
            <div class="form-group">
                <input type="text" class="form-control" name="username" v-model="username_to_register" placeholder="Username" />
                <button type="button" class="btn btn-default" v-on:click.stop.prevent="register()">Register</button>
            </div>
        </form>

        <form id="form-reset-password" class="form-inline">
            <h3>Reset password</h3>
            <div class="form-group">
                <input type="text" class="form-control" name="username" v-model="username_to_reset_password" placeholder="Username" />
                <button type="button" class="btn btn-default" v-on:click.stop.prevent="resetPassword()">Reset</button>
            </div>
        </form>
    </div>
</template>

<script>
import { mapState } from 'vuex' 
import { isEmpty } from '@/utils'
import { key_jwt, key_user_data } from '@/common'
import Logout from '@/components/Logout'

export default {
    name: 'Admin',
    components: {
        Logout
    },
    data() {
        return {
            username_to_register: "",
            username_to_reset_password: ""
        }
    },
    computed: mapState({
        userData: function(state) {
            if (!isEmpty(state.userData)) {
                return state.userData
            } else {
                return JSON.parse(sessionStorage.getItem(key_user_data))
            }
        },
        jwt: function(state) {
            if (state.jwt) {
                return state.jwt 
            } else {
                return sessionStorage.getItem(key_jwt)
            }
        }
    }),
    methods: {
        register: function() {
            this.$store.dispatch('register', { jwt: this.jwt, username: this.username_to_register })
            this.username_to_register = ""
        },
        resetPassword: function() {
            this.$store.dispatch('resetPassword', { jwt: this.jwt, username: this.username_to_reset_password})
            this.username_to_reset_password = ""
        }
    }
}
</script>

<style scoped>
.header-background {
    background: linear-gradient(to right,
                              rgba(0, 78, 161, 1),
                              rgba(134, 60, 186, 1),
                              rgba(185, 35, 163, 1));
    /* background: linear-gradient(to right,
                              rgba(0, 78, 161, 1),
                              rgba(134, 60, 186, 1),
                              rgba(185, 35, 163, 1)),
                url('../assets/header_background_image.png'); */
    /* background-image: url('../assets/header_background_image.png'); */
    /* background-size: contain; */
    height: 350px;
    min-height: 350px;
    position: absolute;
    z-index: -99;
    width: 100%;
}

.header-background-under {
    z-index: -100;
    opacity: 0.5;
    background: black;
    top: 0;
    height: 350px;
    min-height: 350px;
    position: absolute;
    width: 100%;
}

.header, .matches {
    padding-right: 5px;
    padding-left: 5px;
}

/* Custom page header */
.header {
    position: relative;
    padding-top: 10px;
    padding-bottom: 10px;
    height: 350px;
    min-height: 350px;
}

/* Customize container */
@media (min-width: 768px) {
    .container {
        max-width: 730px;
        margin-top: 20px;
    }
}

/* Supporting matches content */
.matches {
    margin: 10px 0;
}

/* Responsive: Portrait tablets and up */
@media screen and (min-width: 768px) {
    /* Remove the padding we set earlier */
    .header,
    .matches {
        padding-right: 0;
        padding-left: 0;
    }
    /* Space out the masthead */
    .header {
        margin-bottom: 10px;
    }
}
</style>
