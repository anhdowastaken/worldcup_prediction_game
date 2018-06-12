<template>
    <div id="app">
        <router-view @authenticated="setAuthenticated"/>
    </div>
</template>

<script>
export default {
    name: 'App',
    data() {
        return {
            authenticated: false,
        }
    },
    mounted() {
        if (!this.authenticated) {
            this.$router.replace({ name: "Login" });
        }
    },
    methods: {
        setAuthenticated(status) {
            this.authenticated = status;
        },
        logout() {
            this.authenticated = false;
        }
    }

}
</script>

<style>
</style>
