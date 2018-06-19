<template>
    <div>
        <div class="header-background">
            <div class="header-background-under"></div>
        </div>

        <div class="container">
            <div class="header">
                <nav>
                    <ul class="nav nav-pills pull-left">
                        <li>
                            <span class="fa fa-user"
                                  style="font-size: 24px;
                                         color: white;
                                         margin-top: 5px;
                                         padding-right: 10px;
                                         border-right:  solid 2px white;
                                         padding-top: 2px;
                                         padding-bottom: 2px;"
                                  v-on:click.stop.prevent="goToUserCP()">
                            </span><span class="fa fa-trophy"
                                         style="font-size: 24px;
                                                color: white;
                                                margin-top: 5px;
                                                padding-left: 10px;
                                                padding-top: 2px;
                                                padding-bottom: 2px;"
                                         v-on:click.stop.prevent="goToRanking()"></span>
                        </li>
                    </ul>
                    <ul class="nav nav-pills pull-right">
                        <li><logout></logout></li>
                    </ul>
                </nav>
                <account-info></account-info>
            </div>

            <div class="row matches">
                <match v-for="match in matches" v-bind:match="match" :key="match.num"></match>
            </div>
        </div>

    </div>
</template>

<script>
import { mapState } from 'vuex' 
import { mapMutations } from 'vuex'
import { key_jwt, key_user_data } from '@/common'
import Logout from '@/components/Logout'
import AccountInfo from '@/components/AccountInfo'
import Match from '@/components/Match'
import { fetchMatchesWithPredictions } from '@/api'

export default {
    name: 'Home',
    components: {
        Logout,
        AccountInfo,
        Match
    },
    data () {
        return {

        }
    },
    computed: mapState({
        matches: state => state.matches,
        jwt: function(state) {
            if (state.jwt) {
                return state.jwt 
            } else {
                return sessionStorage.getItem(key_jwt)
            }
        }
    }),
    beforeMount() {
        fetchMatchesWithPredictions(this.jwt)
            .then((response) => {
                if (response.status === 200) {
                    this.setMatches({ matches: response.data })
                }
            })
            .catch(error => {
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
            'setMatches',
            'setNotificationContent',
            'showNotification'
        ]),
        goToUserCP: function() {
            this.$router.push({ name: 'UserCP' })
        },
        goToRanking: function() {
            this.$router.push({ name: 'Ranking' })
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.header-background {
    background: linear-gradient(to right,
                              rgba(0, 78, 161, 1),
                              rgba(134, 60, 186, 1),
                              rgba(185, 35, 163, 1));
    /* background: linear-gradient(to right,
                              rgba(0, 78, 161, 1),
                              rgba(134, 60, 186, 1),
                              rgba(185, 35, 163, 1)),
                url('../assets/header_background_image.png'); */
    /* background-image: url('../assets/header_background_image.png'); */
    /* background-size: contain; */
    height: 350px;
    min-height: 350px;
    position: absolute;
    z-index: -99;
    width: 100%;
}

.header-background-under {
    z-index: -100;
    opacity: 0.5;
    background: black;
    top: 0;
    height: 350px;
    min-height: 350px;
    position: absolute;
    width: 100%;
}

.header, .matches {
    padding-right: 5px;
    padding-left: 5px;
}

/* Custom page header */
.header {
    position: relative;
    padding-top: 10px;
    padding-bottom: 10px;
    height: 350px;
    min-height: 350px;
}

/* Customize container */
@media (min-width: 768px) {
    .container {
        max-width: 730px;
        margin-top: 20px;
    }
}

/* Supporting matches content */
.matches {
    margin: 10px 0;
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
