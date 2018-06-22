<template>
    <div class="col-lg-6 match"
         v-bind:class="{ 'most-recent': this.match.most_recent }">
        <match-small v-if="hasMatchResult"
                     v-show="!expand"
                     v-bind:match="match"
                     v-on:click.native="toggleExpand()"></match-small>
        <match-big v-show="expand"
                   v-bind:match="match"
                   v-on:click.native="toggleExpand()"></match-big>
    </div>
</template>

<script>
import { mapState } from 'vuex' 
import { mapMutations } from 'vuex'
import { submitPrediction } from '@/api'
import { key_jwt, key_user_data } from '@/common'
import MatchBig from '@/components/MatchBig'
import MatchSmall from '@/components/MatchSmall'

export default {
    name: 'Match',
    components: {
        MatchBig,
        MatchSmall
    },
    props: {
        match: Object
    },
    data() {
        return {
            expand: true // Default value
        }
    },
    created: function() {
        // After component is created completely, decide how to display
        if (window.innerWidth > 768) { // FIXME: Small screen size is hard-code here
            // Always expand with big screen size
            this.expand = true
        } else {
            this.expand = !this.hasMatchResult
        }
    },
    computed: {
        hasMatchResult: function() {
            if (this.match.score1 != null && this.match.score1 != undefined && this.match.score2 != null && this.match.score2 != undefined) {
                return true
            } else {
                return false
            }
        }
    },
    methods: {
        toggleExpand: function() {
            if (window.innerWidth > 768 || !this.hasMatchResult) { // FIXME: Small screen size is hard-code here
                // Always expand with big screen size
                // and do not collapse if the match doesn't have result
                this.expand = true
            } else {
                this.expand = !this.expand
            }
        }
    }
}
</script>

<style scoped>
.match {
    font-family: localCenturyGothic, "Century Gothic", CenturyGothic, "Apple Gothic", AppleGothic, "URW Gothic L", "Avant Garde", Futura, sans-serif;
    margin-bottom: 10px;
    padding: 5px;
}
</style>
