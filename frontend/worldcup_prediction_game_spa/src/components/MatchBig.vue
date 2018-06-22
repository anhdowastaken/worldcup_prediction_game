<template>
    <div class="col-lg-12 match-container">

        <div class="background">
            <div class="background-under">
                <p class="bg-text">{{ this.match.group }}</p>
            </div>
        </div>

        <div class="content">
            <div v-if="didMatchEnd && isPredictionCorrect"
                  class="result-icon fa fa-thumbs-o-up"></div>
            <div v-if="didMatchEnd && !isPredictionCorrect"
                  class="result-icon fa fa-thumbs-o-down"></div>

            <div class="match-detail">
                <div class="match-information">
                    <span>{{ this.match.local_match_time }}</span>
                </div>
                <div class="match-predict-information">
                    <span v-if="enoughTimeToPredict">{{ timeToPredict }} to predict!</span>
                    <span v-else>This match can't be predicted</span>
                </div>
                <div class="match-title">
                    <div v-if="!didMatchEnd" class="match-title-one-line">
                        <div class="match-team-1">{{ this.match.team1.name }}</div>
                        <div class="match-team-vs">:</div>
                        <div class="match-team-2">{{ this.match.team2.name }}</div>
                    </div>
                    <div v-else>
                        <div class="match-result-line1">
                            <div class="match-team-1">{{ this.match.score1 }}</div>
                            <div class="match-team-vs">:</div>
                            <div class="match-team-2">{{ this.match.score2 }}</div>
                        </div>
                        <div class="match-result-line2">
                            <div class="match-team-1">{{ this.match.team1.name }}</div>
                            <div class="match-team-vs"></div>
                            <div class="match-team-2">{{ this.match.team2.name }}</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="match-prediction">
                <button type="button"
                        class="btn btn-default"
                        v-bind:class="{ 'btn-success': isTeam1Chosen, 'disabled': !enoughTimeToPredict }"
                        v-bind:disabled="!enoughTimeToPredict || !isHttpRequestCompleted"
                        v-on:click.stop.prevent="submit(1)">{{ this.match.team1.code }}</button>
                <button type="button"
                        class="btn btn-default"
                        v-bind:class="{ 'btn-success': isDrawChosen, 'disabled': !enoughTimeToPredict }"
                        v-bind:disabled="!enoughTimeToPredict || !isHttpRequestCompleted"
                        v-on:click.stop.prevent="submit(0)">DRAW</button>
                <button type="button"
                        class="btn btn-default"
                        v-bind:class="{ 'btn-success': isTeam2Chosen, 'disabled': !enoughTimeToPredict }"
                        v-bind:disabled="!enoughTimeToPredict || !isHttpRequestCompleted"
                        v-on:click.stop.prevent="submit(2)">{{ this.match.team2.code }}</button>
            </div>
        </div>

    </div>
</template>

<script>
import { mapState } from 'vuex' 
import { mapMutations } from 'vuex'
import { submitPrediction } from '@/api'
import { msToTime } from '@/utils'
import { key_jwt, key_user_data } from '@/common'

export default {
    name: 'MatchBig',
    props: {
        match: Object
    },
    data() {
        return {
            timeToPredict: '',
            enoughTimeToPredict: false,
            currentPrediction: this.match.prediction,
            isHttpRequestCompleted: true
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
    mounted: function() {
        this.calculateTimeToPredict()
    },
    methods: {
        ...mapMutations([
            'setNotificationContent',
            'showNotification',
            'setNotificationRedirectAfterClose'
        ]),
        calculateTimeToPredict: function() {
            let match_time = this.match.date.replace(/-/g, "/") + ' ' + this.match.time + ' ' + (this.match.timezone ? this.match.timezone : '')
            let d = new Date(match_time)
            let diff = d.getTime() - Date.now()

            if (diff > 0) {
                this.enoughTimeToPredict = true
                // Show second if diff time is under 1 hour
                if (diff > 0 && diff < 60 * 60 * 1000) {
                    this.timeToPredict = msToTime(diff, true, true, true, true)
                } else {
                    this.timeToPredict = msToTime(diff)
                }
                // Create countdown
                setTimeout(() => {
                    this.calculateTimeToPredict()
                }, 1000)
            } else {
                this.enoughTimeToPredict = false
            }
        },
        submit: function(prediction) {
            if (prediction != this.currentPrediction) {
                this.isHttpRequestCompleted = false
                submitPrediction(this.jwt, this.match.num, prediction)
                    .then(response => {
                        this.isHttpRequestCompleted = true
                        if (response.status === 201) {
                            this.currentPrediction = prediction
                        }
                    })
                    .catch(error => {
                        this.isHttpRequestCompleted = true
                        if (error.response.data['message']) {
                            this.setNotificationContent({ header: 'Error',
                                                          body: error.response.data['message'] })
                            this.showNotification()
                            // There is problem with authentication
                            // Back to login
                            if (error.response.status == 401) {
                                this.setNotificationRedirectAfterClose({ redirect: true,
                                                                         component_name: 'Login' })
                                this.$store.dispatch('logout')
                            }
                        } else if (error) {
                            this.setNotificationContent({ header: 'Error',
                                                          body: error })
                            this.showNotification()
                        } else {
                            this.setNotificationContent({ header: 'Error',
                                                          body: 'Error' })
                            this.showNotification()
                        }
                    })
            }
        }
    }
}
</script>

<style scoped>
.match .match-container {
    height: 210px;
    min-height: 210px;
    padding: 5px;
}

.match .background, .match .background .background-under {
    position: absolute;
    display: block;
    min-height: 100%; 
    min-width: 100%;
    border-radius: 15px;
    left: 0;
}

.match .background {
    z-index: -1;
    padding-top: 10px;
    padding-bottom: 10px;
    border-style: solid;
    border-width: 1px;
    border-color: #707070;
    background: linear-gradient(-235deg, #004EA1, #863CBA, #B923A3);
}

.match .background .background-under {
    z-index: -2;
    opacity: 0.5;
    background: black;
    top: 0;
}

.match .background .background-under .bg-text {
    color: lightgray;
    font-size: 28px;
    opacity: 0.3;
    text-transform: uppercase;
    position: absolute;
    bottom: 0;
    right: 0;
    margin-right: 7px;
    margin-bottom: 7px;
    line-height: 80%;
}

.match .content {
    color: #FFFFFF;
    text-align: center;
    padding: 5px;
}

.match .content .match-title {
    font-size: 18px;
    font-weight: bold;
}
.match .content .match-information {
    margin-top: 30px;
    font-size: 12px;
    text-transform: uppercase;
    font-weight: bold;
}

.match .content .match-predict-information {
    font-size: 10px;
    margin-top: 5px;
}

.match-title .match-title-one-line .match-team-1,
.match-title .match-title-one-line .match-team-vs,
.match-title .match-title-one-line .match-team-2 {
    float: left;
    margin-top: 18px;
    margin-bottom: 18px;
}

.match-team-1, .match-team-2 {
    width: 45%;
    text-transform: uppercase;
}

.match-team-1 {
    text-align: right;
}

.match-team-vs {
    width: 10%;
    text-align: center;
}

.match-team-2 {
    text-align: left;
}

.match-result-line1 {
    font-size: 22px;
}

.match-result-line2 {
    font-size: 8px;
}

.match-result-line1 .match-team-1,
.match-result-line1 .match-team-vs,
.match-result-line1 .match-team-2 {
    float: left;
    margin-top: 10px;
    margin-bottom: 0;
}

.match-result-line2 .match-team-1,
.match-result-line2 .match-team-vs,
.match-result-line2 .match-team-2 {
    float: left;
    margin-top: 0;
    margin-bottom: 10px;
}

.result-icon {
    float: right;
    font-size: 24px;
    color: white;
    margin-top: 2px;
    width: 10%;
}
</style>
