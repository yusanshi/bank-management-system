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
          <mini-statistic icon="mdi-account-cash" :title="beautifyMoneyDisplay(totalLoanMoney)" sub-title="总贷款金额" color="purple" />
        </v-flex>

        <!-- mini statistic  end -->
        <v-flex lg8 sm12 xs12>
          <v-widget title="条形图" content-bg="white">
            <v-btn icon slot="widget-header-action">
              <v-icon class="text--secondary">mdi-refresh</v-icon>
            </v-btn>
            <div slot="widget-content">
              <e-chart
                :path-option="[
                  ['dataset.source', siteTrafficData],
                  ['color', [color.lightBlue.base, color.green.lighten1]],
                  ['legend.show', true],
                  ['xAxis.axisLabel.show', true],
                  ['yAxis.axisLabel.show', true],
                  ['grid.left', '2%'],
                  ['grid.bottom', '5%'],
                  ['grid.right', '3%'],
                  ['series[0].type', 'bar'],
                  ['series[0].areaStyle', {}],
                  ['series[0].smooth', true],
                  ['series[1].smooth', true],
                  ['series[1].type', 'bar'],
                  ['series[1].areaStyle', {}]
                ]"
                height="400px"
                width="100%"
              />
            </div>
          </v-widget>
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
        <v-flex lg4 sm12 xs12>
          <box-chart
            card-color="indigo"
            title="Trending"
            sub-title="10%"
            icon="mdi-trending-up"
            :data="siteTrafficData"
            :chart-color="[color.indigo.lighten1]"
            type="line"
          />
          <box-chart
            class="mt-4"
            card-color="pink"
            title="Page views"
            sub-title="10%"
            icon="mdi-trending-up"
            :data="siteTrafficData"
            :chart-color="[color.pink.darken1, 'rgba(255,255,255,0.3)']"
            gradient
            type="area"
          />
        </v-flex>
        <v-flex lg4 sm12 xs12>
          <box-chart
            card-color="indigo"
            title="Trending"
            sub-title="10%"
            icon="mdi-trending-up"
            :data="siteTrafficData"
            :chart-color="[color.indigo.lighten1]"
            type="line"
          />
          <box-chart
            class="mt-4"
            card-color="pink"
            title="Page views"
            sub-title="10%"
            icon="mdi-trending-up"
            :data="siteTrafficData"
            :chart-color="[color.pink.darken1, 'rgba(255,255,255,0.3)']"
            gradient
            type="area"
          />
        </v-flex>
        <!-- statistic section -->
        <v-flex lg4 sm12 xs12>
          <linear-statistic
            title="Sales"
            sub-title="Sales increase"
            icon="mdi-trending-up"
            color="success"
            :value="15"
          />
          <linear-statistic
            class="my-4"
            title="Orders"
            sub-title="Increase"
            icon="mdi-trending-up"
            color="pink"
            :value="30"
          />
          <linear-statistic
            class="my-4"
            title="Revenue"
            sub-title="Revenue increase"
            icon="mdi-trending-up"
            color="primary"
            :value="50"
          />
          <linear-statistic
            class="mt-4"
            title="Cost"
            sub-title="Cost reduce"
            icon="mdi-trending-down"
            color="orange"
            :value="25"
          />
        </v-flex>
        <!-- Circle statistic -->
        <v-flex lg4 sm12 xs12 v-for="(item, index) in trending" :key="'c-trending' + index">
          <circle-statistic
            :title="item.subheading"
            :sub-title="item.headline"
            :caption="item.caption"
            :icon="item.icon.label"
            :color="item.linear.color"
            :value="item.linear.value"
          />
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
import BoxChart from '@/components/widgets/chart/BoxChart.vue';
import CircleStatistic from '@/components/widgets/statistic/CircleStatistic.vue';
import LinearStatistic from '@/components/widgets/statistic/LinearStatistic.vue';

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
    BoxChart,
    CircleStatistic,
    LinearStatistic,
  },
  data() {
    return {
      color: Material,
      trending: [
        {
          subheading: 'Email',
          headline: '15+',
          caption: 'email opens',
          percent: 15,
          icon: {
            label: 'mdi-email',
            color: 'info',
          },
          linear: {
            value: 15,
            color: 'info',
          },
        },
        {
          subheading: 'Tasks',
          headline: '90%',
          caption: 'tasks completed.',
          percent: 90,
          icon: {
            label: 'mdi-list',
            color: 'primary',
          },
          linear: {
            value: 90,
            color: 'success',
          },
        },
        {
          subheading: 'Issues',
          headline: '100%',
          caption: 'issues fixed.',
          percent: 100,
          icon: {
            label: 'mdi-duck',
            color: 'primary',
          },
          linear: {
            value: 100,
            color: 'error',
          },
        },
      ],
      siteTrafficData: [
        { month: 'Jan', 业务金额: 741, 用户数: 463 },
        { month: 'Feb', 业务金额: 1118, 用户数: 323 },
        { month: 'Mar', 业务金额: 540, 用户数: 603 },
        { month: 'Apr', 业务金额: 506, 用户数: 770 },
        { month: 'May', 业务金额: 691, 用户数: 958 },
        { month: 'Jun', 业务金额: 1101, 用户数: 639 },
        { month: 'Jul', 业务金额: 821, 用户数: 351 },
        { month: 'Aug', 业务金额: 322, 用户数: 845 },
        { month: 'Sep', 业务金额: 632, 用户数: 675 },
        { month: 'Oct', 业务金额: 954, 用户数: 701 },
        { month: 'Nov', 业务金额: 428, 用户数: 969 },
        { month: 'Dec', 业务金额: 926, 用户数: 488 },
      ],
      data: {
        banks: [],
        clients: [],
        accounts: [],
        loans: [],
      },
    };
  },
  computed: {
    ...mapGetters(['getToken']),
    totalDepositBalance(): number {
      return this.data.accounts.filter((e: any) => e.account_type === 'deposit').map((e: any) => e.balance).reduce((a, b) => a + b, 0);
    },
    totalLoanMoney(): number {
      return this.data.loans.map((e: any) => e.money).reduce((a, b) => a + b, 0);
    },
    loanStatus(): object {
      return ['未开始发放', '发放中', '已全部发放'].map((x) => ({
        value: this.data.loans.filter((e: any) => e.status === x).length,
        name: x,
      }));
      // TODO update
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
