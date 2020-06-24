<template>
  <!-- eslint-disable max-len -->
  <v-data-table
    :headers="[...headers, actionsItem]"
    :items="formatItems(items, headers)"
    class="elevation-6 pa-3"
    :search="search"
    :loading="loading"
    no-data-text="无数据"
    no-results-text="无匹配数据"
    loading-text="加载中"
    item-key="id_number"
    :show-expand="true"
    :single-expand="true"
  >
    <template v-slot:top>
      <v-toolbar flat color="white">
        <h1 class="hidden-xs-only">客户</h1>
        <v-spacer class="hidden-xs-only"></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="在此输入关键词查询"
          single-line
          hide-details
        ></v-text-field>
        <v-dialog v-model="dialog" max-width="800px">
          <template v-slot:activator="{ on }">
            <v-btn color="primary" dark class="ml-5 mb-2" v-on="on">添加</v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">{{ editedIndex === -1 ? "添加" : "编辑" }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col v-for="(header, i) in headers" :key="i" cols="12" sm="6" md="4">
                    <v-select
                      v-if="i === expandingIndex"
                      v-model="editedItem.accounts_ref"
                      :items="header.choices"
                      :chips="true"
                      :multiple="true"
                      label="关联账户"
                    >
                      <template v-slot:selection="{ item, index }">
                        <v-chip v-if="index <= 1">
                          <span>{{ item }}</span>
                        </v-chip>
                        <span
                          v-if="index === 2"
                          class="grey--text caption"
                        >（+{{ editedItem.accounts_ref.length - 2 }}其他）</span>
                      </template>
                    </v-select>
                    <v-select
                      v-else-if="header.choices"
                      :items="header.choices"
                      v-model="editedItem[header.value]"
                      :label="header.text"
                      :disabled="editedIndex !== -1 && (header.disabled || false)"
                    ></v-select>
                    <v-text-field
                      v-else
                      v-model="editedItem[header.value]"
                      :label="header.text"
                      :disabled="editedIndex !== -1 && (header.disabled || false)"
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
      <v-icon small class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
      <v-icon small @click="removeItem(item)">mdi-delete</v-icon>
    </template>
    <template v-slot:expanded-item="{ headers, item }">
      <td :colspan="headers.length">
        <v-data-table
          class="my-6 mx-6 mx-md-12"
          :headers="headers[expandingIndex].headers"
          :items="formatItems(item.client_account_associations,headers[expandingIndex].headers)"
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
    title: '客户管理',
  },
  mixins: [mixin],
  data() {
    const tempDefault = {
      id_number: '',
      name: '',
      phone_number: '',
      address: '',
      contact_name: '',
      contact_phone_number: '',
      contact_email: '',
      contact_relationship: '',
      staff_ref: '',
      accounts_ref: [],
    };
    return {
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
          text: '地址',
          value: 'address',
        },
        {
          text: '联系人姓名',
          value: 'contact_name',
        },
        {
          text: '联系人手机号',
          value: 'contact_phone_number',
        },
        {
          text: '联系人邮箱',
          value: 'contact_email',
        },
        {
          text: '与联系人关系',
          value: 'contact_relationship',
          choices: ['父子', '母子', '兄弟'],
        },
        {
          text: '负责人身份证号',
          value: 'staff_ref',
          choices: [],
        },
        {
          text: '关联账户',
          value: 'data-table-expand',
          headers: [
            {
              text: '账户号',
              value: 'account_ref',
            },
            {
              text: '最近访问时间',
              value: 'last_visit_date',
              type: 'time',
            },
          ],
          choices: [],
        },
      ],
      items: [] as object[],
      search: '',
      loading: true,
      dialog: false,
      editedIndex: -1,
      editedItem: { ...tempDefault },
      originalItem: null,
      defaultItem: { ...tempDefault },
      actionsItem: {
        text: '操作',
        value: 'actions',
        sortable: false,
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
    add(item: any) {
      // eslint-disable-next-line
      item.client_account_associations = item.accounts_ref.map((x: string) => ({
        client_ref: item.id_number,
        account_ref: x,
        last_visit_date: 0,
      }));
      // eslint-disable-next-line no-param-reassign
      delete item.accounts_ref;
      axios
        .post(`${API_URL}/client/`, item, {
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
      newItem.client_account_associations.forEach((e: any) => {
        e.client_ref = newItem.id_number;
      });
      const old_array = newItem.client_account_associations.map(
        (e: any) => e.account_ref,
      );
      const new_array = newItem.accounts_ref;
      const add_array = new_array.filter((e: any) => !old_array.includes(e));
      const delete_array = old_array.filter((e: any) => !new_array.includes(e));
      // eslint-disable-next-line no-param-reassign
      newItem.client_account_associations = [
        ...newItem.client_account_associations.filter(
          (e: any) => !delete_array.includes(e.account_ref),
        ),
        ...add_array.map((e: string) => ({
          client_ref: newItem.id_number,
          account_ref: e,
          last_visit_date: 0,
        })),
      ];
      // eslint-disable-next-line no-param-reassign
      delete newItem.accounts_ref;
      axios
        .put(`${API_URL}/client/${oldItem.id_number}`, newItem, {
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
        .delete(`${API_URL}/client/${item.id_number}`, {
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

    editItem(item: any) {
      this.editedIndex = this.items.indexOf(item);
      this.editedItem = { ...item };
      (this
        .editedItem as any).accounts_ref = item.client_account_associations.map(
        (x: any) => x.account_ref,
      );
      this.originalItem = { ...item };
      this.dialog = true;
    },

    removeItem(item: any) {
      const index = this.items.indexOf(item);
      // eslint-disable-next-line no-restricted-globals, no-unused-expressions
      confirm('确定要删除此项吗？') && this.remove(item, index);
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = { ...this.defaultItem };
        this.editedIndex = -1;
      });
    },

    save() {
      if (this.editedIndex > -1) {
        this.edit(this.editedItem, this.originalItem, this.editedIndex);
      } else {
        this.add(this.editedItem);
      }
      this.close();
    },
  },

  created() {
    axios
      .get(`${API_URL}/client/`, {
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
      .get(`${API_URL}/account/`, {
        headers: { 'X-Token': this.getToken },
      })
      .then((response) => {
        this.headers[this.expandingIndex].choices = response.data.map(
          (account: any) => account.id,
        );
      })
      .catch((error) => {
        if (error.response && error.response.data.message) {
          this.setError(error.response.data.message);
        } else {
          this.setError(error.message);
        }
      });

    axios
      .get(`${API_URL}/staff/`, {
        headers: { 'X-Token': this.getToken },
      })
      .then((response) => {
        this.headers.find(
          (e) => e.value === 'staff_ref',
        )!.choices = response.data.map((staff: any) => staff.id_number);
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
