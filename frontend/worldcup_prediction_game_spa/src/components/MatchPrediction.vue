<template>
    <div class="match-prediction">
        <a href="#" v-on:click.prevent="submitPrediction(1)">{{ team1.name }} win</a>
        <a href="#" v-on:click.prevent="submitPrediction(0)">Draw</a>
        <a href="#" v-on:click.prevent="submitPrediction(2)">{{ team2.name }} win</a>
        <p v-if="prediction != null">
            <span v-if="prediction == 0">You predicted draw</span>
            <span v-else-if="prediction == 1">You predicted {{ team1.name }} win</span>
            <span v-else-if="prediction == 2">You predicted {{ team2.name }} win</span>
        </p>
    </div>
</template>

<script>
export default {
    name: 'MatchPrediction',
    props: {
        num: Number,
        team1: Object,
        team2: Object,
        prediction: {
            type: Number,
            default: null
        }
    },
    data() {
        return {

        }
    },
    methods: {
        submitPrediction: function(prediction) {
            alert(prediction)
        }
    }
}
</script>

<style scoped>
