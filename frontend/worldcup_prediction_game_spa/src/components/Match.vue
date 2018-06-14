<template>
    <div class="col-lg-6 match">
        <div class="match-detail">
            <div class="match-title">
                <h4>[{{ this.match.group }}] <span class="team-name">{{ this.match.team1.name }}</span> vs <span class="team-name">{{ this.match.team2.name }}</span></h4>
            </div>
            <div class="match-information">
                <p>{{ this.match.local_match_time }}</p>
                <p v-if="enoughTimeToPredict">{{ timeToPredict }} to predict</p>
            </div>
            <div class="match-result">
                <div class="match-score" v-if="this.match.score1 != null">
                    <span class="team-score">{{ this.match.score1 }}</span> - <span class="team-score">{{ this.match.score2 }}</span>
                </div>
            </div>
        </div>

        <div class="match-prediction">
            <button type="button" class="btn btn-default" v-if="enoughTimeToPredict" v-on:click.prevent="submit(1)">{{ this.match.team1.code }}</button>
            <button type="button" class="btn btn-default" v-if="enoughTimeToPredict" v-on:click.prevent="submit(0)">DRAW</button>
            <button type="button" class="btn btn-default" v-if="enoughTimeToPredict" v-on:click.prevent="submit(2)">{{ this.match.team2.code }}</button>
            <p v-if="currentPrediction != null">
                <span v-if="currentPrediction == 0">You predicted a draw</span>
                <span v-else-if="currentPrediction == 1">You predicted {{ this.match.team1.name }} win</span>
                <span v-else-if="currentPrediction == 2">You predicted {{ this.match.team2.name }} win</span>
            </p>
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex' 
import { submitPrediction } from '@/api'
import { msToTime } from '@/utils'

export default {
    name: 'Match',
    props: {
        match: Object
    },
    data() {
        return {
            currentPrediction: this.match.prediction
        }
    },
    computed: mapState({
        jwt: function(state) {
            if (state.jwt) {
                return state.jwt 
            } else {
                return localStorage.jwt
            }
        },
        enoughTimeToPredict: function() {
            let match_time = this.match.date + ' ' + this.match.time + ' ' + (this.match.timezone ? this.match.timezone : '')
            let d = new Date(match_time)
            let diff = d.getTime() - Date.now()
            if (diff > 0) {
                return true
            } else {
                return false
            }
        },
        timeToPredict: function() {
            let match_time = this.match.date + ' ' + this.match.time + ' ' + (this.match.timezone ? this.match.timezone : '')
            let d = new Date(match_time)
            let diff = d.getTime() - Date.now()
            return msToTime(diff)
        }
    }),
    methods: {
        submit: function(prediction) {
            submitPrediction(this.jwt, this.match.num, prediction).then((response) => {
                this.currentPrediction = prediction
            })
        }
    }
}
</script>

<style scoped>
h4 {
  margin-top: 28px;
}</style>
