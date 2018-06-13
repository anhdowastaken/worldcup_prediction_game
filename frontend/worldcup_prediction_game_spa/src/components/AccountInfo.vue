<template>
    <div>
        <h3>[{{ this.userData['user_id'] }}] {{ this.userData['username'] }}</h3>
        <p>Last login: {{ this.userData['last_login_at'] }}</p>
        <p>-{{ this.point }} point(s)</p>
    </div>
</template>

<script>
import { mapState } from 'vuex' 
import { isEmpty } from '@/utils'

export default {
    name: 'AccountInfo',
    data() {
        return {

        }
    },
    computed: mapState({
        matches: state => state.matches,
        userData: function(state) {
            if (!isEmpty(state.userData)) {
                return state.userData
            } else {
                return JSON.parse(localStorage.getItem('user_data'))
            }
        },
        point: function() {
            let current_point = 0;

            for (let i = 0; i < this.matches.length; i++) {
                let match = this.matches[i]
                let prediction = match['prediction']
                let score1 = (match['score1'] ? match['score1'] : 0)
                score1 = score1 + (match['score1i'] ? match['score1i'] : 0)
                score1 = score1 + (match['score1et'] ? match['score1et'] : 0)
                score1 = score1 + (match['score1p'] ? match['score1p'] : 0)
                let score2 = (match['score2'] ? match['score2'] : 0)
                score2 = score2 + (match['score2i'] ? match['score2i'] : 0)
                score2 = score2 + (match['score2et'] ? match['score2et'] : 0)
                score2 = score2 + (match['score2p'] ? match['score2p'] : 0)

                if (!score1 || !score2) {
                    current_point = current_point + 0
                } else if (!((prediction == 0 && score1 == score2) ||
                             (prediction == 1 && score1 > score2) ||
                             (prediction == 2 && score1 < score2))) {
                    current_point = current_point + 10
                }
            }

            return current_point
        }
    })
}
</script>

<style scoped>
</style>
