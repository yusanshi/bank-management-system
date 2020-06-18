<template>
  <v-app>
    <NavigationDrawer :items="drawerItems" v-model="drawer" />
    <v-app-bar :clipped-left="$vuetify.breakpoint.lgAndUp" app color="blue darken-3" dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title style="width: 300px" class="ml-0 pl-4">
        <span class="hidden-sm-and-down">{{ siteName }}</span>
      </v-toolbar-title>
      <v-spacer />
      <v-toolbar-items>
        <v-btn icon @click="toggleFullscreen">
          <v-icon v-if="inFullscreen">mdi-fullscreen-exit</v-icon>
          <v-icon v-else>mdi-fullscreen</v-icon>
        </v-btn>
        <v-menu offset-y origin="center center" transition="scale-transition">
          <template v-slot:activator="{ on }">
            <v-btn icon large text slot="activator" v-on="on">
              <v-avatar>
                <v-icon>mdi-account-circle</v-icon>
              </v-avatar>
            </v-btn>
          </template>
          <v-list class="pa-0">
            <v-list-item
              v-for="(item, index) in topRightItems"
              v-on="item.click ? { click: item.click } : {}"
              :to="item.to"
              :key="index"
            >
              <v-list-item-action v-if="item.icon">
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-toolbar-items>
    </v-app-bar>
    <v-content>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-content>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue';
import { mapGetters, mapMutations, mapActions } from 'vuex';
import NavigationDrawer from '@/components/console/NavigationDrawer.vue';

export default Vue.extend({
  name: 'Console',
  components: {
    NavigationDrawer,
  },
  computed: {
    ...mapGetters(['logged', 'getError']),
    siteName() {
      return process.env.VUE_APP_SITE_NAME;
    },
  },
  data() {
    return {
      // Using null to initialize the drawer
      // as closed on mobile and as open on desktop
      drawer: null,
      inFullscreen: false,
      drawerItems: [
        { heading: '业务管理' },
        {
          icon: 'mdi-chart-bar',
          text: '仪表盘',
          to: '/console',
        },
        {
          icon: 'mdi-account-box-multiple',
          text: '客户管理',
          to: '/console/client',
        },
        {
          icon: 'mdi-folder-account',
          text: '账户管理',
          to: '/console/account',
        },
        {
          icon: 'mdi-account-cash',
          text: '贷款管理',
          to: '/console/loan',
        },
        { heading: '其他' },
        {
          icon: 'mdi-cog',
          text: '密码修改',
          to: '/console/password',
        },
      ],
      topRightItems: [
        {
          icon: 'mdi-logout',
          title: '退出',
          click: (this as any).onLogout,
        },
      ],
    };
  },
  methods: {
    ...mapMutations(['setError']),
    ...mapActions(['logout']),
    onLogout() {
      this.logout()
        .then(() => {
          this.$router.push({ path: '/login' });
        })
        .catch((error) => {
          this.setError(error.message);
        });
    },
    toggleFullscreen() {
      if (document.fullscreenElement !== null) {
        document.exitFullscreen();
        this.inFullscreen = false;
      } else {
        document.documentElement.requestFullscreen();
        this.inFullscreen = true;
      }
    },
  },
  created() {
    if (!this.logged) {
      this.$router.push({ path: '/login' });
      this.setError('您还没有登录');
    }
  },
});
</script>
