<template>
    <div class="match-prediction">
        <a href="#">{{ team1.name }} win</a>
        <a href="#">Draw</a>
        <a href="#">{{ team2.name }} win</a>
    </div>
</template>

<script>
export default {
    name: 'MatchPrediction',
    props: {
        num: Number,
        team1: Object,
        team2: Object
    },
    data() {
        return {

        }
    }
}
</script>

<style scoped>
