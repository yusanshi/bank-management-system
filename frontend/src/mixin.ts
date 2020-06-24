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
        return this.recursivelyFilter(item, search);
      }
      if (andWords.length === 1 && orWords.length === 1) {
        return this.recursivelyFilter(
          item,
          andWords[0].length < orWords[0].length ? andWords[0] : orWords[0],
        );
      }
      if (andWords.length >= 2) {
        return andWords.every((e) => this.recursivelyFilter(item, e));
      }
      if (orWords.length >= 2) {
        return orWords.some((e) => this.recursivelyFilter(item, e));
      }
    },
    recursivelyFilter(obj: object, search: string, depth = 0) {
      if (depth > 1) {
        // maximum depth to search
        return false;
      }
      if (
        Object.values(obj)
          .filter((e) => typeof e === 'string')
          .some((e) => e.indexOf(search) !== -1)
      ) {
        return true;
      }
      if (
        Object.values(obj)
          .filter((e) => typeof e === 'number')
          .map((e) => e.toString())
          .some((e) => e.indexOf(search) !== -1)
      ) {
        return true;
      }
      if (
        Object.values(obj)
          .filter((e) => Array.isArray(e))
          .some((e) => e.some((ee: any) => this.recursivelyFilter(ee, search, depth + 1)))
      ) {
        return true;
      }
      if (
        Object.values(obj)
          .filter((e) => typeof e === 'object')
          .some((e) => this.recursivelyFilter(e, search, depth + 1))
      ) {
        return true;
      }
      return false;
    },
  },
});
