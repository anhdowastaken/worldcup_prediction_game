<template>

    <div class="col-lg-12 match-container">

        <div class="background">
            <div class="background-under">
                <!-- <p class="bg-text">{{ this.match.group }}</p> -->
            </div>
        </div>

        <div class="content">
            <div class="match-detail">
                <div v-if="didMatchEnd && isPredictionCorrect"
                      class="result-icon fa fa-thumbs-o-up"></div>
                <div v-if="didMatchEnd && !isPredictionCorrect"
                      class="result-icon fa fa-thumbs-o-down"></div>
                <div class="match-team-1">{{ this.match.team1.code }} {{ this.match.score1 }}</div>
                <div class="match-team-vs">:</div>
                <div class="match-team-2">{{ this.match.score2 }} {{ this.match.team2.code }}</div>
            </div>
        </div>

    </div>

</template>

<script>
export default {
    name: 'MatchSmall',
    props: {
        match: Object
    },
    data() {
        return {

        }
    },
    computed: {
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

            // Don't count if match has not started
            if (match['score1'] == null || match['score1'] == undefined || match['score2'] == null || match['score2'] == undefined) {
                return true
            } else if (score1 == null || score1 == undefined || score2 == null || score2 == undefined) { // Hmm, there is an unexpected problem
                return true
            } else if (!((prediction == 0 && score1 == score2) ||
                         (prediction == 1 && score1 > score2) ||
                         (prediction == 2 && score1 < score2))) { // Predict incorrectly
                return false
            } else {
                return true
            }
        }
    },
    methods: {

    }
}
</script>

<style scoped>
.match {
    font-family: localCenturyGothic, "Century Gothic", CenturyGothic, "Apple Gothic", AppleGothic, "URW Gothic L", "Avant Garde", Futura, sans-serif;
    margin-bottom: 10px;
    padding: 5px;
}

.match .match-container {
    height: 40px;
    min-height: 40px;
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

/* .match .background .background-under .bg-text {
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
} */

.match .content {
    color: #FFFFFF;
    text-align: center;
    padding: 5px;
}

.match .content .match-detail {
    font-size: 18px;
    font-weight: bold;
}

.match-team-1 {
    width: 45%;
    text-align: right;
}

.match-team-2 {
    width: 35%;
    text-align: left;
}

.match-team-vs {
    width: 10%;
    text-align: center;
}

.match-team-1,
.match-team-vs,
.match-team-2 {
    text-transform: uppercase;
    float: left;
    margin-top: 2px;
    margin-bottom: 10px;
}

.result-icon {
    float: right;
    font-size: 24px;
    color: white;
    margin-top: 2px;
    /* FIXME: z-index doesn't work */
    width: 10%;
}
</style>
