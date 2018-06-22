<template>
    <div>
        <div class="header-background">
            <div class="header-background-under"></div>
        </div>

        <div class="container">
            <div class="header">
                <nav>
                    <ul class="nav nav-pills pull-left">
                        <li><span class="fa fa-chevron-left"
                                  style="font-size:24px;
                                         color:white;
                                         padding-top:2px;
                                         margin-top:2px;
                                         cursor: pointer;"
                                  v-on:click.stop.prevent="goBack"></span></li>
                    </ul>
 
                    <ul class="nav nav-pills pull-right">
                        <li><logout></logout></li>
                    </ul>
                </nav>
                <account-info></account-info>
            </div>

            <form class="form-change-password">
                <h2 class="form-change-password-heading"></h2>
                <label for="inputOldPassword" class="sr-only">Old Password</label>
                <input type="password" id="inputOldPassword" class="form-control" placeholder="old password" required autofocus v-model="old_password">
                <label for="inputNewPassword" class="sr-only">New Password</label>
                <input type="password" id="inputNewPassword" class="form-control" placeholder="new password" required v-model="new_password">
                <button class="btn btn-lg btn-primary btn-block"
                        v-on:submit.stop.prevent="doNothing()"
                        v-on:click.stop.prevent="changePassword()"
                        v-bind:disabled="!isHttpRequestCompleted">Change</button>
            </form>
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex' 
import { mapMutations } from 'vuex'
import { isEmpty } from '@/utils'
import { submitChangePassword } from '@/api'
import { key_jwt, key_user_data } from '@/common'
import AccountInfo from '@/components/AccountInfo'
import Logout from '@/components/Logout'

export default {
    name: 'UserCP',
    components: {
        AccountInfo,
        Logout
    },
    data() {
        return {
            old_password: "",
            new_password: "",
            isHttpRequestCompleted: true
        }
    },
    computed: mapState({
        userData: function(state) {
            if (!isEmpty(state.userData)) {
                return state.userData
            } else {
                return JSON.parse(localStorage.getItem(key_user_data))
            }
        },
        jwt: function(state) {
            if (state.jwt) {
                return state.jwt 
            } else {
                return localStorage.getItem(key_jwt)
            }
        }
    }),
    methods: {
        ...mapMutations([
            'setNotificationContent',
            'showNotification',
            'setNotificationRedirectAfterClose'
        ]),
        changePassword: function() {
            if (this.old_password == '' || this.new_password == '') {
                this.setNotificationContent({ header: 'Error',
                                              body: 'Password can\'t be empty' })
                this.showNotification()
            } else {
                this.isHttpRequestCompleted = false
                submitChangePassword(this.jwt, this.old_password, this.new_password )
                    .then(response => {
                        this.isHttpRequestCompleted = true
                        if (response.status === 201) {
                            this.setNotificationContent({ header: 'Notification',
                                                          body: response.data['message'] })
                            this.showNotification()
                            this.old_password = ""
                            this.new_password = ""
                        }
                    })
                    .catch(error => {
                        this.isHttpRequestCompleted = true
                        if (error.response.data['message']) {
                            this.setNotificationContent({ header: 'Error',
                                                          body: error.response.data['message'] })
                            this.showNotification()
                            // There is problem with authentication
                            // Back to login
                            if (error.response.status == 401) {
                                this.setNotificationRedirectAfterClose({ redirect: true,
                                                                         component_name: 'Login' })
                                this.$store.dispatch('logout')
                            }
                        } else if (error) {
                            context.commit('setNotificationContent', { header: 'Error',
                                                                       body: error })
                            context.commit('showNotification')
                        } else {
                            context.commit('setNotificationContent', { header: 'Error',
                                                                       body: 'Error' })
                            context.commit('showNotification')
                        }
                    })
            }
        },
        doNothing: function() {

        },
        goBack: function() {
            if (window.history.length > 1) {
                this.$router.go(-1)
            } else {
                this.$router.push('/')
            }
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

.form-change-password {
    max-width: 330px;
    padding: 15px;
    margin: 0 auto;
    font-family: localCenturyGothic, "Century Gothic", CenturyGothic, "Apple Gothic", AppleGothic, "URW Gothic L", "Avant Garde", Futura, sans-serif;
}
.form-change-password .form-change-password-heading {
    margin-bottom: 10px;
}
.form-change-password .form-control {
    position: relative;
    height: auto;
    -webkit-box-sizing: border-box;
       -moz-box-sizing: border-box;
            box-sizing: border-box;
    padding: 10px;
    font-size: 16px;
}
.form-change-password .form-control:focus {
    z-index: 2;
}
.form-change-password input[id="inputOldPassword"] {
    margin-bottom: -1px;
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
}
.form-change-password input[id="inputNewPassword"] {
    margin-bottom: 10px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
}
.form-change-password button {
    background: linear-gradient(to right,
                              rgba(0, 78, 161, 1),
                              rgba(134, 60, 186, 1),
                              rgba(185, 35, 163, 1));
    text-transform: lowercase;
}
</style>
