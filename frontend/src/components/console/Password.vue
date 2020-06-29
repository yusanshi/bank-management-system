<template>
  <v-card max-width="500" class="mx-auto mt-12">
    <v-card-text>
      <v-form>
        <v-text-field
          label="旧密码"
          v-model="oldPassword"
          prepend-icon="mdi-lock"
          :append-icon="showOldPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showOldPassword ? 'text' : 'password'"
          @click:append="showOldPassword = !showOldPassword"
          clearable
        />
        <v-text-field
          label="新密码"
          v-model="newPassword"
          prepend-icon="mdi-lock-open"
          :append-icon="showNewPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showNewPassword ? 'text' : 'password'"
          @click:append="showNewPassword = !showNewPassword"
          clearable
        />
      </v-form>
    </v-card-text>

    <v-card-actions>
      <v-row justify="center">
        <v-btn class="ma-3" color="primary" @click="changePassword">确定</v-btn>
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue';
import { mapGetters, mapMutations, mapActions } from 'vuex';
import axios from 'axios';
/* eslint-disable @typescript-eslint/camelcase */

const API_URL = process.env.VUE_APP_API_URL;

export default Vue.extend({
  name: 'Password',
  metaInfo: {
    title: '密码修改',
  },
  data() {
    return {
      oldPassword: '',
      newPassword: '',
      showOldPassword: false,
      showNewPassword: false,
    };
  },
  computed: { ...mapGetters(['getToken']) },
  methods: {
    ...mapMutations(['setError', 'setSuccess']),
    ...mapActions(['logout']),
    changePassword() {
      axios
        .post(
          `${API_URL}/user/password`,
          { old_password: this.oldPassword, new_password: this.newPassword },
          {
            headers: { 'X-Token': this.getToken },
          },
        )
        .then(() => {
          this.setSuccess('密码修改成功，请重新登录');
          this.logout()
            .then(() => {
              this.$router.push({ path: '/login' });
            })
            .catch((error) => {
              this.setError(error.message);
            });
        })
        .catch((error) => {
          if (error.response && error.response.data.message) {
            this.setError(error.response.data.message);
          } else {
            this.setError(error.message);
          }
        });
    },
  },
});
</script>
