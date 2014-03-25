'use strict';

angular.module('myledger.services', [])

.service('myledger.services.JsonRPCService',
    ['$q', '$http',
            'myledger.transformers.IdentityTransformer',
            'myledger.transformers.TreeTransformer',
        function($q, $http, identityTransformer, treeTransformer) {
            
    /* UUID generator for JSON-RPC requests */
    function s4() {
      return Math.floor((1 + Math.random()) * 0x10000)
                 .toString(16)
                 .substring(1);
    };
    
    function guid() {
      return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
             s4() + '-' + s4() + s4() + s4();
    }

    this.call = function (rpcName, params, responseTransformer) {
        var deferred = $q.defer();
        if(_.isUndefined(responseTransformer)){
            responseTransformer = identityTransformer;
        }
        $http(
            {
                method: 'POST',
                url: '/jsonrpc/',
                data: {
                    'jsonrpc': '2.0',
                    'method': rpcName,
                    'id': guid(),
                    'params': params,
                    },
                transformResponse: responseTransformer
            }
            ).
            success(function(data, status) {
                deferred.resolve(data.result);
            }).
            error(function(response, status) {
                console.log('response', response.error.message);
                deferred.reject(response.error.message);
            });
        return deferred.promise;
    };
    
    this.callTree = function (rpcName, params) {
        return this.call(rpcName, params, treeTransformer);
    }
    
}
])

.service('myledger.services.OASRPCService',
    [   'myledger.services.JsonRPCService',
        'myledger.ACCOUNT_TYPES',
        function(jsonrpc, ACCOUNT_TYPES) {
            
    self = this;
    
    function extractDebitCredit(group){
        return {
            debit: group.debitEntries,
            credit: group.creditEntries
        };
    }
    
    self.saveTemplate = function (templateName, legalEntityCode, 
            journalEntries, currencyCode) {
        return jsonrpc.call('save_journal_entries_template',
            [legalEntityCode, currencyCode, templateName, _.map(journalEntries, extractDebitCredit)]
            );
    };
    
    self.saveJournalEntries = function(
            legalEntityCode, 
            journalEntries, currencyCode, valueDate) {
        
        return jsonrpc.call('save_journal_entries',
            [legalEntityCode, currencyCode, valueDate, _.map(journalEntries, extractDebitCredit)]
            );
    };
    
    self.loadCurrencies = function() {
        return jsonrpc.call('get_currencies', []);
    };
    
    self.removeAccount = function(legalEntityCode, accountCode) {
        return jsonrpc.call('remove_account',
            [accountCode, legalEntityCode]
        );
    };
    
    self.loadTemplates = function(legalEntityCode) {
        return jsonrpc.call('get_templates', [legalEntityCode]);
    };
    

    self.loadFromTemplate = function(templateName, legalEntityCode) {
        return jsonrpc.call('get_template_data', [legalEntityCode, templateName]);
    };

    self.createAccount = function(new_code, new_name, new_account_type_code,
            new_parent_code, legalEntityCode) {
        var operationName = 'create_asset_account';
        switch(new_account_type_code) {
            case 'L':
                operationName = 'create_liability_account';
              break;
            case 'I':
                operationName = 'create_income_account';
              break;
            case 'E':
                operationName = 'create_expense_account';
              break;
        }
        var description = ''
        return jsonrpc.call(operationName,
                [
                    new_code, new_name, description, new_parent_code, legalEntityCode
                ]
        );
    }
    
    self.loadEntriesCount = function(legalEntityCode) {
        return jsonrpc.call('get_entries_count', [legalEntityCode])
            .then(function(result) {
                    var entriesCount = _.object(_.map(result, function(item) {
                       return [item.code, item.count_entries]
                    }));
                    return entriesCount;
                    }
                );
    }
    
    self.loadAccounts = function(legalEntityCode) {
        return jsonrpc.callTree('get_accounts', [legalEntityCode]);
    }

    self.updateAccount = function(currentCode, newCode, newName,
            newAccountTypeCode, newParentCode, legalEntityCode){
        return jsonrpc.call('update_account',
                [ currentCode, newCode,  newName,
                 newAccountTypeCode, newParentCode, legalEntityCode ]
                 );
    }
    
    self.moveAccount = function(accountCode, targetAccountCode, legalEntityCode){
        return jsonrpc.call('move_account',
            [ accountCode, targetAccountCode, legalEntityCode ]
            );
    }
    
    self.moveUpAccount = function(accountCode, legalEntityCode){
        return jsonrpc.call('move_up_account',
                [ accountCode, legalEntityCode ]
        );
    }

}
])

;


