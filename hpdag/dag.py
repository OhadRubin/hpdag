import networkx as nx
from itertools import product
import uuid



class TaskIterator:
    def __init__(self, tasks):
        self.tasks = tasks
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.tasks):
            raise StopIteration
        task = self.tasks[self.index]
        self.index += 1
        return task

class _Node:
    daemon_dag = None
    def __init__(self,*, name, values):
        if len(values)==0:
            values = [name]
        self.name = name
        self.uuid = uuid.uuid4()
        self.values = values
        self.daemon_dag.add_param(self)

    def __rshift__(self, other):
        assert self.daemon_dag is not None, "You must use this inside a DAG context"
        if isinstance(other,_Node):
            self.daemon_dag.link(self, other)
        elif isinstance(other,Branch):
            raise NotImplementedError("Node >> Branch is not supported")
        return other

    def __repr__(self):
        # return self.name,
        return f"Node({self.name}=[" + ", ".join(self.daemon_dag.params[self.uuid]) + "])"

class Node:
    def __init__(self, name):
        self.name = name
    def __call__(self, *values,l=None):
        if l is None:
            return _Node(name=self.name, values=values)
        else:
            assert len(values)==0, "You can only specify a list of values for a node with no links"
            return _Node(name=self.name, values=l)
            
    

class Branch:
    daemon_dag = None
    def __init__(self, *nodes):
        self.nodes = nodes


    def __rshift__(self, other):
        assert self.daemon_dag is not None, "You must use this inside a DAG context"
        if isinstance(other,Branch):
            for node in self.nodes:
                for other_node in other.nodes:
                    self.daemon_dag.link(node, other_node)
        else:
            assert isinstance(other,_Node)
            for node in self.nodes:
                self.daemon_dag.link(node, other)
        return other
    def __lshift__(self, other):
        return other >> self
        

    
class Task:
    daemon_dag = None
    def __init__(self, params):
        self.params = {}
        for k, v in params.items():
            k = self.daemon_dag.node_dict[k].name
            self.params[k] = v

    def __repr__(self):
        return "Task(" + ", ".join([f"{k}={v}" for k, v in self.params.items()]) + ")"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False
        return self.params == other.params

    def __hash__(self):
        return hash(tuple(sorted(self.params.items())))
    
class GraphOperations(nx.DiGraph):
    def get_all_paths(self, start_node, end_node):
        return list(nx.all_simple_paths(self, start_node, end_node))
    


class DAG(GraphOperations):
    
    def __init__(self):
        super().__init__()
        self.params = {}
        self.node_dict = {}
        self.layers = []
        self.out = None
        
    def add_param(self,node):
        self.add_node(node.uuid)
        self.params[node.uuid] = node.values
        self.layers.append(node.uuid)
        self.node_dict[node.uuid] = node



    def link(self, from_node, to_node):
        self.add_edge(from_node.uuid, to_node.uuid)
        

    def cartesian_product(self, nodes):
        return list(product(*[self.params[node] for node in nodes]))
    
    def get_all_paths(self, start_nodes, end_nodes):
        all_paths = []
        for start_node in start_nodes:
            for end_node in end_nodes:
                all_paths.extend(super().get_all_paths(start_node, end_node))
        return all_paths
    
    def get_start_nodes(self):
        return [node_uuid for node_uuid, in_degree in self.in_degree if in_degree == 0]
    

    def get_end_nodes(self):
        return [node_uuid for node_uuid, out_degree in self.out_degree if out_degree == 0]
    
    def __str__(self):
        start_nodes = self.get_start_nodes()
        end_nodes = self.get_end_nodes()
        all_paths = self.get_all_paths(start_nodes, end_nodes)
        return '\n'.join(map(str, self.generate_tasks(all_paths)))
    
    def generate_tasks(self, all_paths):
        return [
            Task({path[i]: combo[i] for i in range(len(combo))})
            for path in all_paths
            for combo in self.cartesian_product(path)
        ]

    def task_iterator(self):
        all_paths = self.get_all_paths(self.get_start_nodes(), self.get_end_nodes())
        return TaskIterator(self.generate_tasks(all_paths))
    
    @property
    def tasks(self):
        if self.out is None:
            return list(self.task_iterator())
        else:
            return self.out
    
    def __enter__(self):
        _Node.daemon_dag = self
        Task.daemon_dag = self
        Branch.daemon_dag = self
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.out = list(self.task_iterator())
