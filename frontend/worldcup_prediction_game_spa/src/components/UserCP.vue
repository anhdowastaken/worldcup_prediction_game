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

        <form id="form-change-password" class="form-inline">
            <h3>Change password</h3>
            <div class="form-group">
                <input type="password" class="form-control" name="old_password" v-model="old_password" placeholder="old password" />
                <input type="password" class="form-control" name="new_password" v-model="new_password" placeholder="new password" />
                <button type="button" class="btn btn-default" v-on:click.stop.prevent="changePassword()">change</button>
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
    name: 'UserCP',
    components: {
        Logout
    },
    data() {
        return {
            old_password: "",
            new_password: ""
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
        changePassword: function() {
            this.$store.dispatch('changePassword', { jwt: this.jwt,
                                                     old_password: this.old_password,
                                                     new_password: this.new_password })
            this.old_password = ""
            this.new_password = ""
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
