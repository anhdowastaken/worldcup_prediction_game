<template>
    <div id="app">
        <router-view/>
    </div>
</template>

<script>
export default {
    name: 'App',
    data() {
        return {

        }
    },
    computed: {
        isAuthenticated () {
            return this.$store.getters.isAuthenticated
        }
    },
    mounted() {
        if (!this.isAuthenticated) {
            this.$router.replace({ name: "Login" });
        } else {
            this.$router.replace({ name: "Home" });
        }
    }
}
</script>

<style>
</style>
