import logging
import re
_LOG = logging.getLogger('oas.tools')

class NoneNotAllowedError:
    
    def __init__(self, message='Empty value is not allowed'):
        self._message = message
        
    def __str__(self):
        return self._message

class InvalidStringError:
    
    def __init__(self, value, message=''):
        self._value = value
        self._message = message
        
    def __str__(self):
        output = 'invalid string "%s"' % self._value
        if self._message:
            output += ' (%s)' % self._message
            
        return output

def assert_not_none(a_value):
    if a_value is None:
        raise NoneNotAllowedError()
        
def assert_not_empty(a_string):
    if len(a_string) == 0:
        raise InvalidStringError(a_string)

def assert_no_space(a_string):
    if re.match(r'.*\s', a_string):
        raise InvalidStringError(a_string, 'spaces not allowed')

class SimpleGraphError(Exception):
    pass

class OperationNotAllowed(SimpleGraphError):
    def __init__(self, message=''):
        self.__message = message
        
    def __str__(self):
        return repr(self.__message)

class AlreadyAdded(SimpleGraphError):
    def __init__(self, node):
        self.__node = node
        
    def __str__(self):
        return 'Already added: %s' % repr(self.__node)

class UnkownNode(SimpleGraphError):
    def __init__(self, node):
        self.__node = node
        
    def __str__(self):
        return 'Unknown: %s' % repr(self.__node)

class SimpleGraph(object):
    """
    Graph implemented using one dict for sources and one dict for destinations.
    """
    def __init__(self):
        self.__sources = dict()
        self.__destinations = dict()
        self.__nodes = set()
    
    def add_nodes(self, **args):
        for node in args:
            self.add_node(node)
            
    def add_node(self, node):
        """
        One node can not be added multiple times. Any attempt will be ignored.
        """
        self.__nodes.add(node)
        if not self.__sources.has_key(node):
            self.__sources[node] = set()
            
        if not self.__destinations.has_key(node):
            self.__destinations[node] = set()
        
    def add_directed_edge(self, source, dest):
        """
        One-way edge.
        """
        self.add_node(source)
        self.add_node(dest)
        self.__sources[dest].add(source)
        self.__destinations[source].add(dest)
        
    def add_edge(self, node1, node2):
        """
         edge.
        """
        self.add_directed_edge(node1, node2)
        self.add_directed_edge(node2, node1)
        
    def get_sources(self, node):        
        if not self.has_node(node):
            raise UnkownNode(node)
            
        return self.__sources[node]
        
    def get_destinations(self, node):
        if not self.has_node(node):
            raise UnkownNode(node)
            
        return self.__destinations[node]

    def has_node(self, node):
        return node in self.__nodes
        
    def is_source(self, node):
        if not self.has_node(node):
            raise UnkownNode(node)
            
        return len(self.__destinations[node]) > 0
        
    def is_destination(self, node):
        if not self.has_node(node):
            raise UnkownNode(node)
            
        return len(self.__sources[node]) > 0
        
    def get_nodes(self):
        return self.__nodes

    def __repr__(self):
        """
        Matrix representing the graph.
        """
        LINE_SEP = '\n'
        matrix = LINE_SEP
        nodes = [node for node in self.__nodes if not (self.is_source(node) and self.is_destination(node))]
        left_over = [node for node in self.__nodes if not node in nodes]
        
        def get_node_key(node_index):
            return chr(int(node_index / 26) + ord('a')) + chr(node_index % 26 + ord('a'))
        
        for count, node in enumerate(nodes):
            matrix += '%s: %s' % (get_node_key(count), node) + LINE_SEP
            
        matrix += '%3s' % ' '
        for count_h, node_h in enumerate(nodes):
            if not self.is_destination(node_h):
                matrix += '%3s' % (get_node_key(count_h))
        
        matrix += LINE_SEP
        for count_v, node_v in enumerate(nodes):
            if not self.is_source(node_v):
                matrix += get_node_key(count_v)
                for count_h, node_h in enumerate(nodes):
                    if not self.is_destination(node_h):
                        if node_v in self.get_destinations(node_h):
                            matrix += '%3s' % 'X'
                        
                        else:
                            matrix += '%3s' % '.'
                        
                matrix += LINE_SEP
        
        if len(left_over) > 0:
            matrix += 'Left over: ' + LINE_SEP
            matrix += ', '.join(map(str, left_over))
        
        return matrix

class Walkable(object):
    
    def __init__(self):        
        self.__graph = SimpleGraph()
    
    def is_root(self, node):
        return not self.__graph.is_destination(node)
        
    def is_leaf(self, node):
        return not self.__graph.is_source(node)
        
    def get_children(self, node):
        return self.__graph.get_destinations(node)
        
    def get_leaves(self):
        return [node for node in self.__graph.get_nodes() if self.is_leaf(node)]

    def walk(self, node, parent=None, level=0, top_down=True, sort_key=lambda x: x):
        current_node = node
        current_parent = parent
        current_level = level
        
        #_LOG.debug('current node %s: %s' % (str(current_node), str(self.get_children(current_node))))
        
        if top_down:
            #_LOG.debug('reached main node %3d: %s' % (level, str(node)))
            yield current_node, current_parent, current_level
        
        #_LOG.debug('inspecting children of %s: %s' % (str(current_node), str(self._get_graph().get_destinations(current_node))))
        
        for child in sorted(self.get_children(node), key=sort_key):
            for node, parent, level in self.walk(child, current_node, current_level+1, top_down):
                #_LOG.debug('reached child node %3d: %s' % (level, str(node)))
                yield node, parent, level
        
        if not top_down:
            #_LOG.debug('reached main node %3d: %s' % (current_level, str(current_node)))
            yield current_node, current_parent, current_level

    def has_node(self, node):
        return self._get_graph().has_node(node)

    def _get_graph(self):
        return self.__graph

class SimpleTreeSet(Walkable):
    """
    Maintaining a set of trees (also known as Forest).
    """
    def __init__(self):
        Walkable.__init__(self)
        
    def add_root(self, node):
        if self._get_graph().has_node(node):
            raise AlreadyAdded(node)
            
        self._get_graph().add_node(node)
        
    def create_parent_child(self, parent, child):
        """
        The child must be a root.
        """
        if not self._get_graph().has_node(parent):
            self.add_root(parent)
            
        if not self._get_graph().has_node(child):
            self.add_root(child)
            
        if not self.is_root(child):
            raise OperationNotAllowed('The child must be a tree root')
            
        self._get_graph().add_directed_edge(parent, child)
        
    def get_roots(self):
        return [node for node in self._get_graph().get_nodes() if self.is_root(node)]

    def attach_tree(self, tree):
        node_list = tree.walk(node=tree.get_root(), top_down=True)
        for node, parent, level in node_list:
            if parent is None:
                self.add_root(node)
            else:
                self.create_parent_child(parent, node)
    
    def group(self):
        tree = SimpleTree()
        #_LOG.debug('grouping trees')
        for root in self.get_roots():
            node_list = self.walk(node=root, top_down=True)
            for node, parent, level in node_list:
                #_LOG.debug('aggregating node %s' % str(node))
                if parent is not None:
                    #_LOG.debug('adding edge %s -> %s' % (parent, node))
                    tree.add_child(parent, node)
                else:
                    #_LOG.debug('adding root %s -> %s' % (tree.get_root(), node))
                    tree.add_child(tree.get_root(), node)
            
        return tree
        
    def __str__(self):
        return str(self._get_graph())
    
class SimpleTree(Walkable):
    
    def __init__(self, root_node=None):
        Walkable.__init__(self)
        
        class DefaultRoot(object):
            
            def __repr__(self):
                return '<root>'
        
        if root_node is None:
            root_node = DefaultRoot()
            
        self._get_graph().add_node(root_node)
        self.__root = root_node
    
    def add_child(self, parent, child):
        if not self._get_graph().has_node(parent):
            raise UnkownNode(parent)
            
        self._get_graph().add_directed_edge(parent, child)
        
    def get_root(self):
        return self.__root
        
    def get_children_root(self):
        return self.get_children(self.get_root())
        
    def __repr__(self):
        return str(tree_to_dict(self))

def safe_transform(tree, transform, node):
    if node == tree.get_root():
        tr_node = '<root>'
        
    else:
        tr_node = transform(node)
        
    return tr_node

def tree_to_dict(tree, key_transform=lambda x: x, data_transform=lambda x: x):
    """
    @return: pair (dict representing the tree, dict mapping nodes with data)
    """
    walk = tree.walk(tree.get_root(), top_down=True)
    dict_struct = dict()
    dict_data = dict()
    for node, parent, level in walk:
        tr_node = safe_transform(tree, key_transform, node)
        dict_struct[tr_node] = dict()
        if not dict_data.has_key(tr_node):
            dict_data[tr_node] = safe_transform(tree, data_transform, node)
            
        if parent:
            tr_parent = safe_transform(tree, key_transform, parent)
            dict_struct[tr_parent][tr_node] = dict_struct[tr_node]

    root = safe_transform(tree, key_transform, tree.get_root())
    dict_data.pop('<root>', None)
    return (dict_struct[root], dict_data)

def test_tree_set():
    tree = SimpleTreeSet()
    tree.add_root('top')
    tree.add_root('child_1')
    tree.add_root('child_2')
    tree.add_root('child_3')
    tree.add_root('child_1_1')
    tree.add_root('child_1_2')
    tree.add_root('child_1_3')
    tree.add_root('child_1_1_1')
    tree.add_root('child_1_1_2')
    tree.add_root('child_1_3_1')
    tree.add_root('child_3_1')
    tree.add_root('child_3_2')
    tree.create_parent_child('top', 'child_1')
    tree.create_parent_child('top', 'child_2')
    tree.create_parent_child('child_1', 'child_1_1')
    tree.create_parent_child('child_1', 'child_1_2')
    tree.create_parent_child('child_1', 'child_1_3')
    tree.create_parent_child('child_1_1', 'child_1_1_1')
    tree.create_parent_child('child_1_1', 'child_1_1_2')
    tree.create_parent_child('child_3', 'child_3_1')
    tree.create_parent_child('child_3', 'child_3_2')
    tree.create_parent_child('top', 'child_3')
    node_list = tree.walk(node='top', top_down=False)
    for node, parent, level in node_list:
        _LOG.debug(str(level) + ':' + '   ' * level + str(node))

def test_tree():
    tree = SimpleTree('top')
    tree.add_child('top', 'child_1')
    tree.add_child('top', 'child_2')
    tree.add_child('top', 'child_3')
    tree.add_child('child_1', 'child_1_1')
    tree.add_child('child_1', 'child_1_2')
    tree.add_child('child_1', 'child_1_3')
    tree.add_child('child_1_1', 'child_1_1_1')
    tree.add_child('child_1_1', 'child_1_1_2')
    tree.add_child('child_3', 'child_3_1')
    tree.add_child('child_3', 'child_3_2')
    node_list = tree.walk(node='top', top_down=False)
    for node, parent, level in node_list:
        _LOG.debug(str(level) + ':' + '   ' * level + str(node))
