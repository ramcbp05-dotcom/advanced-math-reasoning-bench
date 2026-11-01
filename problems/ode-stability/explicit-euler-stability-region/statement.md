# The explicit Euler stability region

## Assumptions

Apply the explicit (forward) Euler method $y_{n+1} = y_n + h f(t_n, y_n)$ to
the **Dahlquist test equation**

$$y' = \lambda y, \qquad \lambda \in \mathbb{C}, \ \operatorname{Re}\lambda < 0,
\qquad y(0) = y_0 .$$

The exact solution $y(t) = y_0e^{\lambda t}$ satisfies $|y(t)| \to 0$.

A one-step method is **absolutely stable** for a given $h\lambda$ if its
numerical solution also satisfies $|y_n| \to 0$. Its **region of absolute
stability** is $\{z = h\lambda \in \mathbb{C} : |R(z)| \le 1\}$, where $y_{n+1}
= R(z)y_n$.

## Part 1

Show $R(z) = 1 + z$ for explicit Euler and deduce that the stability region is

$$\boxed{\ \{z \in \mathbb{C} : |1 + z| \le 1\}\ }$$

the closed disc of radius 1 centred at $-1$. For real $\lambda < 0$, show this
is exactly

$$0 < h \le \frac{2}{|\lambda|}.$$

## Part 2

Consider the stiff system

$$y_1' = -\lambda_{\text{fast}}\,y_1, \qquad
  y_2' = -\lambda_{\text{slow}}\,y_2, \qquad \lambda_{\text{fast}} = 10^{6},\
  \lambda_{\text{slow}} = 1 ,$$

integrated to $t = 10$. What step size does accuracy require for $y_2$? What
step size does *stability* require? Compute the number of steps forced by each.

## Part 3

The **local truncation error** of explicit Euler is $\tfrac12h^2y''(\xi)$: it
is $O(h^2)$ for every $h$, with no threshold. Reconcile this with the fact that
the method fails catastrophically for $h|\lambda| > 2$.

State precisely what quantity has a threshold and what quantity does not.

## Part 4

State what changes for the **implicit** Euler method $y_{n+1} = y_n +
hf(t_{n+1}, y_{n+1})$: compute its $R(z)$ and its stability region, and say
what it costs.

## What a complete answer contains

1. $R(z)$ derived for both methods and both regions described geometrically.
2. The two step counts in Part 2, as numbers.
3. A precise statement in Part 3: not "the error grows", but which error and by
   what factor.
