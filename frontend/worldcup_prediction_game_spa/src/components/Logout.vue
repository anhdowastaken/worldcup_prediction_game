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
    font-family: localCenturyGothic, "Century Gothic", CenturyGothic, "Apple Gothic", AppleGothic, "URW Gothic L", "Avant Garde", Futura, sans-serif;
    font-weight: bold;
}
</style>
