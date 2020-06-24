 <template>
  <v-data-table
    :headers="[...meta.headers, actionsItem]"
    :items="formatItems(items, meta.headers)"
    class="elevation-6 pa-3"
    :search="search"
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
        <h1 class="hidden-xs-only">{{ meta.title }}</h1>
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
                  <v-col v-for="(header, i) in meta.headers" :key="i" cols="12" sm="6" md="4">
                    <v-select
                      v-if="i === expandingIndex"
                      v-model="editedItem.clients_ref"
                      :items="header.choices"
                      :chips="true"
                      :multiple="true"
                      :label="header.text"
                    >
                      <template v-slot:selection="{ item, index }">
                        <v-chip v-if="index <= 1">
                          <span>{{ item }}</span>
                        </v-chip>
                        <!-- eslint-disable max-len -->
                        <span
                          v-if="index === 2"
                          class="grey--text caption"
                        >（+{{ editedItem.clients_ref.length - 2 }}其他）</span>
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
          class="my-6 mx-16"
          :headers="headers[expandingIndex].headers"
          :items="formatItems(item.client_account_associations, headers[expandingIndex].headers)"
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
import mixin from '@/mixin.ts';
import { mapMutations } from 'vuex';

/* eslint-disable @typescript-eslint/camelcase */

// TODO disable empty input
export default Vue.extend({
  name: 'AccountTable',
  mixins: [mixin],
  data() {
    return {
      search: '',
      dialog: false,
      editedIndex: -1,
      editedItem: this.meta.default,
      originalItem: null,
      defaultItem: this.meta.default,
      actionsItem: {
        text: '操作',
        value: 'actions',
        sortable: false,
      },
    };
  },
  props: ['meta', 'items', 'loading'],
  watch: {
    dialog(val) {
      // eslint-disable-next-line no-unused-expressions
      val || this.close();
    },
  },
  computed: {
    expandingIndex(): number {
      return this.meta.headers.findIndex(
        (e: any) => e.value === 'data-table-expand',
      );
    },
  },
  methods: {
    ...mapMutations(['setError']),
    editItem(item: any) {
      this.editedIndex = this.items.indexOf(item);
      this.editedItem = { ...item };
      (this
        .editedItem as any).clients_ref = item.client_account_associations.map(
        (x: any) => x.client_ref,
      );
      this.originalItem = { ...item };
      this.dialog = true;
    },

    removeItem(item: any) {
      const index = this.items.indexOf(item);
      // eslint-disable-next-line no-restricted-globals, no-unused-expressions
      confirm('确定要删除此项吗？') && this.$emit('remove', item, index);
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = { ...this.defaultItem };
        this.editedIndex = -1;
      });
    },

    save() {
      const convertedItem = {
        ...this.editedItem,
        open_date: Math.floor(
          new Date(this.editedItem.open_date).getTime() / 1000,
        ),
      };
      if (Number.isNaN(convertedItem.open_date)) {
        this.setError('不正确的时间格式');
        return;
      }
      if (this.editedIndex > -1) {
        this.$emit('edit', convertedItem, this.originalItem, this.editedIndex);
      } else {
        this.$emit('add', convertedItem);
      }
      this.close();
    },
  },
});
</script>
