<template>
    <div class="home">
        <match v-for="match in matches" v-bind:match="match" :key="match.num"></match>
    </div>
</template>

<script>
import { fetchMatches } from '@/api'
import { fetchPredictions } from '@/api'
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
            fetchPredictions(1).then(response => {
                let predictions = response.data
                for (let i = 0; i < predictions.length; i++) {
                    let p = predictions[i]
                    for (let j = 0; j < this.matches.length; j++) {
                        if (this.matches[j].num == p.match_id) {
                            this.matches[j].prediction = p.prediction
                            break
                        }
                    }
                }
            })
        })
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
