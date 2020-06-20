import Vue from 'vue';

export default Vue.extend({
  methods: {
    formatItems(items: any, headers: any) {
      headers.forEach((header: any) => {
        if (header.type === 'money') {
          items.forEach((item: any) => {
            if (typeof item[header.value] === 'number') {
              // eslint-disable-next-line no-param-reassign
              item[header.value] = item[header.value].toFixed(2);
            }
          });
        } else if (header.type === 'rate') {
          items.forEach((item: any) => {
            if (typeof item[header.value] === 'number') {
              // eslint-disable-next-line no-param-reassign
              item[header.value] = item[header.value].toFixed(4);
            }
          });
        } else if (header.type === 'time') {
          items.forEach((item: any) => {
            if (typeof item[header.value] === 'number') {
              // eslint-disable-next-line no-param-reassign
              item[header.value] = new Date(item[header.value] * 1000).toLocaleString();
            }
          });
        }
      });
      return items;
    },
  },
});
