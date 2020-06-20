import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);

const API_URL = process.env.VUE_APP_API_URL;

const userString = localStorage.getItem('user');
export default new Vuex.Store({
  state: {
    // If `user` in localStorage and not expired, restore it
    user: (userString !== null && JSON.parse(userString).expiresAt > Math.floor(Date.now() / 1000))
      ? JSON.parse(userString) : {
        username: null,
        token: null,
        expiresAt: null,
      },
    info: '',
    success: '',
    error: '',
  },
  getters: {
    logged(state) {
      return state.user.token !== null;
    },
    getToken(state) {
      return state.user.token;
    },
    getUser(state) {
      return state.user;
    },
    getInfo(state) {
      return state.info;
    },
    getSuccess(state) {
      return state.success;
    },
    getError(state) {
      return state.error;
    },
  },
  mutations: {
    setUser(state, payload) {
      state.user = payload;
    },
    setInfo(state, payload) {
      state.info = payload;
    },
    setSuccess(state, payload) {
      state.success = payload;
    },
    setError(state, payload) {
      state.error = payload;
    },

  },
  actions: {
    login({ commit }, payload) {
      return new Promise((resolve, reject) => {
        axios.post(`${API_URL}/user/login`,
          {
            username: payload.username,
            password: payload.password,
          })
          .then((response) => {
            const user = {
              username: payload.username,
              token: (response.data as any).token,
              // expiresAt: Math.floor(Date.now() / 1000) + response.data.expires,
              expiresAt: Math.floor(Date.now() / 1000) + 365 * 24 * 60 * 60, // backend/issues/1
            };
            commit('setUser', user);
            localStorage.setItem('user', JSON.stringify(user));
            resolve();
          }).catch((error) => {
            if (error.response && error.response.data.message) {
              reject(error.response.data);
            } else {
              reject(error);
            }
          });
      });
    },
    logout({ commit, getters }) {
      return new Promise((resolve, reject) => {
        axios.post(`${API_URL}/user/logout`, {}, {
          headers: { 'X-Token': getters.getToken },
        })
          .then(() => {
            commit('setUser', {
              username: null,
              token: null,
              expiresAt: null,
            });
            localStorage.removeItem('user');
            resolve();
          }).catch((error) => {
            if (error.response && error.response.data.message) {
              reject(error.response.data);
            } else {
              reject(error);
            }
          });
      });
    },
  },
});
