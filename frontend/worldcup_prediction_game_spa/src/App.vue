<template>
    <div id="app">
        <notification></notification>
        <router-view/>
    </div>
</template>

<script>
import Notification from './components/Notification'

export default {
    name: 'App',
    components: {
        Notification
    },
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
@font-face {
    font-family: localCenturyGothic;
    src: url('./assets/fonts/centurygothic-webfont.woff') format('woff');
}

@font-face {
    font-family: localCenturyGothic;
    src: url('./assets/fonts/centurygothicbold-webfont.woff') format('woff');
    font-weight: bold;
}
</style>
