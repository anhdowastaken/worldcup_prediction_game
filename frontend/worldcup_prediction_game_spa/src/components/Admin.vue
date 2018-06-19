<template>
    <div>
        <div class="header-background">
            <div class="header-background-under"></div>
        </div>

        <div class="container">
            <div class="header">
                <nav>
                    <ul class="nav nav-pills pull-left">
                        <li><span class="fa fa-user"
                                  style="font-size: 24px;
                                         color: white;
                                         margin-top: 5px;
                                         padding-right: 10px;
                                         padding-top: 2px;
                                         padding-bottom: 2px;
                                         cursor: pointer;"
                                  v-on:click.stop.prevent="goToUserCP()"></span></li>
                    </ul>

                    <ul class="nav nav-pills pull-right">
                        <li><logout></logout></li>
                    </ul>
                </nav>
                <account-info></account-info>
            </div>

            <form class="form-register">
                <h2 class="form-register-heading">Register New User</h2>
                <label for="inputUsernameToRegister" class="sr-only">Username</label>
                <input type="text" id="inputUsernameToRegister" class="form-control" placeholder="username" required v-model="username_to_register">
                <button class="btn btn-lg btn-primary btn-block"
                        v-on:submit.stop.prevent="doNothing()"
                        v-on:click.stop.prevent="register()">Register</button>
            </form>

            <form class="form-reset-password">
                <h2 class="form-reset-password-heading">Reset Password</h2>
                <label for="inputUsernameToResetPassword" class="sr-only">Username</label>
                <input type="text" id="inputUsernameToResetPassword" class="form-control" placeholder="username" required v-model="username_to_reset_password">
                <button class="btn btn-lg btn-primary btn-block"
                        v-on:submit.stop.prevent="doNothing()"
                        v-on:click.stop.prevent="resetPassword()">Reset</button>
            </form>

            <form class="form-delete-user">
                <h2 class="form-delete-user-heading">Delete Existing User</h2>
                <label for="inputUsernameToDelete" class="sr-only">Username</label>
                <input type="text" id="inputUsernameToDelete" class="form-control" placeholder="username" required v-model="username_to_delete">
                <button class="btn btn-lg btn-primary btn-block"
                        v-on:submit.stop.prevent="doNothing()"
                        v-on:click.stop.prevent="deleteUser()">Delete</button>
            </form>
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex' 
import { mapMutations } from 'vuex'
import { isEmpty } from '@/utils'
import { key_jwt, key_user_data } from '@/common'
import AccountInfo from '@/components/AccountInfo'
import Logout from '@/components/Logout'
import { submitRegister } from '@/api'
import { submitResetPassword } from '@/api'
import { submitDeleteUser} from '@/api'

export default {
    name: 'Admin',
    components: {
        AccountInfo,
        Logout
    },
    data() {
        return {
            username_to_register: "",
            username_to_reset_password: "",
            username_to_delete: ""
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
        ...mapMutations([
            'setNotificationContent',
            'showNotification'
        ]),
        register: function() {
            if (this.username_to_register == "") {
                this.setNotificationContent({ header: 'Error',
                                              body: 'Empty username isn\'t allowed' })
                this.showNotification()
            } else {
                submitRegister(this.jwt, this.username_to_register)
                    .then(response => {
                        if (response.status === 201) {
                            this.setNotificationContent({ header: 'Notification',
                                                          body: response.data['message'] + '\nPassword: ' + response.data['user_data']['password'] })
                            this.showNotification()
                            this.username_to_register = ""
                        }
                    })
                    .catch(error => {
                        if (error.response.data['message']) {
                            // There is problem with authentication
                            // Back to login
                            if (error.response.status == 401) {
                                alert(error.response.data['message'])
                                this.$store.dispatch('logout')
                            } else {
                                this.setNotificationContent({ header: 'Error',
                                                              body: error.response.data['message'] })
                                this.showNotification()
                            }
                        } else if (error) {
                            this.setNotificationContent({ header: 'Error',
                                                          body: error })
                            this.showNotification()
                        } else {
                            this.setNotificationContent({ header: 'Error',
                                                          body: 'Error' })
                            this.showNotification()
                        }
                    })
            }
        },
        resetPassword: function() {
            if (this.username_to_reset_password == "") {
                this.setNotificationContent({ header: 'Error',
                                              body: 'Empty username isn\'t allowed' })
                this.showNotification()
            } else {
                if (confirm('Are you sure?')) {
                    submitResetPassword(this.jwt, this.username_to_reset_password)
                        .then(response => {
                            if (response.status === 201) {
                                this.setNotificationContent({ header: 'Notification',
                                                              body: response.data['message'] + '\nPassword: ' + response.data['user_data']['password'] })
                                this.showNotification()
                                this.username_to_reset_password = ""
                            }
                        })
                        .catch(error => {
                            if (error.response.data['message']) {
                                // There is problem with authentication
                                // Back to login
                                if (error.response.status == 401) {
                                    alert(error.response.data['message'])
                                    this.$store.dispatch('logout')
                                } else {
                                    this.setNotificationContent({ header: 'Error',
                                                                  body: error.response.data['message'] })
                                    this.showNotification()
                                }
                            } else if (error) {
                                this.setNotificationContent({ header: 'Error',
                                                              body: error })
                                this.showNotification()
                            } else {
                                this.setNotificationContent({ header: 'Error',
                                                              body: 'Error' })
                                this.showNotification()
                            }
                        })
                }
            }
        },
        deleteUser: function() {
            if (this.username_to_delete == "") {
                this.setNotificationContent({ header: 'Error',
                                              body: 'Empty username isn\'t allowed' })
                this.showNotification()
            } else {
                if (confirm('Are you sure?')) {
                    submitDeleteUser(this.jwt, this.username_to_delete)
                        .then(response => {
                            if (response.status === 201) {
                                this.setNotificationContent({ header: 'Notification',
                                                              body: response.data['message'] })
                                this.showNotification()
                                this.username_to_delete = ""
                            }
                        })
                        .catch(error => {
                            if (error.response.data['message']) {
                                // There is problem with authentication
                                // Back to login
                                if (error.response.status == 401) {
                                    alert(error.response.data['message'])
                                    this.$store.dispatch('logout')
                                } else {
                                    this.setNotificationContent({ header: 'Error',
                                                                  body: error.response.data['message'] })
                                    this.showNotification()
                                }
                            } else if (error) {
                                this.setNotificationContent({ header: 'Error',
                                                              body: error })
                                this.showNotification()
                            } else {
                                this.setNotificationContent({ header: 'Error',
                                                              body: 'Error' })
                                this.showNotification()
                            }
                        })
                }
            }
        },
        goToUserCP: function() {
            this.$router.push({ name: 'UserCP' })
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

.form-register,
.form-reset-password,
.form-delete-user {
    max-width: 330px;
    padding: 15px;
    margin: 0 auto;
    font-family: localCenturyGothic, "Century Gothic", CenturyGothic, "Apple Gothic", AppleGothic, "URW Gothic L", "Avant Garde", Futura, sans-serif;
}
.form-register .form-register-heading,
.form-reset-password .form-reset-password-heading,
.form-delete-user .form-delete-user-heading {
    margin-bottom: 10px;
}
.form-register .form-control,
.form-reset-password .form-control,
.form-delete-user .form-control {
    position: relative;
    height: auto;
    -webkit-box-sizing: border-box;
       -moz-box-sizing: border-box;
            box-sizing: border-box;
    padding: 10px;
    font-size: 16px;
}
.form-register .form-control:focus,
.form-reset-password .form-control:focus,
.form-delete-user .form-control:focus {
    z-index: 2;
}
.form-register input,
.form-reset-password input,
.form-delete-user input {
    margin-bottom: 10px;
}
.form-register button,
.form-reset-password button,
.form-delete-user button {
    background: linear-gradient(to right,
                              rgba(0, 78, 161, 1),
                              rgba(134, 60, 186, 1),
                              rgba(185, 35, 163, 1));
    text-transform: lowercase;
}
</style>
