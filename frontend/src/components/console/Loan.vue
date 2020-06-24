<template>
  <!-- eslint-disable max-len -->
  <v-data-table
    :headers="[...headers, actionsItem]"
    :items="formatItems(items, headers)"
    class="elevation-6 pa-3"
    :search="search"
    :custom-filter="customFilter"
    :loading="loading"
    no-data-text="无数据"
    no-results-text="无匹配数据"
    loading-text="加载中"
    item-key="id"
    :show-expand="true"
    :single-expand="true"
  >
    <template v-slot:top>
      <v-toolbar flat color="white">
        <h1 class="hidden-xs-only">贷款</h1>
        <v-spacer class="hidden-xs-only"></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="支持“|”和“&”的使用，但不能混用。如“北京 | 178”、“gmail.com & 159 & 安徽”。"
          single-line
          hide-details
        ></v-text-field>
        <v-btn color="primary" dark class="ml-5 mb-2" @click="addLoanDialog">添加</v-btn>
        <v-dialog v-model="dialog" max-width="800px">
          <v-card v-if="focusedIndex === -1">
            <v-card-title>
              <span class="headline">添加</span>
            </v-card-title>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col v-for="(header, i) in headers" :key="i" cols="12" sm="6" md="4">
                    <v-select
                      v-if="i === expandingIndex"
                      v-model="editedItem.clients"
                      :items="header.clients.choices"
                      :chips="true"
                      :multiple="true"
                      label="关联客户"
                    >
                      <template v-slot:selection="{ item, index }">
                        <v-chip v-if="index <= 1">
                          <span>{{ item }}</span>
                        </v-chip>
                        <span
                          v-if="index === 2"
                          class="grey--text caption"
                        >（+{{ editedItem.clients.length - 2 }}其他）</span>
                      </template>
                    </v-select>
                    <v-select
                      v-else-if="header.choices"
                      :items="header.choices"
                      v-model="editedItem[header.value]"
                      :label="header.text"
                      :disabled="header.disabled || false"
                    ></v-select>
                    <v-text-field
                      v-else
                      v-model="editedItem[header.value]"
                      :label="header.text"
                      :disabled="header.disabled || false"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close">取消</v-btn>
              <v-btn color="blue darken-1" text @click="save">保存</v-btn>
            </v-card-actions>
          </v-card>
          <v-card v-else>
            <v-card-title>
              <span class="headline">添加支付</span>
            </v-card-title>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col v-for="(header, i) in payments.headers" :key="i" cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="payments.editedItem[header.value]"
                      :label="header.text"
                      :disabled="header.disabled || false"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close">取消</v-btn>
              <v-btn color="blue darken-1" text @click="save">保存</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>

    <template v-slot:item.actions="{ item }">
      <v-icon small class="mr-2" @click="removeLoanDialog(item)">mdi-cash-plus</v-icon>
      <v-icon small @click="removeLoan(item)">mdi-delete</v-icon>
    </template>
    <template v-slot:expanded-item="{ headers, item }">
      <td :colspan="headers.length">
        <v-data-table
          class="my-6 mx-6 mx-md-12"
          :headers="headers[expandingIndex].payments.headers"
          :items="formatItems(item.payments, headers[expandingIndex].payments.headers)"
          :dense="true"
          hide-default-footer
          no-data-text="无数据"
        ></v-data-table>
        <v-divider></v-divider>
        <v-data-table
          class="my-6 mx-6 mx-md-12"
          :headers="headers[expandingIndex].clients.headers"
          :items="formatItems(item.clients, headers[expandingIndex].clients.headers)"
          :dense="true"
          hide-default-footer
          no-data-text="无数据"
        ></v-data-table>
      </td>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import Vue from 'vue';
import { mapGetters, mapMutations } from 'vuex';
import axios from 'axios';
import mixin from '@/mixin.ts';

/* eslint-disable @typescript-eslint/camelcase */

const API_URL = process.env.VUE_APP_API_URL;

export default Vue.extend({
  name: 'Client',
  metaInfo: {
    title: '贷款管理',
  },
  mixins: [mixin],
  data() {
    const tempDefault = {
      id: 0,
      money: 0,
      status: '未开始发放',
      bank_ref: '',
      clients: [],
      payments: [],
    };
    return {
      headers: [
        {
          text: '贷款号',
          value: 'id',
          disabled: true,
        },
        {
          text: '金额',
          value: 'money',
          type: 'money',
        },
        {
          text: '状态',
          value: 'status',
          disabled: true,
        },
        {
          text: '银行',
          value: 'bank_ref',
          choices: [],
        },
        {
          text: '更多信息',
          value: 'data-table-expand',
          payments: {
            headers: [
              {
                text: '支付号',
                value: 'id',
              },
              {
                text: '支付时间',
                value: 'pay_date',
                type: 'time',
              },
              {
                text: '金额',
                value: 'money',
                type: 'money',
              },
            ],
          },
          clients: {
            headers: [
              {
                text: '身份证号',
                value: 'id_number',
              },
              {
                text: '姓名',
                value: 'name',
              },
              {
                text: '手机号',
                value: 'phone_number',
              },
              {
                text: '负责人身份证号',
                value: 'staff_ref',
              },
            ],
            choices: [],
          },
        },
      ],
      items: [] as object[],
      search: '',
      loading: true,
      dialog: false,
      focusedIndex: -1,
      editedItem: { ...tempDefault },
      originalItem: null,
      defaultItem: { ...tempDefault },
      actionsItem: {
        text: '操作',
        value: 'actions',
        sortable: false,
      },
      payments: {
        headers: [
          {
            text: '支付时间',
            value: 'pay_date',
            type: 'time',
          },
          {
            text: '金额',
            value: 'money',
            type: 'money',
          },
        ],
        defaultItem: { pay_date: new Date().toLocaleString(), money: 0 },
        editedItem: { pay_date: new Date().toLocaleString(), money: 0 },
      },
    };
  },
  watch: {
    dialog(val) {
      // eslint-disable-next-line
      val || this.close();
    },
  },
  computed: {
    ...mapGetters(['getToken']),
    expandingIndex(): number {
      return this.headers.findIndex(
        (e: any) => e.value === 'data-table-expand',
      );
    },
  },
  methods: {
    ...mapMutations(['setError']),
    addLoanDialog() {
      this.focusedIndex = -1;
      this.dialog = true;
    },
    removeLoanDialog(item: any) {
      this.focusedIndex = this.items.indexOf(item);
      this.dialog = true;
    },
    removeLoan(item: any) {
      const index = this.items.indexOf(item);
      // eslint-disable-next-line no-restricted-globals, no-unused-expressions
      if (confirm('确定要删除此项吗？')) {
        axios
          .delete(`${API_URL}/loan/${item.id}`, {
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
      }
    },

    close() {
      this.dialog = false;
      this.editedItem = { ...this.defaultItem };
      this.payments.editedItem = { ...this.payments.defaultItem };
    },
    save() {
      if (this.focusedIndex === -1) {
        axios
          .post(`${API_URL}/loan/`, this.editedItem, {
            headers: { 'X-Token': this.getToken },
          })
          .then((response) => {
            // eslint-disable-next-line no-param-reassign
            this.items.push(response.data);
          })
          .catch((error) => {
            if (error.response && error.response.data.message) {
              this.setError(error.response.data.message);
            } else {
              this.setError(error.message);
            }
          });
      } else {
        const convertedItem = {
          ...this.payments.editedItem,
          pay_date: Math.floor(
            new Date(this.payments.editedItem.pay_date).getTime() / 1000,
          ),
        };
        if (Number.isNaN(convertedItem.pay_date)) {
          this.setError('不正确的时间格式');
          return;
        }
        axios
          .post(
            `${API_URL}/loan/${
              (this.items[this.focusedIndex] as any).id
            }/payment`,
            convertedItem,
            {
              headers: { 'X-Token': this.getToken },
            },
          )
          .then((response) => {
            Object.assign(this.items[this.focusedIndex], response.data);
          })
          .catch((error) => {
            if (error.response && error.response.data.message) {
              this.setError(error.response.data.message);
            } else {
              this.setError(error.message);
            }
          });
      }
      this.close();
    },
  },

  created() {
    axios
      .get(`${API_URL}/loan/`, {
        headers: { 'X-Token': this.getToken },
      })
      .then((response) => {
        this.items = response.data;
        this.loading = false;
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
        this.headers.find(
          (e) => e.value === 'bank_ref',
        )!.choices = response.data.map((bank: any) => bank.name);
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
        this.headers[this.expandingIndex].clients!.choices = response.data.map(
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
