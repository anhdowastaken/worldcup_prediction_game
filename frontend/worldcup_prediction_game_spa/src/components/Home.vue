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
        matches: state => state.matches
    }),
    beforeMount() {
        // // FIXME: Hard code user_id
        this.$store.dispatch('loadMatchesWithPredictions', { user_id: 1})
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
