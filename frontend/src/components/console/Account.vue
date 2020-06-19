<template>
  <div>
      <Table :meta="meta" :items="items" @add="add" @edit="edit" @remove="remove"/>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Table from '@/components/Table.vue';

export default Vue.extend({
  name: 'Account',
  metaInfo: {
    title: '账户管理',
  },
  components: {
    Table,
  },
  data() {
    return {
      meta: {
        title: '账户',
        default: {
          id: '0',
          balance: 0,
          opentime: '',
        },
        headers: [
          {
            text: 'ID',
            value: 'id',
          },
          {
            text: '余额',
            value: 'balance',
          },
          {
            text: '办理时间',
            value: 'opentime',
          },
        ],
      },
      items: [
        {
          id: '00001',
          balance: 54,
          opentime: 521,
        },
        {
          id: '00011',
          balance: 4,
          opentime: 5421,
        },
        {
          id: '00021',
          balance: 514,
          opentime: 1521,
        },
      ],
    };
  },
  methods: {
    add(item: any) {
      this.items.push(item);
    },
    edit(item: any, index: number) {
      Object.assign(this.items[index], item);
    },
    remove(index: number) {
      this.items.splice(index, 1);
    },
  },
});
</script>
