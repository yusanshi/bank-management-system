<template>
   <AccountTable
      :meta="meta"
      :items="items"
      @add="add"
      @edit="edit"
      @remove="remove"
    />
</template>

<script lang="ts">
import Vue from 'vue';
import { mapGetters, mapMutations } from 'vuex';
import AccountTable from '@/components/console/AccountTable.vue';
import axios from 'axios';

/* eslint-disable @typescript-eslint/camelcase */

const API_URL = process.env.VUE_APP_API_URL;

export default Vue.extend({
  name: 'AccountCheque',
  metaInfo: {
    title: '支票账户管理',
  },
  components: {
    AccountTable,
  },
  data() {
    return {
      meta: {
        title: '支票账户',
        default: {
          id: '',
          balance: 0,
          open_date: new Date().toLocaleString(),
          bank_ref: '',
          overdraft: 0,
          account_type: 'cheque',
          clients_ref: [],
        },
        headers: [
          {
            text: '账户号',
            value: 'id',
            disabled: true,
          },
          {
            text: '余额',
            value: 'balance',
            type: 'money',
          },
          {
            text: '开户时间',
            value: 'open_date',
            type: 'time',
          },
          {
            text: '开户行',
            value: 'bank_ref',
            choices: [],
          },
          {
            text: '透支额',
            value: 'overdraft',
            type: 'money',
          },
          {
            text: '关联客户',
            value: 'data-table-expand',
            headers: [
              {
                text: '客户身份证号',
                value: 'client_ref',
              }, {
                text: '最近访问时间',
                value: 'last_visit_date',
                type: 'time',
              },
            ],
            choices: [],
          },
        ],
      },
      items: [] as object[],
    };
  },
  computed: {
    ...mapGetters(['getToken']),
    expandingIndex(): number {
      return this.meta.headers.findIndex((e: any) => e.value === 'data-table-expand');
    },
  },
  methods: {
    ...mapMutations(['setError']),
    add(item: any) {
      // eslint-disable-next-line
      item.client_account_associations = item.clients_ref.map(
        (x: string) => ({
          client_ref: x,
          account_ref: item.id,
          last_visit_date: 0,
        }),
      );
      // eslint-disable-next-line no-param-reassign
      delete item.clients_ref;
      axios
        .post(`${API_URL}/account/`, item, {
          headers: { 'X-Token': this.getToken },
        })
        .then(() => {
          this.items.push(item);
        })
        .catch((error) => {
          if (error.response && error.response.data.message) {
            this.setError(error.response.data.message);
          } else {
            this.setError(error.message);
          }
        });
    },
    edit(newItem: any, oldItem: any, index: number) {
      const old_array = newItem.client_account_associations.map(
        (e: any) => e.client_ref,
      );
      const new_array = newItem.clients_ref;
      const add_array = new_array.filter((e: any) => !old_array.includes(e));
      const delete_array = old_array.filter((e: any) => !new_array.includes(e));
      // eslint-disable-next-line no-param-reassign
      newItem.client_account_associations = [
        ...newItem.client_account_associations.filter(
          (e: any) => !delete_array.includes(e.client_ref),
        ),
        ...add_array.map((e: string) => ({
          client_ref: e,
          account_ref: newItem.id,
          last_visit_date: 0,
        })),
      ];
      // eslint-disable-next-line no-param-reassign
      delete newItem.clients_ref;
      axios
        .put(`${API_URL}/account/${oldItem.id}`, newItem, {
          headers: { 'X-Token': this.getToken },
        })
        .then(() => {
          Object.assign(this.items[index], newItem);
        })
        .catch((error) => {
          if (error.response && error.response.data.message) {
            this.setError(error.response.data.message);
          } else {
            this.setError(error.message);
          }
        });
    },
    remove(item: any, index: number) {
      axios
        .delete(`${API_URL}/account/${item.id}`, {
          headers: { 'X-Token': this.getToken },
        })
        .then(() => {
          this.items.splice(index, 1);
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
  created() {
    axios
      .get(`${API_URL}/account/`, {
        headers: { 'X-Token': this.getToken },
      })
      .then((response) => {
        this.items = response.data.filter((account: any) => account.account_type === 'cheque');
      })
      .catch((error) => {
        if (error.response && error.response.data.message) {
          this.setError(error.response.data.message);
        } else {
          this.setError(error.message);
        }
      });

    axios
      .get(`${API_URL}/bank/`, {
        headers: { 'X-Token': this.getToken },
      })
      .then((response) => {
        this.meta.headers.find((e) => e.value === 'bank_ref')!.choices = response.data.map((bank: any) => bank.name);
      })
      .catch((error) => {
        if (error.response && error.response.data.message) {
          this.setError(error.response.data.message);
        } else {
          this.setError(error.message);
        }
      });

    axios
      .get(`${API_URL}/client/`, {
        headers: { 'X-Token': this.getToken },
      })
      .then((response) => {
        this.meta.headers[this.expandingIndex].choices = response.data.map(
          (client: any) => client.id_number,
        );
      })
      .catch((error) => {
        if (error.response && error.response.data.message) {
          this.setError(error.response.data.message);
        } else {
          this.setError(error.message);
        }
      });
  },
});

</script>
