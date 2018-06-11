<template>
    <div class="match-prediction">
        <a href="#" v-on:click.prevent="submit(1)">{{ team1.name }} win</a>
        <a href="#" v-on:click.prevent="submit(0)">Draw</a>
        <a href="#" v-on:click.prevent="submit(2)">{{ team2.name }} win</a>
        <p v-if="prediction != null">
            <span v-if="prediction == 0">You predicted draw</span>
            <span v-else-if="prediction == 1">You predicted {{ team1.name }} win</span>
            <span v-else-if="prediction == 2">You predicted {{ team2.name }} win</span>
        </p>
    </div>
</template>

<script>
import { submitPrediction } from '@/api'

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
        submit: function(prediction) {
            submitPrediction(1, this.num, prediction).then((response) => {
                this.prediction = prediction
            })
        }
    }
}
</script>

<style scoped>
