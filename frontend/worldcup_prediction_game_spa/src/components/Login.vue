<template>
    <div id="form-login">
        <h1>Login</h1>
        <input type="text" name="username" v-model="username" placeholder="Username" />
        <input type="password" name="password" v-model="password" placeholder="Password" />
        <button type="button" v-on:click="login()">Login</button>
    </div>
</template>

<script>
import { submitLogin} from '@/api'

export default {
    name: 'Login',
    data() {
        return {
            username: "",
            password: ""
        }
    },
    methods: {
        login: function() {
            this.$store.dispatch('login', { username: this.username, password: this.password })
                .then(() => this.$router.replace({ name: "Home" }))
        }
    }
}
</script>

<style scoped>
</style>
