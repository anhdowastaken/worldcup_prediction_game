<template>
    <div class="match-detail">
        <div class="match-title">
            <h1>[{{ group }}] <span class="team-name">{{ team1.name }}</span> vs <span class="team-name">{{ team2.name }}</span></h1>
        </div>
        <div class="match-information">
            <div class="stadium">{{ stadium.name }}</div>
            <div class="location">{{ city }}</div>
            <div class="time"><span>{{ date }} {{ time }} {{ timezone }}</span></div>
        </div>
        <div class="match-result">
            <div class="match-score" v-if="score1 != null">
                <span class="team-score">{{ score1 }}</span> - <span class="team-score">{{ score2 }}</span>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'MatchDetail',
    props: {
        num: Number,
        city: String,
        stadium: Object,
        date: String,
        time: String,
        timezone: String,
        group: String,
        team1: Object,
        team2: Object,
        score1: Number,
        score2: Number
    },
    data() {
        return {

        }
    }
}
</script>

<style scoped>
</style>
