r"""
Use this module to write your answers to the questions in the notebook.

Note: Inside the answer strings you can use Markdown format and also LaTeX
math (delimited with $$).
"""

# ==============
# Part 2 answers


def part2_overfit_hp():
    wstd, lr, reg = 0, 0, 0
    # TODO: Tweak the hyperparameters until you overfit the small dataset.
    # ====== YOUR CODE: ======
    wstd = 0.1
    lr = 0.045
    reg = 0.001
    # ========================
    return dict(wstd=wstd, lr=lr, reg=reg)


def part2_optim_hp():
    wstd, lr_vanilla, lr_momentum, lr_rmsprop, reg, = 0, 0, 0, 0, 0

    # TODO: Tweak the hyperparameters to get the best results you can.
    # You may want to use different learning rates for each optimizer.
    # ====== YOUR CODE: ======
    wstd = 0.03
    lr_vanilla = 0.01
    lr_momentum = 0.01
    lr_rmsprop = 0.0005
    reg = 0.001
    # ========================
    return dict(wstd=wstd, lr_vanilla=lr_vanilla, lr_momentum=lr_momentum,
                lr_rmsprop=lr_rmsprop, reg=reg)


def part2_dropout_hp():
    wstd, lr, = 0, 0
    # TODO: Tweak the hyperparameters to get the model to overfit without
    # dropout.
    # ====== YOUR CODE: ======
    wstd = 0.001
    lr = 0.002
    # ========================
    return dict(wstd=wstd, lr=lr)


part2_q1 = r"""
**Your answer:**

1. As we expected, we managed to overfit over the data using no-dropout
since the training set wasn't big. Since we overfitted the data,
we got low test accuracy for no-dropout.
Using dropout, we were able to increase the model's generalization
and therefore get lower training accuracy, but higher test accuracy
(and better performance).

2. As we can see, as the dropout increases, the training accuracy goes lower,
while the test accuracy goes higher, but only to some point. As we can see in
the graph, the test accuracy of dropout=0.4 and dropout=0.8 are very similar,
but if we were going beyond 0.8, we would have gotten worse results on both
training set and test set, because we would have left with too small model. 

"""

part2_q2 = r"""
**Your answer:**

Yes. Cross Entropy Loss depends on other class scores than the true-class score.
Therefore, increasing other class scores (while maintaining the true-class score
the highest), will directly increase the loss. 
At the same time, we can have a different sample, which has two similar scores
one for the true-class and one for some other class. If they change values,
the loss will decrease by their diff. If that diff is small, we'll get 
a bit smaller loss, while getting higher accuracy. Therefore, it is possible that
the total loss will go higher while we get better results. Moreover,
even on the same sample it's possible to increase the loss, and at the same time
improve accuracy for that same sample (when combining the two explanations above - 
getting the right class while being less decisive over other classes).

"""
# ==============

# ==============
# Part 3 answers

part3_q1 = r"""
**Your answer:**


Write your answer using **markdown** and $\LaTeX$:
```python
# A code block
a = 2
```
An equation: $e^{i\pi} -1 = 0$

"""

part3_q2 = r"""
**Your answer:**


Write your answer using **markdown** and $\LaTeX$:
```python
# A code block
a = 2
```
An equation: $e^{i\pi} -1 = 0$

"""

part3_q3 = r"""
**Your answer:**


Write your answer using **markdown** and $\LaTeX$:
```python
# A code block
a = 2
```
An equation: $e^{i\pi} -1 = 0$

"""

part3_q4 = r"""
**Your answer:**


Write your answer using **markdown** and $\LaTeX$:
```python
# A code block
a = 2
```
An equation: $e^{i\pi} -1 = 0$

"""

part3_q5 = r"""
**Your answer:**


Write your answer using **markdown** and $\LaTeX$:
```python
# A code block
a = 2
```
An equation: $e^{i\pi} -1 = 0$

"""
# ==============
