<template>
    <div id="form-register">
        <h1>Register</h1>
        <input type="text" name="username" v-model="username" placeholder="Username" />
        <button type="button" v-on:click="register()">Register</button>
    </div>
</template>

<script>
import { mapState } from 'vuex' 

export default {
    name: 'Register',
    data() {
        return {
            username: "",
        }
    },
    computed: mapState({
        jwt: function(state) {
            if (state.jwt) {
                return state.jwt 
            } else {
                return localStorage.jwt
            }
        }
    }),
    methods: {
        register: function() {
            this.$store.dispatch('register', { jwt: this.jwt, username: this.username })
        }
    }
}
</script>

<style scoped>
</style>
