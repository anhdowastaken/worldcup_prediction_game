<template>
    <div class="container">
      <transition name="modal">
            <div class="modal fade" role="dialog"
                 v-bind:style="{ display: modalDisplayStyle }"
                 v-bind:class="{ in: showModal }">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" class="close" v-on:click="hideModal">&times;</button>
                            <h4 class="modal-title">{{ this.modalHeader}} </h4>
                        </div>
                        <div class="modal-body">
                            <p>{{ this.modalBody }}</p>
                        </div>
                        <!-- <div class="modal-footer"></div> -->
                    </div>
                </div>
            </div>
      </transition>

        <form class="form-signin">
            <h2 class="form-signin-heading"></h2>
            <label for="inputUsername" class="sr-only">Username</label>
            <input type="username" id="inputUsername" class="form-control" placeholder="username" required autofocus v-model="username">
            <label for="inputPassword" class="sr-only">Password</label>
            <input type="password" id="inputPassword" class="form-control" placeholder="password" required v-model="password">
            <button class="btn btn-lg btn-primary btn-block" v-on:click.stop.prevent="login()" v-on:submit.stop.prevent="login()">Login</button>
        </form>

    </div>
</template>

<script>
import { mapMutations } from 'vuex'
import { submitLogin } from '@/api'

export default {
    name: 'Login',
    data() {
        return {
            showModal: false,
            modalDisplayStyle: 'none',
            modalHeader: "",
            modalBody: "",
            username: "",
            password: ""
        }
    },
    methods: {
        ...mapMutations([
            'setJwtToken',
            'setUserData'
        ]),
        login: function() {
            if (this.username == '' || this.password == '') {
                this.modalHeader = ('Error')
                this.modalBody = ('Username and password can\'t be empty')
                this.modalDisplayStyle = 'block'
                this.showModal = true
            } else {
                submitLogin(this.username, this.password)
                    .then(response => {
                        console.log(response)
                        if (response.status === 200) {
                            this.setJwtToken({ jwt: response.data['token'] })
                            this.setUserData({ userData: response.data['user_data'] })
                            this.$router.push({ name: "Home" })
                        }
                    })
                    .catch(error => {
                        this.modalHeader = ('Error')
                        if (error.response.data['message']) {
                            this.modalBody = error.response.data['message']
                        } else if (error) {
                            this.modalBody = ('Error Authenticating: ' + error)
                        } else {
                            this.modalBody = ('Error')
                        }
                        this.modalDisplayStyle = 'block'
                        this.showModal = true
                    })
            }
        },
        hideModal: function() {
            this.modalDisplayStyle = 'none'
            this.showModal = false
        }
    }
}
</script>

<style scoped>
.form-signin {
  max-width: 330px;
  padding: 15px;
  margin: 0 auto;
  font-family: localCenturyGothic, "Century Gothic", CenturyGothic, "Apple Gothic", AppleGothic, "URW Gothic L", "Avant Garde", Futura, sans-serif;
}
.form-signin .form-signin-heading,
.form-signin .checkbox {
  margin-bottom: 10px;
}
.form-signin .checkbox {
  font-weight: normal;
}
.form-signin .form-control {
  position: relative;
  height: auto;
  -webkit-box-sizing: border-box;
     -moz-box-sizing: border-box;
          box-sizing: border-box;
  padding: 10px;
  font-size: 16px;
}
.form-signin .form-control:focus {
  z-index: 2;
}
.form-signin input[type="username"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}
.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
.form-signin button {
  background: linear-gradient(to right,
                            rgba(0, 78, 161, 1),
                            rgba(134, 60, 186, 1),
                            rgba(185, 35, 163, 1));
  text-transform: lowercase;
}
</style>
