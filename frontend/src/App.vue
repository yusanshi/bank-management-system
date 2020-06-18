<template>
  <div id="app">
    <!-- TODO don't hard code the color -->
    <v-snackbar
      v-model="infoSnackbar"
      :timeout="2000"
      :top="true"
      color="#42A5F5"
    >
      {{ getInfo }}
    </v-snackbar>
    <v-snackbar
      v-model="successSnackbar"
      :timeout="2000"
      :top="true"
      color="#43A047"
    >
      {{ getSuccess }}
    </v-snackbar>
    <v-snackbar
      v-model="errorSnackbar"
      :timeout="2000"
      :top="true"
      color="#EF5350"
    >
      {{ getError }}
    </v-snackbar>
    <router-view />
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { mapGetters, mapMutations } from 'vuex';

export default Vue.extend({
  name: 'App',
  metaInfo: {
    titleTemplate: `%s - ${process.env.VUE_APP_SITE_NAME}`,
  },
  computed: {
    ...mapGetters(['getInfo', 'getSuccess', 'getError']),
  },
  data() {
    return {
      infoSnackbar: false,
      successSnackbar: false,
      errorSnackbar: false,
    };
  },
  methods: {
    ...mapMutations(['setInfo', 'setSuccess', 'setError']),
  },
  watch: {
    getInfo(val) {
      if (val !== '') {
        this.infoSnackbar = true;
      }
    },
    infoSnackbar(val) {
      if (!val) {
        this.setInfo('');
      }
    },

    getSuccess(val) {
      if (val !== '') {
        this.successSnackbar = true;
      }
    },
    successSnackbar(val) {
      if (!val) {
        this.setSuccess('');
      }
    },

    getError(val) {
      if (val !== '') {
        this.errorSnackbar = true;
      }
    },
    errorSnackbar(val) {
      if (!val) {
        this.setError('');
      }
    },
  },
});
</script>
