<template>
    <div class="home">
        <logout></logout>
        <match v-for="match in matches" v-bind:match="match" :key="match.num"></match>
    </div>
</template>

<script>
import { mapState } from 'vuex' 
import Logout from '@/components/Logout'
import Match from '@/components/Match'

export default {
    name: 'Home',
    components: {
        Logout,
        Match
    },
    data () {
        return {

        }
    },
    computed: mapState({
        matches: state => state.matches,
        jwt: state => state.jwt
    }),
    beforeMount() {
        this.$store.dispatch('loadMatchesWithPredictions', { jwt: this.jwt })
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
