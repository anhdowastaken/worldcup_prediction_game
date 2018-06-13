<template>
    <div class="match-prediction">
        <a href="#" v-on:click.prevent="submit(1)">{{ team1.name }} win</a>
        <a href="#" v-on:click.prevent="submit(0)">Draw</a>
        <a href="#" v-on:click.prevent="submit(2)">{{ team2.name }} win</a>
        <p v-if="currentPrediction != null">
            <span v-if="currentPrediction == 0">You predicted draw</span>
            <span v-else-if="currentPrediction == 1">You predicted {{ team1.name }} win</span>
            <span v-else-if="currentPrediction == 2">You predicted {{ team2.name }} win</span>
        </p>
    </div>
</template>

<script>
import { mapState } from 'vuex' 
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
            currentPrediction: this.prediction
        }
    },
    computed: mapState({
        jwt: state => state.jwt
    }),
    methods: {
        submit: function(prediction) {
            submitPrediction(this.jwt, this.num, prediction).then((response) => {
                this.currentPrediction = prediction
            })
        }
    }
}
</script>

<style scoped>
</style>
