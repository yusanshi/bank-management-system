<template>
  <v-app>
    <v-main>
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="4">
            <v-alert icon="mdi-duck">账号：admin，密码：p@ssword</v-alert>
            <v-card class="elevation-12 mb-6">
              <v-toolbar color="primary" dark flat>
                <v-toolbar-title>登录</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form>
                  <v-text-field
                    label="用户名"
                    name="username"
                    v-model="username"
                    prepend-icon="mdi-account"
                    type="text"
                  />

                  <v-text-field
                    id="password"
                    label="密码"
                    name="password"
                    v-model="password"
                    prepend-icon="mdi-lock"
                    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="showPassword ? 'text' : 'password'"
                    @click:append="showPassword = !showPassword"
                  />
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer />
                <v-btn color="primary" @click="onLogin" :loading="loading"
                  >登录</v-btn
                >
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue';
import { mapGetters, mapMutations, mapActions } from 'vuex';

export default Vue.extend({
  name: 'Login',
  metaInfo: {
    title: '登录',
  },
  computed: {
    ...mapGetters(['logged']),
  },
  data() {
    return {
      loading: false,
      showPassword: false,
      username: '',
      password: '',
    };
  },
  methods: {
    ...mapMutations(['setError']),
    ...mapActions(['login']),
    onLogin() {
      this.loading = true;
      this.login({
        username: this.username,
        password: this.password,
      })
        .then(() => {
          this.$router.push({ path: '/console' });
        })
        .catch((error) => {
          this.setError(error.message);
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
  created() {
    if (this.logged) {
      this.$router.push({ path: '/console' });
    }
  },
});
</script>
