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
            <button type="button"
                    class="btn btn-default"
                    v-if="enoughTimeToPredict"
                    v-bind:class="{ 'btn-success': isTeam1Chosen }"
                    v-on:click.prevent="submit(1)">{{ this.match.team1.code }}</button>
            <button type="button"
                    class="btn btn-default"
                    v-if="enoughTimeToPredict"
                    v-bind:class="{ 'btn-success': isDrawChosen }"
                    v-on:click.prevent="submit(0)">DRAW</button>
            <button type="button"
                    class="btn btn-default"
                    v-if="enoughTimeToPredict"
                    v-bind:class="{ 'btn-success': isTeam2Chosen }"
                    v-on:click.prevent="submit(2)">{{ this.match.team2.code }}</button>
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
            // Replace "-" by "/" to avoid issue on Safari
            let d = new Date(match_time.replace(/-/g, "/"))
            let diff = d.getTime() - Date.now()
            if (diff > 0) {
                return true
            } else {
                return false
            }
        },
        timeToPredict: function() {
            let match_time = this.match.date + ' ' + this.match.time + ' ' + (this.match.timezone ? this.match.timezone : '')
            // Replace "-" by "/" to avoid issue on Safari
            let d = new Date(match_time.replace(/-/g, "/"))
            let diff = d.getTime() - Date.now()
            return msToTime(diff)
        },
        isTeam1Chosen: function() {
            if (this.currentPrediction == 1) {
                return true
            } else {
                return false
            }
        },
        isTeam2Chosen: function() {
            if (this.currentPrediction == 2) {
                return true
            } else {
                return false
            }
        },
        isDrawChosen: function() {
            if (this.currentPrediction == 0) {
                return true
            } else {
                return false
            }
        }
    }),
    methods: {
        submit: function(prediction) {
            if (prediction != this.currentPrediction) {
                submitPrediction(this.jwt, this.match.num, prediction)
                    .then(response => {
                        if (response.status === 201) {
                            this.currentPrediction = prediction
                        }
                    })
                    .catch(error => {
                        if (error.response.data['message']) {
                            // TODO: Use HTML dialog
                            alert(error.response.data['message'])
                        } else if (error) {
                            alert(error)
                        } else {
                            alert('Error')
                        }
                    })
            }
        }
    }
}
</script>

<style scoped>
h4 {
  margin-top: 28px;
}</style>
