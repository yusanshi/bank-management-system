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
    // eslint-disable-next-line consistent-return
    customFilter(value: any, search: string, item: any) {
      const andWords = search
        .split('&')
        .map((e) => e.trim())
        .filter((e) => e !== '');
      const orWords = search
        .split('|')
        .map((e) => e.trim())
        .filter((e) => e !== '');
      if (andWords.length === 0 || orWords.length === 0) {
        return this.myFilter(item, search);
      }
      if (andWords.length === 1 && orWords.length === 1) {
        return this.myFilter(
          item,
          andWords[0].length < orWords[0].length ? andWords[0] : orWords[0],
        );
      }
      if (andWords.length >= 2) {
        return andWords.every((e) => this.myFilter(item, e));
      }
      if (orWords.length >= 2) {
        return orWords.some((e) => this.myFilter(item, e));
      }
    },
    myFilter(obj: object, search: string) {
      return JSON.stringify(obj).replace(/"[A-Za-z0-9_]+":/g, ' ').indexOf(search) !== -1;
    },
  },
});
