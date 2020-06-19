<template>
  <v-data-table
    :headers="[...meta.headers, actionsItem]"
    :items="items"
    class="elevation-6 pa-3"
    :search="search"
    no-data-text="无数据"
    no-results-text="无匹配数据"
  >
    <template v-slot:top>
      <v-toolbar flat color="white">
        <h1>{{ meta.title }}</h1>
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="在此输入关键词查询"
          single-line
          hide-details
        ></v-text-field>
        <v-dialog v-model="dialog" max-width="500px">
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
                  <!-- eslint-disable-next-line max-len-->
                  <v-col v-for="(header, i) in meta.headers" :key="i" cols="12" sm="6" md="4">
                    <!-- eslint-disable-next-line max-len-->
                    <v-text-field v-model="editedItem[header.value]" :label="header.text"></v-text-field>
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
  </v-data-table>
</template>

<script>
export default {
  name: 'Table',
  data() {
    return {
      search: '',
      dialog: false,
      editedIndex: -1,
      editedItem: { ...this.meta.default },
      defaultItem: { ...this.meta.default },
      actionsItem: {
        text: '操作',
        value: 'actions',
        sortable: false,
      },
    };
  },
  props: ['meta', 'items'],
  watch: {
    dialog(val) {
      // eslint-disable-next-line no-unused-expressions
      val || this.close();
    },
  },
  methods: {
    editItem(item) {
      this.editedIndex = this.items.indexOf(item);
      this.editedItem = { ...item };
      this.dialog = true;
    },

    removeItem(item) {
      const index = this.items.indexOf(item);
      // eslint-disable-next-line
      confirm("确定要删除此项吗？") && this.$emit('remove', index);
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
        this.$emit('edit', this.editedItem, this.editedIndex);
      } else {
        this.$emit('add', this.editedItem);
      }
      this.close();
    },
  },
};
</script>
