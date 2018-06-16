<template>
    <div id="form-logout">
        <div class="button-logout" v-on:click.stop.prevent="logout()">logout <span class="fa fa-sign-out"></span></div>
    </div>
</template>

<script>
import { mapState } from 'vuex' 

export default {
    name: 'Logout',
    data() {
        return {

        }
    },
    methods: {
        logout: function() {
            this.$store.dispatch('logout')
                .then(() => this.$router.replace({ name: "Login" }))
        }
    }
}
</script>

<style scoped>
.button-logout {
    border: solid 2px;
    border-color: white;
    padding-top: 8px;
    padding-bottom: 7px;
    padding-left: 13px;
    padding-right: 13px;
    color: white;
    font-family: "Century Gothic", CenturyGothic, AppleGothic, sans-serif;
    font-weight: bold;
}
</style>
