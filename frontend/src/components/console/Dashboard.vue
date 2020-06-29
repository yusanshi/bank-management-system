<template>
  <!-- eslint-disable max-len -->
  <div class="page--dash">
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
        <v-flex lg3 sm6 xs12>
          <mini-statistic
            icon="mdi-account-box-multiple"
            :title="data.clients.length.toString()"
            sub-title="客户数"
            color="indigo"
          />
        </v-flex>
        <v-flex lg3 sm6 xs12>
          <mini-statistic
            icon="mdi-folder-account"
            :title="data.accounts.length.toString()"
            sub-title="账户数"
            color="red"
          />
        </v-flex>
        <v-flex lg3 sm6 xs12>
          <mini-statistic
            icon="mdi-cash-multiple"
            :title="beautifyMoneyDisplay(totalDepositBalance)"
            sub-title="总存款金额"
            color="light-blue"
          />
        </v-flex>
        <v-flex lg3 sm6 xs12>
          <mini-statistic
            icon="mdi-account-cash"
            :title="beautifyMoneyDisplay(totalLoanMoney)"
            sub-title="总贷款金额"
            color="purple"
          />
        </v-flex>

        <v-flex lg8 sm12 xs12>
          <v-card>
            <v-toolbar color="transparent" text dense elevation="0">
              <v-toolbar-title>
                <h4>支行统计</h4>
              </v-toolbar-title>
            </v-toolbar>
            <v-divider></v-divider>
            <v-row class="ma-2">
              <v-col>
                <v-select :items="select.bank.items" v-model="select.bank.value" label="银行"></v-select>
              </v-col>
              <v-col>
                <v-select :items="select.time.items" v-model="select.time.value" label="时间周期"></v-select>
              </v-col>
              <v-col>
                <v-text-field v-model="select.timeLength" label="长度" type="number"></v-text-field>
              </v-col>
            </v-row>
            <v-divider></v-divider>
            <e-chart class="mt-5"
              :path-option="[
                  ['dataset.source', bankStaticsData],
                  ['color', [color.lightBlue.base, color.green.lighten1, color.indigo.base]],
                  ['legend.show', true],
                  ['xAxis.axisLabel.show', true],
                  ['yAxis.axisLabel.show', true],
                  ['grid.left', '2%'],
                  ['grid.bottom', '5%'],
                  ['grid.right', '2%'],
                  ['series[0].type', 'line'],
                  ['series[0].smooth', true],
                  ['series[0].lineStyle', {'width': '3'}],
                  ['series[1].type', 'line'],
                  ['series[1].smooth', true],
                  ['series[1].lineStyle', {'width': '3'}],
                  ['series[2].type', 'line'],
                  ['series[2].smooth', true],
                  ['series[2].lineStyle', {'width': '3'}],
                ]"
              height="400px"
              width="100%"
            />
            <v-divider></v-divider>
            <e-chart class="mt-5"
              :path-option="[
                  ['dataset.source', bankStaticsDataReordered],
                  ['color', [color.pink.base]],
                  ['legend.show', true],
                  ['xAxis.axisLabel.show', true],
                  ['yAxis.axisLabel.show', true],
                  ['grid.left', '2%'],
                  ['grid.bottom', '5%'],
                  ['grid.right', '2%'],
                  ['series[0].type', 'line'],
                  ['series[0].smooth', true],
                  ['series[0].lineStyle', {'width': '3'}]
                ]"
              height="400px"
              width="100%"
            />
            <v-divider></v-divider>
           <v-data-table class="mt-5"
          :headers="headers"
          :items="bankStaticsData"
          hide-default-footer
        ></v-data-table>
          </v-card>
        </v-flex>
        <v-flex lg4 sm12 xs12>
          <v-widget title="贷款状态" content-bg="white">
            <div slot="widget-content">
              <e-chart
                :path-option="[
                  ['dataset.source', loanStatus],
                  ['legend.bottom', '0'],
                  [
                    'color',
                    [
                      color.lightBlue.base,
                      color.indigo.base,
                      color.pink.base,
                      color.green.base,
                      color.cyan.base,
                      color.teal.base
                    ]
                  ],
                  ['xAxis.show', false],
                  ['yAxis.show', false],
                  ['series[0].type', 'pie'],
                  ['series[0].avoidLabelOverlap', true],
                  ['series[0].radius', ['50%', '70%']]
                ]"
                height="400px"
                width="100%"
              />
            </div>
          </v-widget>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { mapGetters, mapMutations } from 'vuex';
import axios from 'axios';
import EChart from '@/components/chart/echart';
import MiniStatistic from '@/components/widgets/statistic/MiniStatistic.vue';
import VWidget from '@/components/VWidget.vue';
import Material from 'vuetify/es5/util/colors';

/* eslint-disable @typescript-eslint/camelcase */

const API_URL = process.env.VUE_APP_API_URL;
export default Vue.extend({
  name: 'Dashboard',
  metaInfo: {
    title: '仪表盘',
  },
  components: {
    VWidget,
    MiniStatistic,
    EChart,
  },
  data() {
    return {
      color: Material,
      select: {
        bank: { items: [] as string[], value: '' },
        time: { items: ['年', '季', '月'], value: '年' },
        timeLength: 5,
      },
      data: {
        banks: [],
        clients: [],
        accounts: [],
        loans: [],
      },
      headers: ['时间', '储蓄额', '支票额', '贷款额', '开户数'].map((e) => ({
        text: e,
        value: e,
      })),
    };
  },
  computed: {
    ...mapGetters(['getToken']),
    totalDepositBalance(): number {
      return this.data.accounts
        .filter((e: any) => e.account_type === 'deposit')
        .map((e: any) => e.balance)
        .reduce((a, b) => a + b, 0);
    },
    totalLoanMoney(): number {
      return this.data.loans
        .map((e: any) => e.money)
        .reduce((a, b) => a + b, 0);
    },
    loanStatus(): object {
      return ['未开始发放', '发放中', '已全部发放'].map((x) => ({
        value: this.data.loans.filter((e: any) => e.status === x).length,
        name: x,
      }));
    },
    bankStaticsData(): object {
      const allAccounts = this.data.accounts.filter(
        (e: any) => e.bank_ref === this.select.bank.value,
      );
      const allDepositAccounts = allAccounts
        .filter((e: any) => e.account_type === 'deposit')
        .map((e: any) => ({
          money: e.balance,
          date: e.open_date,
        }));
      const allChequeAccounts = allAccounts
        .filter((e: any) => e.account_type === 'cheque')
        .map((e: any) => ({
          money: e.balance,
          date: e.open_date,
        }));
      const allPayments = this.data.loans
        .filter((e: any) => e.bank_ref === this.select.bank.value)
        .flatMap((e: any) => e.payments)
        .map((e: any) => ({
          money: e.money,
          date: e.pay_date,
        }));
      const utc2String = (utc: any, unit: any) => {
        const year = new Date(utc * 1000).getUTCFullYear();
        const month = new Date(utc * 1000).getUTCMonth();
        if (unit === '年') {
          return `${year}`;
        }
        if (unit === '季') {
          return `${year}Q${Math.floor(month / 3) + 1}`;
        }
        if (unit === '月') {
          return `${year}.${month}`;
        }
        return 'Unknown';
      };
      let timestamp = Math.floor(Date.now() / 1000);
      let result = [] as any;
      while (timestamp > 0) {
        result.push(utc2String(timestamp, this.select.time.value));
        timestamp -= 3600 * 24 * 15;
      }
      result = result
        .filter((i: any, idx: number) => result[idx - 1] !== i)
        .reverse()
        .map((e: any) => ({
          时间: e,
          储蓄额: 0,
          支票额: 0,
          贷款额: 0,
          开户数: 0,
        }));
      [
        [allDepositAccounts, '储蓄额'],
        [allChequeAccounts, '支票额'],
        [allPayments, '贷款额'],
      ].forEach((e: any) => {
        e[0].forEach((e2: any) => {
          const found = result.find(
            (e3: any) => e3.时间 === utc2String(e2.date, this.select.time.value),
          );
          found[e[1]] += e2.money;
        });
      });
      allAccounts.forEach((e: any) => {
        const found = result.find(
          (e2: any) => e2.时间 === utc2String(e.open_date, this.select.time.value),
        );
        found.开户数 += 1;
      });
      return result.slice(-this.select.timeLength).map((e: any) => ({
        时间: e.时间,
        储蓄额: Number(e.储蓄额.toFixed(2)),
        支票额: Number(e.支票额.toFixed(2)),
        贷款额: Number(e.贷款额.toFixed(2)),
        开户数: e.开户数,
      }));
    },
    bankStaticsDataReordered(): object {
      return (this.bankStaticsData as any).map((e: any) => ({
        时间: e.时间,
        开户数: e.开户数,
      }));
    },
  },
  methods: {
    ...mapMutations(['setError']),
    beautifyMoneyDisplay(money: number): string {
      let unit = '元';
      while (money > 1e4) {
        // eslint-disable-next-line no-param-reassign
        money /= 1e4;
        if (unit[0] === '万') {
          unit = `亿${unit.substring(1)}`;
        } else {
          unit = `万${unit}`;
        }
      }
      return money.toFixed(2) + unit;
    },
  },
  created() {
    axios
      .get(`${API_URL}/bank/`, {
        headers: { 'X-Token': this.getToken },
      })
      .then((response) => {
        this.data.banks = response.data;
        this.select.bank.items = this.data.banks.map((e: any) => e.name);
        [this.select.bank.value] = this.select.bank.items;
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
        this.data.clients = response.data;
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
        this.data.accounts = response.data;
      })
      .catch((error) => {
        if (error.response && error.response.data.message) {
          this.setError(error.response.data.message);
        } else {
          this.setError(error.message);
        }
      });

    axios
      .get(`${API_URL}/loan/`, {
        headers: { 'X-Token': this.getToken },
      })
      .then((response) => {
        this.data.loans = response.data;
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
