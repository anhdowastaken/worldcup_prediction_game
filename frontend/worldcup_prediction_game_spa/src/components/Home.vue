<template>
    <div class="home">
        <logout></logout>
        <match v-for="match in matches" v-bind:match="match" :key="match.num"></match>
    </div>
</template>

<script>
import { fetchMatchesWithPredictions } from '@/api'
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
            matches: []
        }
    },
    beforeMount() {
        // FIXME: Hard code user_id
        fetchMatchesWithPredictions(1).then(response => {
            this.matches = response.data
        })
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
