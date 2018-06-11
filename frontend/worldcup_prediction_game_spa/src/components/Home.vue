<template>
    <div class="home">
        <match v-for="match in matches" v-bind:match="match" :key="match.num"></match>
    </div>
</template>

<script>
import { fetchMatches } from '@/api'
import Match from '@/components/Match'

export default {
    name: 'Home',
    components: {
        Match
    },
    data () {
        return {
            matches: []
        }
    },
    beforeMount() {
        fetchMatches().then(response => {
            this.matches = response.data
        })
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
