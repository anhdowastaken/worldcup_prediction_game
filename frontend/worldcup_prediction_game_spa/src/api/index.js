const sample_matches = [{
    num: 2,
    date: "2014-06-13",
    time: "13:00",
    team1: {
      name: "Mexico",
      code: "MEX"
    },
    team2: {
      name: "Cameroon",
      code: "CMR"
    },
    score1: 1,
    score2: 0,
    score1i: null,
    score2i: null,
    goals: [{
      name: "Oribe Peralta",
      team: {
        name: "Mexico",
        code: "MEX"
      },
      minute: 61,
      score1: 1,
      score2: 0
    }],
    group: "Group A"
  },
  {
    num: 3,
    date: "2014-06-13",
    time: "16:00",
    team1: {
      name: "Spain",
      code: "ESP"
    },
    team2: {
      name: "Netherlands",
      code: "NED"
    },
    score1: 1,
    score2: 5,
    score1i: null,
    score2i: null,
    goals: [{
        name: "Xabi Alonso",
        team: {
          name: "Spain",
          code: "ESP"
        },
        minute: 27,
        score1: 1,
        score2: 0,
        penalty: true
      },
      {
        name: "Robin Van Persie",
        team: {
          name: "Netherlands",
          code: "NED"
        },
        minute: 44,
        score1: 1,
        score2: 1
      },
      {
        name: "Arjen Robben",
        team: {
          name: "Netherlands",
          code: "NED"
        },
        minute: 53,
        score1: 1,
        score2: 2
      },
      {
        name: "Stefan De Vrij",
        team: {
          name: "Netherlands",
          code: "NED"
        },
        minute: 65,
        score1: 1,
        score2: 3
      },
      {
        name: "Robin Van Persie",
        team: {
          name: "Netherlands",
          code: "NED"
        },
        minute: 72,
        score1: 1,
        score2: 4
      },
      {
        name: "Arjen Robben",
        team: {
          name: "Netherlands",
          code: "NED"
        },
        minute: 80,
        score1: 1,
        score2: 5
      }
    ],
    group: "Group B",
    stadium: {
      key: "fontenova",
      name: "Arena Fonte Nova"
    },
    city: "Salvador",
    timezone: "UTC-3"
  },
  {
    num: 4,
    date: "2014-06-13",
    time: "18:00",
    team1: {
      name: "Chile",
      code: "CHI"
    },
    team2: {
      name: "Australia",
      code: "AUS"
    },
    score1: 3,
    score2: 1,
    score1i: null,
    score2i: null,
    goals: [{
        name: "Alexis Sánchez",
        team: {
          name: "Chile",
          code: "CHI"
        },
        minute: 12,
        score1: 1,
        score2: 0
      },
      {
        name: "Jorge Valdívia",
        team: {
          name: "Chile",
          code: "CHI"
        },
        minute: 14,
        score1: 2,
        score2: 0
      },
      {
        name: "Cahill",
        team: {
          name: "Australia",
          code: "AUS"
        },
        minute: 35,
        score1: 2,
        score2: 1
      },
      {
        name: "Jean Beausejour",
        team: {
          name: "Chile",
          code: "CHI"
        },
        minute: 90,
        offset: 2,
        score1: 3,
        score2: 1
      }
    ],
    group: "Group B",
    stadium: {
      key: "pantanal",
      name: "Arena Pantanal"
    },
    city: "Cuiabá",
    timezone: "UTC-4"
  }
]

import axios from 'axios'

const API_URL = 'http://127.0.0.1:5000/api'

export function fetchMatchesWithPredictions(jwt) {
    return axios.create({withCredentials: true})
                .get(`${API_URL}/get_matches_with_prediction`,
                     { headers: { Authorization: `Bearer: ${jwt}` } }
                    )
}

export function submitPrediction(jwt, match_id, prediction) {
    return axios.create({withCredentials: true})
                .post(`${API_URL}/submit_prediction`,
                      { match_id: match_id,
                        prediction: prediction
                      },
                      { headers: { Authorization: `Bearer: ${jwt}` } }
                    )
}

export function submitLogin(username, password) {
    return axios.create({withCredentials: true})
                .post(`${API_URL}/login`,
                      { username: username,
                        password: password
                      }
                    )
}

export function submitLogout(jwt) {
    return axios.create({withCredentials: true})
                .post(`${API_URL}/logout`)
}

export function submitRegister(jwt, username) {
    return axios.create({withCredentials: true})
                .post(`${API_URL}/register`,
                      { username: username },
                      { headers: { Authorization: `Bearer: ${jwt}` } }
                    )
}

export function submitResetPassword(jwt, username) {
    return axios.create({withCredentials: true})
                .post(`${API_URL}/reset_password`,
                      { username: username },
                      { headers: { Authorization: `Bearer: ${jwt}` } }
                    )
}

export function submitChangePassword(jwt, old_password, new_password) {
    return axios.create({withCredentials: true})
                .post(`${API_URL}/change_password`,
                      { old_password: old_password, new_password: new_password },
                      { headers: { Authorization: `Bearer: ${jwt}` } }
                    )
}

export function getRanking(jwt) {
    return axios.create({withCredentials: true})
                .get(`${API_URL}/get_ranking`,
                      { headers: { Authorization: `Bearer: ${jwt}` } }
                    )
}
