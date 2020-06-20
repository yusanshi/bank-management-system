import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import Login from '@/views/Login.vue';
import Console from '@/views/Console.vue';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    component: Login,
  },
  {
    path: '/console',
    component: Console,
    children: [
      {
        path: '',
        component: () => import('@/components/console/Dashboard.vue'),
      },
      {
        path: 'client',
        component: () => import('@/components/console/Client.vue'),
      },
      {
        path: 'account/deposit',
        component: () => import('@/components/console/AccountDeposit.vue'),
      },
      {
        path: 'account/cheque',
        component: () => import('@/components/console/AccountCheque.vue'),
      },
      {
        path: 'loan',
        component: () => import('@/components/console/Loan.vue'),
      },
      {
        path: 'password',
        component: () => import('@/components/console/Password.vue'),
      },
    ],
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
