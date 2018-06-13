<template>
    <div id="form-logout">
        <button type="button" v-on:click="logout()">Logout</button>
    </div>
</template>

<script>
import { mapState } from 'vuex' 
import { submitLogout } from '@/api'

export default {
    name: 'Logout',
    data() {
        return {

        }
    },
    computed: mapState({
        jwt: state => state.jwt
    }),
    methods: {
        logout: function() {
            submitLogout(this.jwt).then((response) => {
                this.$router.replace({ name: "Login" });
            })
        }
    }
}
</script>

<style scoped>
</style>
