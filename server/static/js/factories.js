'use strict';

angular.module('myledger.factories', [])

.factory('myledger.factories.EntryFactory',
    [
        'myledger.ACCOUNT_TYPES',
        
    function(accountTypes){
                
        return {
            create: function(accountCode, accountType, quantity, price, label){
                var newEntry = new Object();
                newEntry.accountCode = accountCode;
                newEntry.accountType = accountType || accountTypes[0].code;
                newEntry.label = label;
                if(quantity){
                    newEntry.quantity = parseFloat(quantity).toFixed(2);
                } else{
                    newEntry.quantity = 1;
                } 
                if(price){
                    newEntry.price = parseFloat(price).toFixed(2);
                } else{
                    newEntry.price = '';
                }
                return newEntry;
            }
        }
    }
])

.factory('myledger.factories.EntriesListingFactory',
    [
    function(){
                
        return {
        }
    }
])

.factory('myledger.factories.EntryGroupFactory',
    [
        'myledger.factories.EntryFactory',
    function(entryFactory){
        return {
            create: function(){
                var group = new Object();
                group.debitEntries = new Array();
                group.creditEntries = new Array();
                
                group.addDebitEntry = function(accountCode, accountType, quantity, price, label){
                    var entry = entryFactory.create(accountCode, accountType, quantity, price, label);
                    group.debitEntries.push(entry);
                }
                
                group.insertDebitEntry = function(antecedent){
                    var entry = entryFactory.create();
                    var index = _.indexOf(group.debitEntries, antecedent);
                    group.debitEntries.splice(index, 0, entry);
                }
                
                group.addCreditEntry = function(accountCode, accountType, quantity, price, label){
                    var entry = entryFactory.create(accountCode, accountType, quantity, price, label);
                    group.creditEntries.push(entry);
                }
                
                group.insertCreditEntry = function(antecedent){
                    var entry = entryFactory.create();
                    var index = _.indexOf(group.creditEntries, antecedent) + 1;
                    group.creditEntries.splice(index, 0, entry);
                }
                
                group.addDoubleEntry = function(accountDebit, accountCredit, typeDebit, typeCredit, quantity, price){
                    group.addDebitEntry(accountDebit, typeDebit, quantity, price);
                    group.addCreditEntry(accountCredit, typeCredit, quantity, price);
                }
                
                group.isMergeCandidate = function(){
                    return group.debitEntries.length == 1
                        &&  group.creditEntries.length == 1;
                }
                
                group.removeDebit = function(index) {
                    group.debitEntries.splice(index, 1);
                    if(group.isMergeCandidate()) {
                        // keeps both side in sync in that case
                        group.debitEntries[0].price = group.creditEntries[0].price;
                        group.debitEntries[0].quantity = group.creditEntries[0].quantity;
                    }
                }
                
                group.removeCredit = function(index) {
                    group.creditEntries.splice(index, 1);
                    if(group.isMergeCandidate()) {
                        // keeps both side in sync in that case
                        group.creditEntries[0].price = group.debitEntries[0].price;
                        group.creditEntries[0].quantity = group.debitEntries[0].quantity;
                    }
                }
                
                group.reset = function() {
                    group.debitEntries.length = 0;
                    group.creditEntries.length = 0;
                }
                
                group.diffDebitCredit = function() {
                    var sumDebit = 0;
                    var sumCredit = 0;
                    _.each(group.debitEntries, function (entry) {
                            sumDebit += entry.price * entry.quantity;
                        });
                    _.each(group.creditEntries, function (entry) {
                            sumCredit += entry.price * entry.quantity;
                        });
                    return sumDebit - sumCredit;
                };
                
                return group;
            }
        }
    }
])

.factory('myledger.factories.EntriesManager',
    [
        'myledger.services.OASRPCService',
        'myledger.factories.EntryGroupFactory',
    function(oasrpc, entryGroupFactory){
        return {
            create: function(legalEntityCode) {
                
                var manager = new Object();
                manager.entries = new Array();
                                
                manager.reset = function() {
                    // emptying the array
                    _.each(manager.entries, function(group) {
                            group.reset();
                        });
                    manager.entries.length = 0;
                };
                
                manager.createGroup = function() {
                    var group = entryGroupFactory.create();
                    manager.entries.push(group);
                    return group;
                };
                
                manager.addDoubleEntry = function(accountDebit, accountCredit, typeDebit, typeCredit, quantity, price){
                    var group = entryGroupFactory.create();
                    group.addDoubleEntry(accountDebit, accountCredit, typeDebit, typeCredit, quantity, price);
                    manager.entries.push(group);
                    return group;
                };
                
                manager.remove = function(index){
                    manager.entries.splice(index, 1);
                };
                
                manager.upload = function(valueDate, currency){
                    return oasrpc.saveJournalEntries(
                        legalEntityCode,
                        manager.entries,
                        currency.code,
                        valueDate);
                    };
                
                
                manager.loadFromTemplate = function(templateName){
                    manager.reset();
                    return oasrpc.loadFromTemplate(templateName, legalEntityCode)
                    .then(function(result){
                        for(var indexGroup=0; indexGroup < result.length; indexGroup++) {
                            var group = manager.createGroup();
                            for(var indexEntry=0; indexEntry < result[indexGroup].length; indexEntry++) {
                                var template = result[indexGroup][indexEntry];
                                console.log('read template', template);
                                var accountCode = template.account_code;
                                var accountType = template.account_type_code;
                                var quantity = template.quantity;
                                var price = template.unit_cost;
                                var description = template.description
                                if(template.is_debit){
                                    group.addDebitEntry(accountCode, accountType, quantity, price, description);
                                }
                                else {
                                    group.addCreditEntry(accountCode, accountType, quantity, price, description);
                                }
                            }
                        }
                    });
                };
                    
                return manager;
            }
        }
    }
])

.factory('myledger.factories.TemplateEntriesFactory',
    [
        'myledger.services.OASRPCService',
    function(oasrpc){
        return {
            create: function(legalEntityCode){
                
                var factory = new Object();
                
                factory.save = function(templateName, entries, currencyCode){
                    return oasrpc.saveTemplate(
                        templateName, legalEntityCode, entries, currencyCode);
                }
                
                factory.loadAll = function(){
                    return oasrpc.loadTemplates(legalEntityCode);
                }
               
               return factory;
            }
        }
    }
])

.factory('myledger.factories.Currencies',
    [
        'myledger.services.OASRPCService',
    function(oasrpc){
        return {
            load: function(){
                return oasrpc.loadCurrencies();
               }
        }
    }
])

.factory('myledger.factories.AccountTreeFactory',
    [
        '$q',
        'myledger.services.OASRPCService',
        'myledger.ACCOUNT_TYPES',
    function($q, oasrpc, ACCOUNT_TYPES){
    return {
        build: function(legalEntityCode){
            
            var treeSet = new Object();
            
            treeSet.loadAccounts = function() {
                var trees = oasrpc.loadAccounts(legalEntityCode)
                    .then(function(oasTrees){
                        treeSet.assetTree = oasTrees[0][0];
                        treeSet.liabilityTree = oasTrees[1][0];
                        treeSet.incomeTree = oasTrees[2][0];
                        treeSet.expenseTree = oasTrees[3][0];
                        // attaching entries count
                        return oasrpc.loadEntriesCount(legalEntityCode)
                            .then(function(entriesCount){
                                treeSet.walk(function(node){
                                        node.badge = entriesCount[node.id];
                                    });
                                treeSet.assetTree.messages = new Array();
                                treeSet.liabilityTree.messages = new Array();
                                treeSet.incomeTree.messages = new Array();
                                treeSet.expenseTree.messages = new Array();
                                return treeSet;
                                });
                    });
                return trees;
            }
    
            treeSet.generateNewCode = function(referenceNode){
                var referenceCode = referenceNode.id;
                var counter = 0;
                var newCode = '';
                do  {
                    counter++;
                    newCode = referenceCode + '.' + counter;
                } while(treeSet.lookupNodeId(newCode));
                return newCode;
            }
                
            treeSet.assetAccounts = function(){
                var nodes = new Object();
                treeSet.walk(function(node){
                            nodes[node.id] = node.name;
                        }
                        , treeSet.assetTree);
                return nodes
            }
            
            treeSet.liabilityAccounts = function(){
                var nodes = new Object();
                treeSet.walk(function(node){
                            nodes[node.id] = node.name;
                        }
                        , treeSet.liabilityTree);
                return nodes
            }
            
            treeSet.incomeAccounts = function(){
                var nodes = new Object();
                treeSet.walk(function(node){
                            nodes[node.id] = node.name;
                        }
                        , treeSet.incomeTree);
                return nodes
            }
            
            treeSet.expenseAccounts = function(){
                var nodes = new Object();
                treeSet.walk(function(node){
                            nodes[node.id] = node.name;
                        }
                        , treeSet.expenseTree);
                return nodes
            }
            
            treeSet.flatAccounts = function(){
                return {
                'A': treeSet.assetAccounts(),
                'L': treeSet.liabilityAccounts(),
                'I': treeSet.incomeAccounts(),
                'E': treeSet.expenseAccounts()
                }
            }
            
            treeSet.treeAccounts = function(){
                return {
                'A': treeSet.assetTree,
                'L': treeSet.liabilityTree,
                'I': treeSet.incomeTree,
                'E': treeSet.expenseTree
                }
            }
            
            treeSet.lookupNodeId = function(nodeId){
                var node = treeSet.walk(function(currentNode, foundNode){
                                if(_.isUndefined(foundNode)){
                                    if (currentNode.id == nodeId){
                                        return currentNode;
                                    }
                                } else {
                                    return foundNode;
                                }
                            });
                return node;
            }
            
            treeSet.findTree = function(nodeId){
                var accountType = treeSet.findAccountType(nodeId);
                switch(accountType.code){
                    case 'A':
                        return treeSet.assetTree;
                    case 'L':
                      return treeSet.liabilityTree;
                    case 'I':
                      return treeSet.incomeTree;
                    case 'E':
                      return treeSet.expenseTree;
                }
            }
            
            treeSet.findAccountType = function(nodeId){;
                if(_.has(treeSet.liabilityAccounts(), nodeId)){
                    return _.find(ACCOUNT_TYPES, function (type) { return type.code === 'L' });
                } else if(_.has(treeSet.incomeAccounts(), nodeId)){
                    return _.find(ACCOUNT_TYPES, function (type) { return type.code === 'I' });
                } else if(_.has(treeSet.expenseAccounts(), nodeId)){
                    return _.find(ACCOUNT_TYPES, function (type) { return type.code === 'E' });
                } else {
                    return _.find(ACCOUNT_TYPES, function (type) { return type.code === 'A' });
                }
            }
            
            treeSet.findLayer = function(nodeId){
                var node = treeSet.lookupNodeId(nodeId);
                if(node.parent) {
                    var parent = treeSet.lookupNodeId(node.parent);
                    return parent.children;
                } else {
                    return treeSet.findTree(nodeId);
                }
            }
            
            treeSet.getSiblings = function(nodeId){
                var children = treeSet.findLayer(nodeId);
                var siblings = _.filter(children, function(item){
                                        return item.id != nodeId;
                                    }
                                );
                return siblings;
            }
            
            treeSet.moveAccount = function(code, targetCode){
                return oasrpc.moveAccount(code, targetCode, legalEntityCode)
                    .then(
                    function(result){
                        var node = treeSet.lookupNodeId(code);
                        var targetNode = treeSet.lookupNodeId(targetCode);
                        var targetLayer = targetNode.children;
                        var sourceLayer = treeSet.findLayer(node.id);
                        // removes from current location
                        var nodeIndex = _.indexOf(sourceLayer, node);
                        sourceLayer.splice(nodeIndex, 1);
                        // insertion into new place
                        targetLayer.push(node);
                        node.parent = targetNode.parent
                    }
                );
            }
            
            treeSet.moveUp = function(nodeId){
                return oasrpc.moveUpAccount(nodeId, legalEntityCode)
                    .then(
                    function(result){
                        var node = treeSet.lookupNodeId(nodeId);
                        var parent = treeSet.lookupNodeId(node.parent);
                        var parentLayer = treeSet.findLayer(node.parent);
                        
                        // removes from current location
                        treeSet.popAccount(nodeId);
                        
                        // insertion into new place
                        node.parent = parent.parent
                        parentLayer.push(node);
                    }
                );
            }
            
            treeSet.removeAccount = function(nodeId){
                var node = treeSet.lookupNodeId(nodeId);
                var moveUpNodes = new Array();
                for(var index=0; index < node.children.length; index++){
                    moveUpNodes.push(node.children[index].id);
                }
                var requests = new Array();
                for(var index=0; index < node.children.length; index++){
                    requests.push(treeSet.moveUp(moveUpNodes[index]));
                }
                return $q.all(requests).
                    then(function(){
                        return oasrpc.removeAccount(legalEntityCode, nodeId).then(
                            function(result){
                                treeSet.popAccount(nodeId);
                            }
                            );
                    }
                    );
            }
            
            treeSet.createAccount = function(code,
                            name,
                            typeCode,
                            parentCode,
                            legalEntityCode){
                return oasrpc.createAccount(code, name, typeCode,
                    parentCode, legalEntityCode).then(
                    function(result){
                        var newAccount = {
                                    id: code,
                                    name: name,
                                    parent: parentCode
                            };
                        if(parentCode){
                            var layer = treeSet.findLayer(parentCode);
                            layer.push(newAccount);
                        } else {
                            treeSet.treeAccounts[typeCode].push(newAccount);
                        }
                    }
                    );
            }
            
            treeSet.popAccount = function(nodeId){
                var node = treeSet.lookupNodeId(nodeId);
                var layer = treeSet.findLayer(nodeId);
                var nodeIndex = _.indexOf(layer, node);
                layer.splice(nodeIndex, 1);
                return node
            }
            
            treeSet.updateAccount = function(currentCode, code,
                            name,
                            typeCode,
                            parentCode,
                            legalEntityCode){
                return oasrpc.updateAccount(currentCode, code, name, typeCode,
                    parentCode, legalEntityCode).then(
                        function(result){
                            var node = treeSet.lookupNodeId(currentCode);
                            var currentType = treeSet.findAccountType(currentCode);
                            node.id = code;
                            node.name = name;
                            var account = treeSet.popAccount(code);
                            if (parentCode){
                                var parentAccount = treeSet.lookupNodeId(parentCode);
                                parentAccount.children.push(account);
                                account.parent = parentAccount.id;
                            } else {
                                var treeAccounts = treeSet.treeAccounts();
                                treeAccounts[typeCode].push(account);
                            }
                        }
                    );
            }
            
            treeSet.walk = function(func, tree, value, visited_nodes){
                // recursively calls func(node) on each node of each tree
                // and returns aggregated results
                if(_.isUndefined(visited_nodes)){
                    visited_nodes = new Object();
                }
                var result = value; 
                if(_.isUndefined(tree)){
                    result = treeSet.walk(func, treeSet.assetTree, result, visited_nodes);
                    result = treeSet.walk(func, treeSet.liabilityTree, result, visited_nodes);
                    result = treeSet.walk(func, treeSet.incomeTree, result, visited_nodes);
                    result = treeSet.walk(func, treeSet.expenseTree, result, visited_nodes);
                } else {
                    for(var index=0; index < tree.length; index++){
                        var node = tree[index];
                        if(visited_nodes[node.id]){
                            throw {
                                message: 'inconsistent tree: loop detected',
                                node: node.id
                            };
                        }
                        visited_nodes[node.id] = true;
                        var localValue = func(node, result);
                        result = treeSet.walk(func, node.children, localValue, visited_nodes);
                    }
                }
                return result;
            }
            
            return treeSet;
        },
    }
}
    ])

.factory('myledger.factories.MenuItemTreeFactory',
    function(){
    var treeSet;
    return {
        initTreeSet: function(aTreeSet){
            treeSet = aTreeSet;
        },
        addItem: function(label, enabling, action){
            treeSet.walk(function(node){
                if(_.isUndefined(node.items)){
                    node.items = new Array();
                }
                var items = [
                    label,
                    enabling(node),
                    function(){ action(node); }
                ];
                node.items.push(items);
            });
        },
        addSeparator: function(){
            treeSet.walk(function(node){
                if(_.isUndefined(node.items)){
                    node.items = new Array();
                }
                node.items.push(['']);
            });
        }
    }
})

;
