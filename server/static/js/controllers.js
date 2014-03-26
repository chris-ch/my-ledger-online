
angular.module('myledger.controllers', [])


/* ***************** */
/*                   */
/* Journal Entry     */
/*                   */
/* ***************** */

.controller('TemplateEntriesCreationModalController',
    ['$scope',
    function($scope) {
        $scope.template = new Object();
    }
])

.controller('NewJournalEntryController',
    ['$scope', '$window',
        'myledger.factories.AccountTreeFactory',
        'myledger.factories.TemplateEntriesFactory',
        'myledger.factories.EntriesManager',
        'myledger.factories.Currencies',
        'myledger.ACCOUNT_TYPES',
        'dateFilter',
        'createDialog',
    function($scope, $window,
        accountsFactory, 
        templateEntriesFactory,
        entriesManager,
        currencies,
        ACCOUNT_TYPES,
        dateFilter, createDialogService) {
        
        var legalEntityCode = $window.legalEntityCode;
        
        $scope.messages = new Array();
        $scope.accountTypes = ACCOUNT_TYPES;
        
        var templateEntries = templateEntriesFactory.create(legalEntityCode);
        
        var entriesManager = entriesManager.create(legalEntityCode);
        $scope.entries = entriesManager.entries;
        
        $scope.closeMessage = function(index) { $scope.messages.splice(index, 1); };
        
		$scope.launchTemplateEntriesModal = function() {
            console.log('modal entry template choice');
			createDialogService('/partials/templateEntriesModal.html', {
              id: 'templateEntriesModal',
              title: 'Template creation',
              backdrop: true,
              css: {},
              controller: 'TemplateEntriesCreationModalController',
              success: {
                    label: 'Create',
                    fn: function(){
                        // this function gets executed inside
                        // the scope of the modal controller
                        templateEntries.save(this.template.name,
                            entriesManager.entries,
                            $scope.currency.code)
                            .then(
                                function(){
                                    var message = 'Template successfully saved';
                                    $scope.messages.push({
                                        content: message,
                                        type: 'success'
                                        }
                                    );
                                })
                            .catch(
                                function(message){
                                    $scope.messages.push({ content: message});
                                }
                            );
                        }
                    },
              }
        	  );
		};
		
        function init(){
            entriesManager.reset();
            $scope.valueDate = new Date();
            currencies.load().then(
                function(result) {
                    $scope.currencies = result;
                    $scope.currency = $scope.currencies[0];
                }
            );
            templateEntries.loadAll().then(
                function(result) {
                    $scope.templates = result;
                }
            );
            var factory = accountsFactory.build(legalEntityCode);
            factory.loadAccounts().then(
                function() {
                    $scope.accounts = factory.flatAccounts();
                }
            );
        }
        
        init();
        entriesManager.addDoubleEntry();
        
        $scope.$watch('valueDate', function (valueDate){
            $scope.valueDateString = dateFilter(valueDate, 'yyyy-MM-dd');
        });
        
        $scope.$watch('valueDateString', function (valueDateString){
            $scope.valueDate = new Date(valueDateString);
        });
        
        $scope.removeEntry = function(index) {
            return entriesManager.remove(index);
        };
        
        $scope.addNewEntry = function() {
            return entriesManager.addDoubleEntry();
        };
        
        $scope.uploadNewEntries = function() {
            console.log('upload new entries');
            entriesManager.upload($scope.valueDate, $scope.currency)
                .then(
                    function(){
                        $scope.messages.push({
                                content: 'Data have been successfully uploaded',
                                type: 'success'
                        });
                    }
                )
                .catch(
                    function(message){
                        $scope.messages.push({ content: message });
                    }
                );
        };
        
        $scope.loadFromTemplate = function(template) {
            $scope.currentTemplate = template;
            entriesManager.loadFromTemplate(template.name)
                .catch(
                    function(message){
                        message = 'Failed to load template "' + template.name + '": ' + message;
                        $scope.messages.push({ content: message });
                    });
        };
        
        $scope.clearAll = function() {
            entriesManager.reset();
            entriesManager.addDoubleEntry();
        };
                
    }
])

/* ***************** */
/*                   */
/* Managing accounts */
/*                   */
/* ***************** */

.controller('SiblingsChoiceModalController',
    ['$scope', 'node', 'siblings',
    function($scope, node, siblings) {
        $scope.modalNode = node;
        $scope.modalSiblings = {
            choices: siblings,
            selection: siblings[0].id
        }
    }
])

.controller('AccountEditionModalController',
    ['$scope', 'node', 'treeSet', 'accountTypes',
    function($scope, node, treeSet, accountTypes) {
        $scope.account = node;
        $scope.flatAccounts = treeSet.flatAccounts();
        $scope.accountTypes = accountTypes;
        $scope.account.typeCode = treeSet.findAccountType(node.id).code;
    }
])

.controller('AccountCreationModalController',
    ['$scope',
        'treeSet',
        'accountTypes',
        'parent',
    function($scope, treeSet, accountTypes, parent) {
        $scope.flatAccounts = treeSet.flatAccounts();
        $scope.accountTypes = accountTypes;
        $scope.account = new Object();
        $scope.account.typeCode = accountTypes[0].code;        
        if(parent){
            $scope.account.parentId = parent.id;
            $scope.account.id = treeSet.generateNewCode(parent);
        }
    }
])

.controller('ManageAccountController',
    ['$scope', '$window',
        'myledger.factories.AccountTreeFactory',
        'myledger.factories.MenuItemTreeFactory',
        'createDialog',
        'myledger.ACCOUNT_TYPES',
    function($scope, $window,
            accountsTreeFactory,
            menuItemTreeFactory,
            createDialogService,
            ACCOUNT_TYPES) {
        
        $scope.accountTypes = ACCOUNT_TYPES;
        $scope.messages = new Array();
        var legalEntityCode = $window.legalEntityCode;
        var accountsTree = accountsTreeFactory.build(legalEntityCode);
        
		$scope.launchSiblingsChoiceModal = function(treeSet, node) {
            console.log('modal node', node);
            var siblings = treeSet.getSiblings(node.id);
			createDialogService('/partials/siblingsChoiceModal.html', {
              id: 'siblingsChoiceModal',
              title: 'Parent account selection',
              backdrop: true,
              css: {},
              controller: 'SiblingsChoiceModalController',
              success: {
                    label: 'Apply',
                    fn: function(){
                        // this function gets executed inside
                        // the scope of the modal controller
                        var targetNodeId = this.modalSiblings.selection;
                        console.log('selected:', targetNodeId);
                        treeSet.moveAccount(node.id, targetNodeId);
                        }
                    },
              },
              {
                  node: node,
                  siblings: siblings,
        	  }
        	  );
		};
		
		$scope.launchAccountEditionModal = function(treeSet, node) {
            console.log('editing node', node);
            var account_code = node.id;
			createDialogService('/partials/accountModal.html', {
              id: 'accountEditionModal',
              title: 'Account Edition',
              backdrop: true,
              css: {},
              controller: 'AccountEditionModalController',
              success: {
                    label: 'Save',
                    fn: function(){
                        // this function gets executed inside
                        // the scope of the modal controller
                        accountsTree.updateAccount(
                            account_code,
                            this.account.id,
                            this.account.name,
                            this.account.typeCode,
                            this.account.parentId,
                            legalEntityCode)
                        .then(function(result){
                            console.log('account updated');
                            });
                        }
                    },
              },
              {
                  node: node,
                  treeSet: treeSet,
                  accountTypes: ACCOUNT_TYPES,
              }
        	  );
		};
		
		$scope.launchAccountCreationModal = function(treeSet, parent) {
            console.log('modal account');
			createDialogService('/partials/accountModal.html', {
              id: 'accountCreationModal',
              title: 'Account Creation',
              backdrop: true,
              css: {},
              controller: 'AccountCreationModalController',
              success: {
                    label: 'Create',
                    fn: function(){
                        // this function gets executed inside
                        // the scope of the modal controller
                        treeSet.createAccount(
                            this.account.id,
                            this.account.name,
                            this.account.typeCode,
                            this.account.parentId,
                            legalEntityCode).then(
                                function(result){
                                    console.log('account updated');
                                },
                                function(message){
                                    $scope.messages.push({ content: message});
                                }
                            );
                        }
                    },
              },
              {
                  treeSet: treeSet,
                  accountTypes: ACCOUNT_TYPES,
                  parent: parent
        	  }
        	  );
		};
        
        $scope.closeMessage = function(index) { $scope.messages.splice(index, 1); };
        
        $scope.closeTreeMessage = function(treeview, index) {
            treeview.messages.splice(index, 1);
        };
  
        accountsTree.loadAccounts()
            .then(function(treeSet) {
                    $scope.treeSet = treeSet;
                    $scope.treeviewAccounts = treeSet.treeAccounts();
                    $scope.flatAccounts = treeSet.flatAccounts();
                
                // populates dropdown callback functions
                menuItemTreeFactory.initTreeSet(treeSet);
                menuItemTreeFactory.addItem('Open entries...',
                        function(node){ return node.badge != 0 },
                        function(node){
                            console.log('open', node);
                        }
                );
                menuItemTreeFactory.addSeparator();
                menuItemTreeFactory.addItem('Move up one level',
                        function(node){ return node.parent },
                        function(node){
                            treeSet.moveUp(node.id)
                                .catch(function(reason){
                                    var tree = treeSet.findTree(node.id);
                                    tree.messages.push({
                                        content: 'account ' + node.id + ' could not be moved up'
                                    });
                                });
                        });
                menuItemTreeFactory.addItem('Move under sibling...',
                        function(node){
                            return treeSet.getSiblings(node.id) && treeSet.getSiblings(node.id).length > 0;
                        },
                        function(node){
                            console.log('move under sibling', node);
                            $scope.launchSiblingsChoiceModal(treeSet, node);
                        });
                menuItemTreeFactory.addSeparator();
                menuItemTreeFactory.addItem('Edit...',
                        function(node){
                            return true;
                        },
                        function(node){
                            console.log('editing account', node);
                            $scope.launchAccountEditionModal(treeSet, node);
                        });
                menuItemTreeFactory.addItem('Remove',
                        function(node){
                            return node.badge == 0;
                        },
                        function(node){
                            console.log('remove', node);
                            treeSet.removeAccount(node.id)
                                .catch(function(reason){
                                    var tree = treeSet.findTree(node.id);
                                    tree.messages.push({ content: 'account ' + node.id + ' could not be removed'});
                                });
                        });
                menuItemTreeFactory.addSeparator();
                menuItemTreeFactory.addItem('Create sub-account...',
                        function(node){
                            return true;
                        },
                        function(node){
                            console.log('create a sub-account', node);
                            $scope.launchAccountCreationModal(treeSet, node);
                        });
            }
        );
        
    }
])

.controller('JournalController',
    ['$scope',
    'myledger.factories.EntriesListingFactory',
    
    function($scope, entriesListingFactory) {
        
    $scope.entries = entriesListingFactory.getEntries();

    var dateTemplate = '<div ng-class="col.colIndex()">'
        + '<div class="ngCellText" style="text-align: center;">'
        + '<span ng-cell-text>'
        + '{{row.getProperty(col.field) | date:\'yyyy/MM/dd\'}}'
        + '</span>'
        + '</div>'
        + '</div>';
        
    $scope.gridOptions = { 
        data: 'entries',
        enableCellSelection: false,
        enableRowSelection: false,
        enableCellEditOnFocus: false,
        plugins: [],
        columnDefs: [
            {
                field: 'date',
                displayName: 'Value Date',
                enableCellEdit: true,
                cellFilter: 'date:\'yyyy/MM/dd\'',
                width: '100px',
                cellTemplate: dateTemplate,
            },
            {
                field: 'ref',
                displayName: 'Ref',
                enableCellEdit: true,
                width: '60px'
            },
            {
                field: 'debit',
                displayName: 'Debit',
                enableCellEdit: true,
                width: '100px'
            },
            {
                field: 'credit',
                displayName: 'Credit',
                enableCellEdit: true,
                width: '100px'
            },
            {
                field: 'unitCost',
                displayName: 'Price',
                enableCellEdit: true,
                width: '80px',
                cellClass:'center', 
            },
            {
                field: 'quantity',
                displayName: 'Qty',
                enableCellEdit: true,
                width: '60px',
                cellClass:'center', 
            },
            {
                field: 'total',
                displayName: 'Amount',
                enableCellEdit: false,
                width: '100px',
                cellClass:'center', 
            },
            {
                field: 'currency',
                displayName: '',
                enableCellEdit: false,
                width: '50px',
                cellClass:'center', 
            },
            {
                field: 'label',
                displayName: 'Description',
                enableCellEdit: true
            },
        ]
    };
}
]
)

;


