<template>
    <div class="col-lg-6 match">
        <div class="col-lg-12 match-container">

            <div class="background">
                <p class="bg-text">{{ this.match.group }}</p>
            </div>

            <div class="content">
                <span v-if="didMatchEnd && isPredictionCorrect"
                      class="result-icon fa fa-thumbs-o-up" style="color:white"></span>
                <span v-if="didMatchEnd && !isPredictionCorrect"
                      class="result-icon fa fa-thumbs-o-down" style="color:red"></span>

                <div class="match-detail">
                    <div class="match-title">
                        <p v-if="!didMatchEnd">{{ this.match.team1.name }} vs {{ this.match.team2.name }}</p>
                        <p v-if="didMatchEnd">{{ this.match.team1.name }} {{ this.match.score1 }} - {{ this.match.score2 }} {{ this.match.team2.name }}</p>
                    </div>
                    <div class="match-result">
                    </div>
                    <div class="match-information">
                        <p>{{ this.match.local_match_time }}</p>
                    </div>
                    <div class="match-predict-information">
                        <p v-if="enoughTimeToPredict">{{ timeToPredict }} to predict!</p>
                        <p v-else>This match can't be predicted</p>
                    </div>
                </div>

                <div class="match-prediction">
                    <button type="button"
                            class="btn btn-default"
                            v-bind:class="{ 'btn-success': isTeam1Chosen, 'disabled': !enoughTimeToPredict }"
                            v-bind:disabled="!enoughTimeToPredict"
                            v-on:click.stop.prevent="submit(1)">{{ this.match.team1.code }}</button>
                    <button type="button"
                            class="btn btn-default"
                            v-bind:class="{ 'btn-success': isDrawChosen, 'disabled': !enoughTimeToPredict }"
                            v-bind:disabled="!enoughTimeToPredict"
                            v-on:click.stop.prevent="submit(0)">DRAW</button>
                    <button type="button"
                            class="btn btn-default"
                            v-bind:class="{ 'btn-success': isTeam2Chosen, 'disabled': !enoughTimeToPredict }"
                            v-bind:disabled="!enoughTimeToPredict"
                            v-on:click.stop.prevent="submit(2)">{{ this.match.team2.code }}</button>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex' 
import { submitPrediction } from '@/api'
import { msToTime } from '@/utils'
import { key_jwt, key_user_data } from '@/common'

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
                return sessionStorage.getItem(key_jwt)
            }
        },
        enoughTimeToPredict: function() {
            // Replace "-" by "/" to avoid issue on Safari
            let match_time = this.match.date.replace(/-/g, "/") + ' ' + this.match.time + ' ' + (this.match.timezone ? this.match.timezone : '')
            let d = new Date(match_time)
            let diff = d.getTime() - Date.now()
            if (diff > 0) {
                return true
            } else {
                return false
            }
        },
        timeToPredict: function() {
            // Replace "-" by "/" to avoid issue on Safari
            let match_time = this.match.date.replace(/-/g, "/") + ' ' + this.match.time + ' ' + (this.match.timezone ? this.match.timezone : '')
            let d = new Date(match_time)
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
        },
        didMatchEnd: function() {
            if (this.match.score1 == null || this.match.score1 == undefined || this.match.score2 == null || this.match.score2 == undefined) {
                return false
            } else {
                return true
            }
        },
        isPredictionCorrect: function() {
            let match = this.match
            let prediction = match['prediction']
            let score1 = (match['score1'] ? match['score1'] : 0)
            score1 = score1 + (match['score1i'] ? match['score1i'] : 0)
            score1 = score1 + (match['score1et'] ? match['score1et'] : 0)
            score1 = score1 + (match['score1p'] ? match['score1p'] : 0)
            let score2 = (match['score2'] ? match['score2'] : 0)
            score2 = score2 + (match['score2i'] ? match['score2i'] : 0)
            score2 = score2 + (match['score2et'] ? match['score2et'] : 0)
            score2 = score2 + (match['score2p'] ? match['score2p'] : 0)

            // console.log(i + '-' + score1 + '-' + score2 + '-' + prediction)
            if (match['score1'] == null || match['score1'] == undefined || match['score2'] == null || match['score2'] == undefined) {
                return true
            } else if (score1 == null || score1 == undefined || score2 == null || score2 == undefined) {
                return true
            } else if (!((prediction == 0 && score1 == score2) ||
                         (prediction == 1 && score1 > score2) ||
                         (prediction == 2 && score1 < score2))) {
                return false
            } else {
                return true
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
.match {
    margin-bottom: 20px;
}

.match .match-container {
    height: 210px;
    min-height: 210px;
}

.match .background {
    position: absolute;
    z-index: -999999;
    display: block;
    min-height: 100%; 
    min-width: 100%;
    background: linear-gradient(to right, #B923A3, #863CBA, #024EA1, #004EA1);
    padding-top: 10px;
    padding-bottom: 10px;
    border-style: solid;
    border-width: 1px;
    border-color: #707070;
    border-radius: 15px;
    /* opacity: 0.9; */
    left: 0;
}

.match .background .bg-text {
    color: lightgray;
    font-size: 34px;
    opacity: 0.3;
    text-transform: uppercase;
    position: absolute;
    bottom: 0;
    right: 0;
    margin-right: 7px;
    margin-bottom: 7px;
    line-height: 80%;
    font-family: "Century Gothic", CenturyGothic, AppleGothic, sans-serif;
}

.match .content {
    color: #FFFFFF;
    text-align: center;
    padding: 10px;
}

.match .content .match-title {
    margin-top: 30px;
    font-family: "Century Gothic", CenturyGothic, AppleGothic, sans-serif;
    font-size: 18px;
    text-transform: uppercase;
}
.match .content .match-information {
    font-family: "Century Gothic", CenturyGothic, AppleGothic, sans-serif;
    font-size: 12px;
    text-transform: uppercase;
}

.match .content .match-predict-information {
    font-family: "Century Gothic", CenturyGothic, AppleGothic, sans-serif;
    font-size: 10px;
}
.result-icon {
    float: right;
    font-size: 24px;
}
</style>
