<template>
    <div v-if="userData">
        <h3 class="text-muted">{{ this.userData['username'] }}</h3>
        <p>Last login: {{ this.userData['last_login_at'] }}</p>
        <p><span v-show="point > 0">-</span>{{ this.point }} point<span v-show="point > 0">s</span></p>
    </div>
</template>

<script>
import { mapState } from 'vuex' 
import { isEmpty } from '@/utils'
import { key_jwt, key_user_data } from '@/common'

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
                let ret = sessionStorage.getItem(key_user_data)
                if (ret) {
                    return JSON.parse(sessionStorage.getItem(key_user_data))
                } else {
                    return null
                }
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

                // console.log(i + '-' + score1 + '-' + score2 + '-' + prediction)
                if (match['score1'] == null || match['score1'] == undefined || match['score2'] == null || match['score2'] == undefined) {
                    continue
                } else if (score1 == null || score1 == undefined || score2 == null || score2 == undefined) {
                    continue
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
