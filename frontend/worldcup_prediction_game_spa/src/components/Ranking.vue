<template>
    <div class="container">
        <div class="background-under"></div>
        <div class="background"></div> 

        <div class="header">
            <nav>
                <ul class="nav nav-pills pull-left">
                    <li><span class="fa fa-chevron-left"
                              style="font-size:24px;
                                     color:white;
                                     padding-top:2px;
                                     margin-top:2px;
                                     cursor: pointer;"
                              v-on:click.stop.prevent="goBack"></span></li>
                </ul>
 
                <ul class="nav nav-pills pull-right">
                    <li><logout></logout></li>
                </ul>
            </nav>
        </div>

        <loader v-if="!isFetchingCompleted"></loader>
        <div v-else class="ranking">
            <div class="ranking-header">Top ocschos</div>
            <div class="ranking-table">
                <table>
                    <tr v-for="(record, index) in ranking" :key="record.id">
                        <td style="padding-right: 10px;">{{ index + 1 }}.</td>
                        <td >{{ record.username }}</td>
                        <td style="padding-left: 80px;">{{ record.point }}p</td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex' 
import { mapMutations } from 'vuex'
import { key_jwt, key_user_data } from '@/common'
import { getRanking } from '@/api'
import Logout from '@/components/Logout'
import Loader from '@/components/Loader'

export default {
    name: 'Ranking',
    components: {
        Logout,
        Loader
    },
    data () {
        return {
            isFetchingCompleted: false,
            ranking: []
        }
    },
    computed: mapState({
        jwt: function(state) {
            if (state.jwt) {
                return state.jwt 
            } else {
                return sessionStorage.getItem(key_jwt)
            }
        }
    }),
    beforeMount() {
        // this.$store.dispatch('loadMatchesWithPredictions', { jwt: this.jwt })
        getRanking(this.jwt)
            .then(response => {
                this.isFetchingCompleted = true
                if (response.status === 200) {
                    this.ranking = response.data['ranking']
                }
            })
            .catch(error => {
                this.isFetchingCompleted = true
                if (error.response.data['message']) {
                    // There is problem with authentication
                    // Back to login
                    if (error.response.status == 401) {
                        alert(error.response.data['message'])
                        this.$store.dispatch('logout')
                    } else {
                        this.setNotificationContent({ header: 'Error',
                                                      body: error.response.data['message'] })
                        this.showNotification()
                    }
                } else if (error) {
                    this.setNotificationContent({ header: 'Error',
                                                  body: error })
                    this.showNotification()
                } else {
                    this.setNotificationContent({ header: 'Error',
                                                  body: 'Error' })
                    this.showNotification()
                }
            })
    },
    methods: {
        ...mapMutations([
            'setNotificationContent',
            'showNotification'
        ]),
        goBack: function() {
            if (window.history.length > 1) {
                this.$router.go(-1)
            } else {
                this.$router.push('/')
            }
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.container {
    position: relative;
    height: 100vh;
}

.background {
    background: linear-gradient(to right,
                              rgba(0, 78, 161, 1),
                              rgba(134, 60, 186, 1),
                              rgba(185, 35, 163, 1));
    position: absolute;
    z-index: -2;
    width: 100%;
    top: 0;
    bottom: 0;
    left: 0;
}

.background-under {
    z-index: -1;
    opacity: 0.5;
    background: black;
    top: 0;
    bottom: 0;
    position: absolute;
    width: 100%;
    left: 0;
}

.header {
    position: relative;
    padding-top: 10px;
    padding-bottom: 10px;
    padding-right: 5px;
    padding-left: 5px;
    height: 70px;
    min-height: 70px;
}

.ranking {
    color: white;
    font-family: localCenturyGothic, "Century Gothic", CenturyGothic, "Apple Gothic", AppleGothic, "URW Gothic L", "Avant Garde", Futura, sans-serif;
    padding-right: 5px;
    padding-left: 5px;
}

.ranking .ranking-header {
    border-bottom: solid 2px white;
    display: inline;
    padding-bottom: 5px;
    text-transform: uppercase;
    font-weight: bold;
    font-size: 38px;
}

.ranking .ranking-table {
    margin-top: 20px;
    font-size: 24px;
}

.ranking .ranking-table tr td {
    /* padding-right: 20px; */
}

/* Customize container */
@media (min-width: 768px) {
    .container {
        max-width: 730px;
        margin-top: 20px;
    }
}

/* Responsive: Portrait tablets and up */
@media screen and (min-width: 768px) {
    /* Remove the padding we set earlier */
    .header,
    .matches {
        padding-right: 0;
        padding-left: 0;
    }
    /* Space out the masthead */
    .header {
        margin-bottom: 10px;
    }
}
</style>
