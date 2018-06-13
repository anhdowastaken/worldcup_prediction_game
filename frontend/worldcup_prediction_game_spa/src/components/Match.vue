<template>
    <div class="match">

        <div class="match-detail">
            <div class="match-title">
                <h1>[{{ this.match.group }}] <span class="team-name">{{ this.match.team1.name }}</span> vs <span class="team-name">{{ this.match.team2.name }}</span></h1>
            </div>
            <div class="match-information">
                <div class="stadium">{{ this.match.stadium.name }}</div>
                <div class="time"><span>{{ this.match.date }} {{ this.match.time }} {{ this.match.timezone }}</span></div>
            </div>
            <div class="match-result">
                <div class="match-score" v-if="this.match.score1 != null">
                    <span class="team-score">{{ this.match.score1 }}</span> - <span class="team-score">{{ this.match.score2 }}</span>
                </div>
            </div>
        </div>

        <div class="match-prediction">
            <a href="#" v-on:click.prevent="submit(1)">{{ this.match.team1.code }}</a>
            <a href="#" v-on:click.prevent="submit(0)">DRAW</a>
            <a href="#" v-on:click.prevent="submit(2)">{{ this.match.team2.code }}</a>
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
</style>
