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

export function fetchMatchesWithPredictions(user_id) {
    return axios.get(`${API_URL}/get_matches_with_prediction/user_id/${user_id}`)
}

export function submitPrediction(user_id, match_id, prediction) {
    return axios.post(`${API_URL}/submit_prediction`,
                      { user_id: user_id,
                        match_id: match_id,
                        prediction: prediction
                      })
}
