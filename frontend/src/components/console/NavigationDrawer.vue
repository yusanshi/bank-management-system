<template>
  <v-navigation-drawer v-model="localDrawer" :clipped="$vuetify.breakpoint.lgAndUp" app>
    <v-list>
      <template v-for="item in items">
        <v-row v-if="item.heading" :key="item.heading">
          <v-col cols="6">
            <v-subheader>
              {{ item.heading }}
            </v-subheader>
          </v-col>
        </v-row>
        <v-list-group
          v-else-if="item.children"
          :key="item.text"
          v-model="item.model"
          :prepend-icon="item.icon"
        >
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title>
                {{ item.text }}
              </v-list-item-title>
            </v-list-item-content>
          </template>
          <v-list-item
            v-for="(child, index) in item.children"
            :key="index"
            :to="child.to"
            exact
            link
          >
            <v-list-item-action v-if="child.icon">
              <v-icon>{{ child.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>
                {{ child.text }}
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-group>
        <v-list-item
          v-else
          :key="item.text"
          :to="item.to"
          exact
          link
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>
              {{ item.text }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </template>
    </v-list>
  </v-navigation-drawer>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  name: 'NavigationDrawer',
  props: ['items', 'value'],
  data() {
    return {
      localDrawer: this.value,
    };
  },
  watch: {
    value() {
      this.localDrawer = this.value;
    },
    localDrawer() {
      this.$emit('input', this.localDrawer);
    },
  },
});
</script>
