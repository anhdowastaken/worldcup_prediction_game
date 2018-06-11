<template>
    <div class="match-detail">
        <div class="match-title">
            <span class="team-name">{{ team1.name }}</span> vs <span class="team-name">{{ team2.name }}</span>
        </div>
        <div class="match-result">
            <span class="team-score">{{ score1 }}</span> - <span class="team-score">{{ score2 }}</span>
        </div>
    </div>
</template>

<script>
export default {
    name: 'MatchDetail',
    props: {
        num: Number,
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
