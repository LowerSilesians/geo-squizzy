from copy import deepcopy
import geosquizzy.utils as utils


class Tree:
    def __init__(self, *args, **kwargs):
        self.leaf = dict({'id': None, 'children': [], 'level': 0, 'parent': None, 'completed': False})
        """
        @self.leaf completed property will announce that the leaf is ready
        """
        self.tree = dict()
        self.nodes = dict()

    def add_leaf(self, id=None, leaf=None):
        if self.nodes.get(id, None) is None:
            self.nodes[id] = leaf
        else:
            self.nodes[leaf['id']] = leaf
            self.nodes[id]['children'].append(leaf['id'])

    def get_all_leafs_paths(self):
        """will return list of list where each list contain
           a path to leaf ['properties', 'some_property', 'root']
           the each path direction is descending from leaf to the root
           we removed root as it is only abstract
           node which doesn't exist in geojson doc
        """
        paths = []
        for x in self.nodes:
            current_path = []
            if self.nodes[x]['children'].__len__() == 0:
                current_path.append(self.nodes[x]['id'])
                last_parent = self.nodes[x]['parent']
                while not (last_parent is None):
                    current_path.append(self.nodes[last_parent]['id'])
                    if not (self.nodes[last_parent]['parent'] is None):
                        last_parent = self.nodes[last_parent]['parent']
                    else:
                        paths.append(current_path)
                        last_parent = None
        return paths

    def prepare_new_leaf(self, **kwargs):
        new_leaf = deepcopy(self.leaf)
        new_leaf['id'] = kwargs.get('id', None)
        new_leaf['level'] = kwargs.get('level', None)
        new_leaf['parent'] = kwargs.get('parent', None)
        return new_leaf


class FeaturesTree(Tree):
    def __init__(self, *args, **kwargs):
        super(FeaturesTree, self).__init__(*args, **kwargs)
        root = self.prepare_new_leaf(id='root', level=0)
        geometry = self.prepare_new_leaf(id='geometry', level=1, parent='root')
        properties = self.prepare_new_leaf(id='properties', level=1, parent='root')
        self.add_leaf(id='root', leaf=root)
        self.add_leaf(id='root', leaf=geometry)
        self.add_leaf(id='root', leaf=properties)
        #print(self.nodes)
        #print(self.get_all_leafs_paths())


class GeoJSON:
    def __init__(self, *args, **kwargs):
        self.type = kwargs['geojson_doc_type']
        self.data = dict({"type": self.type, "features": []})
        self.tree = FeaturesTree()
        self.geojson = None
        self.percentage = None
        self.is_doc = False
        pass

    def start(self, **kwargs):
        """
        kwargs['is_doc'] is optional flag but provided will grow
        the performance, we will not have to check if doc is a chunk or full doc
        """
        self.geojson = kwargs.get('geojson', None)
        self.percentage = kwargs.get('percentage', None)
        self.is_doc = kwargs.get('is_doc', False)
        self.__read_geojson__()

    def get_keys(self):
        pass

    def __read_geojson__(self):
        """
        @self.percentage How much of the provided geojson should be checked, default is set to all
        @self.geojson String which can represent both or full geojson document or what will be in favour for future
         improvements it could be a chunk of String which consist a full geojson document

        as main activity it should all the time update self.tree nodes
        """

        if self.is_doc or utils.is_geojson_doc(self.geojson):
            """
            geojson doc mode
            """
            features_string = utils.get_string_slice(r'features (.*) ]', self.geojson, 2)
            print(features_string)
            pass
        else:
            """
            geojson chunk mode
            """
            pass