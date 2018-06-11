<template>
    <div class="match">
        <match-detail v-bind:num="match.num"
                      v-bind:city="match.city"
                      v-bind:stadium="match.stadium"
                      v-bind:date="match.date"
                      v-bind:time="match.time"
                      v-bind:timezone="match.timezone"
                      v-bind:group="match.group"
                      v-bind:team1="match.team1"
                      v-bind:team2="match.team2"
                      v-bind:score1="match.score1"
                      v-bind:score2="match.score2"></match-detail>
        <match-prediction v-bind:num="match.num"
                          v-bind:team1="match.team1"
                          v-bind:team2="match.team2"
                          v-bind:prediction="match.prediction"></match-prediction>
    </div>
</template>

<script>
import MatchDetail from '@/components/MatchDetail'
import MatchPrediction from '@/components/MatchPrediction'

export default {
    name: 'Match',
    components: {
        MatchDetail,
        MatchPrediction
    },
    props: {
        match: Object
    },
    data() {
        return {

        }
    }
}
</script>

<style scoped>
</style>
