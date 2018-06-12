<template>
    <div id="form-logout">
        <button type="button" v-on:click="logout()">Logout</button>
    </div>
</template>

<script>
import { submitLogout } from '@/api'

export default {
    name: 'Logout',
    data() {
        return {

        }
    },
    methods: {
        logout: function() {
            submitLogout().then((response) => {
                this.$emit("authenticated", false);
                this.$router.replace({ name: "Login" });
            })
        }
    }
}
</script>

<style scoped>
</style>
