<template>
    <div id="form-login">
        <h1>Login</h1>
        <input type="text" name="username" v-model="input.username" placeholder="Username" />
        <input type="password" name="password" v-model="input.password" placeholder="Password" />
        <button type="button" v-on:click="login()">Login</button>
    </div>
</template>

<script>
import { submitLogin} from '@/api'

export default {
    name: 'Login',
    data() {
        return {
            input: {
                username: "",
                password: ""
            }
        }
    },
    methods: {
        login: function() {
            if (this.input.username != '' && this.input.password != '') {
                submitLogin(this.input.username, this.input.password).then((response) => {
                    this.$emit("authenticated", true);
                    this.$router.replace({ name: "Home" });
                })
            } else {
                console.log('Username or password is empty')
            }
        }
    }
}
</script>

<style scoped>
</style>
