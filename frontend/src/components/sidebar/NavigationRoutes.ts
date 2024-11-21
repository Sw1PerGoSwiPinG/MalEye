export interface INavigationRoute {
  name: string
  displayName: string
  meta: { icon: string }
  children?: INavigationRoute[]
}

export default {
  root: {
    name: '/',
    displayName: 'navigationRoutes.home',
  },
  routes: [
    {
      name: 'index',
      displayName: 'menu.index',
      meta: {
        iconName: 'home',
      },
    },
    {
      name: 'dataset',
      displayName: 'menu.dataset',
      meta: {
        iconName: 'storage',
      },
    },
    {
      name: 'mfr',
      displayName: 'menu.mfr',
      meta: {
        iconName: 'apps',
      },
    },
    {
      name: 'pre-train',
      displayName: 'menu.pre-train',
      meta: {
        iconName: 'model_training',
      },
    },
    {
      name: 'fine-tune',
      displayName: 'menu.fine-tune',
      meta: {
        iconName: 'tune',
      },
    },
    {
      name: 'detection',
      displayName: 'menu.trafficDetection',
      meta: {
        iconName: 'troubleshoot',
      },
    },
    {
      name: 'real-time',
      displayName: 'menu.realtimeDetection',
      meta: {
        iconName: 'wifi_find',
      },
    },
    // {
    //   name: 'dashboard',
    //   displayName: 'menu.dashboard',
    //   meta: {
    //     // icon: 'vuestic-iconset-dashboard',
    //   },
    // },
    // {
    //   name: 'users',
    //   displayName: 'menu.users',
    //   meta: {
    //     // icon: 'group',
    //   },
    // },
    // {
    //   name: 'projects',
    //   displayName: 'menu.projects',
    //   meta: {
    //     // icon: 'folder_shared',
    //   },
    // },
    // {
    //   name: 'payments',
    //   displayName: 'menu.payments',
    //   meta: {
    //     // icon: 'credit_card',
    //   },
    //   children: [
    //     {
    //       name: 'payment-methods',
    //       displayName: 'menu.payment-methods',
    //     },
    //     {
    //       name: 'pricing-plans',
    //       displayName: 'menu.pricing-plans',
    //     },
    //     {
    //       name: 'billing',
    //       displayName: 'menu.billing',
    //     },
    //   ],
    // },
    // {
    //   name: 'auth',
    //   displayName: 'menu.auth',
    //   meta: {
    //     // icon: 'login',
    //   },
    //   children: [
    //     {
    //       name: 'login',
    //       displayName: 'menu.login',
    //     },
    //     {
    //       name: 'signup',
    //       displayName: 'menu.signup',
    //     },
    //     {
    //       name: 'recover-password',
    //       displayName: 'menu.recover-password',
    //     },
    //   ],
    // },

    // {
    //   name: 'faq',
    //   displayName: 'menu.faq',
    //   meta: {
    //     // icon: 'quiz',
    //   },
    // },
    // {
    //   name: '404',
    //   displayName: 'menu.404',
    //   meta: {
    //     // icon: 'vuestic-iconset-files',
    //   },
    // },
    // {
    //   name: 'preferences',
    //   displayName: 'menu.preferences',
    //   meta: {
    //     // icon: 'manage_accounts',
    //   },
    // },
    // {
    //   name: 'settings',
    //   displayName: 'menu.settings',
    //   meta: {
    //     // icon: 'settings',
    //   },
    // },
  ] as INavigationRoute[],
}
