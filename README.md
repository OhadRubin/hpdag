# hpdag

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
print(dag)
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
```
