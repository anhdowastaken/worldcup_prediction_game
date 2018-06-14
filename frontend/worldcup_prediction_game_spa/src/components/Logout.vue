<template>
    <div id="form-logout">
        <button type="button" class="btn btn-default btn-block" v-on:click="logout()">Logout</button>
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
</style>
