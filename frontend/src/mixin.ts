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
    customFilter(_: any, search: string, item: any) {
      const keywords = '()&|';
      let elements: string[] = [];
      let element: string[] = [];
      [...search].forEach((c) => {
        if (keywords.includes(c)) {
          elements.push(element.join(''));
          elements.push(c);
          element = [];
        } else {
          element.push(c);
        }
      });
      elements.push(element.join(''));
      elements = elements.map((e) => e.trim()).filter((e) => e !== '');
      const searchInObject = (obj: object, text: string) => JSON.stringify(obj).replace(/"[A-Za-z0-9_]+":/g, ' ').indexOf(text) !== -1;
      // eslint-disable-next-line no-nested-ternary
      elements = elements.map((e) => (keywords.includes(e) ? e : (searchInObject(item, e) ? 'true' : 'false'))).map((e) => {
        if (e === '&') {
          return '&&';
        } if (e === '|') {
          return '||';
        }
        return e;
      });
      while (elements.length !== 0) {
        try {
          // eslint-disable-next-line no-eval
          return eval(elements.join(''));
        } catch (e) {
          elements.pop();
        }
      }
      return true;
    },
  },
});
