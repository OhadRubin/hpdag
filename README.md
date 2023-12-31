# hpdag
hpdag is a lightweight library designed to simplify experiment configurations in your research.
Inspired by Airflow, define your experimental workflow via Directed Acyclic Graphs (DAGs) to easily manage complex combinations and options.


Key features:
- Minimal: 150 lines of code.
- Airflow-inspired syntax: use the ">>" operator to connect nodes in your day to easily create complex experiments.
- Customizable: Hadle experiments with different levels of complexity.
- Modular: Create nodes to organize shared configurations and reduce duplication.

# Installation
```
pip install hpdag
```

# Usage:

```python
from hpdag import DAG,Node,Branch
dataset = Node("dataset")
lr = Node("lr")
with DAG() as dag:
    datasets = Branch(
        dataset("the_pile") >> lr(0.001), #for example, one dataset might require specific settings than the others
        dataset( "c4") >> lr(0.01),
        )
    ablations = Branch( #do a type of ablation on each dataset
            Node("use_glu")(True,False), #run the experiment with and without the glu
            Node("positional_enc")("alibi","rotary"), #run the experiment with two different positional encodings
            )
    sizes = Node("size")("7b","3b") #run the experiment with two different sizes
    datasets >> ablations >>sizes
for task in dag.tasks:
    print(task)
print(task.params) #Access dictionary representing the task
```

Output:
```
Task(dataset=the_pile, lr=0.001, use_glu=True, size=7b)
Task(dataset=the_pile, lr=0.001, use_glu=True, size=3b)
Task(dataset=the_pile, lr=0.001, use_glu=False, size=7b)
Task(dataset=the_pile, lr=0.001, use_glu=False, size=3b)
Task(dataset=the_pile, lr=0.001, positional_enc=alibi, size=7b)
Task(dataset=the_pile, lr=0.001, positional_enc=alibi, size=3b)
Task(dataset=the_pile, lr=0.001, positional_enc=rotary, size=7b)
Task(dataset=the_pile, lr=0.001, positional_enc=rotary, size=3b)
Task(dataset=c4, lr=0.01, use_glu=True, size=7b)
Task(dataset=c4, lr=0.01, use_glu=True, size=3b)
Task(dataset=c4, lr=0.01, use_glu=False, size=7b)
Task(dataset=c4, lr=0.01, use_glu=False, size=3b)
Task(dataset=c4, lr=0.01, positional_enc=alibi, size=7b)
Task(dataset=c4, lr=0.01, positional_enc=alibi, size=3b)
Task(dataset=c4, lr=0.01, positional_enc=rotary, size=7b)
Task(dataset=c4, lr=0.01, positional_enc=rotary, size=3b)
{'dataset': 'c4', 'lr': 0.01, 'positional_enc': 'rotary', 'size': '3b'}
```
