'use strict';

angular.module('myledger',
    [
    'ngResource',
    'angularTreeview',
    'ui.bootstrap',
    'fundoo.services',
    'ngGrid',
    
    'myledger.services',
    'myledger.factories',
    'myledger.directives',
    'myledger.controllers',
    'myledger.transformers',
    'myledger.decorators',
  ]
)

/* Configuration */
    /* Version */
    .constant('APP_NAME','myLedger')
    .constant('APP_VERSION','0.1')
    
    /* Application constants */
    .constant('myledger.ACCOUNT_TYPES', [ 
        { code: 'A', name: 'Asset' },
        { code: 'L', name: 'Liability / Equity' },
        { code: 'I', name: 'Income' },
        { code: 'E', name: 'Expense' },
    ])
;

