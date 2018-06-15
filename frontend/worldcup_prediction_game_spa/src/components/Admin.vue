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
                return JSON.parse(sessionStorage.getItem('user_data'))
            }
        },
        jwt: function(state) {
            if (state.jwt) {
                return state.jwt 
            } else {
                return sessionStorage.getItem('jwt')
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
.header,
.matches {
  padding-right: 15px;
  padding-left: 15px;
}

/* Custom page header */
.header {
  padding-bottom: 10px;
  border-bottom: 1px solid #e5e5e5;
}
/* Make the masthead heading the same height as the navigation */
.header h3 {
  margin-top: 0;
  margin-bottom: 0;
  line-height: 40px;
}

/* Customize container */
@media (min-width: 768px) {
  .container {
    max-width: 730px;
    margin-top: 20px;
  }
}
.container-narrow > hr {
  margin: 20px 0;
}

/* Supporting matches content */
.matches {
  margin: 20px 0;
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
