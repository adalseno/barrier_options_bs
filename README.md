# Barrier options using closed formula

## Analytical formula

from: https://www.asc.tuwien.ac.at/~juengel/simulations/fincalculator/doc/Barrier.pdf (see Hull page 604)

$$\lambda = \frac {r-q + \sigma^2/2}{\sigma^2}, \quad y = \frac {\ln{(H^2/S_0K)}}{\sigma\sqrt{T}}+\lambda \sigma\sqrt{T}$$

$$ x_1 = \frac {\ln({S_0/H})}{\sigma\sqrt{T}}+\lambda\sigma\sqrt{T}, \quad y_1= \frac {\ln({H/S_0})}{\sigma\sqrt{T}}+\lambda\sigma\sqrt{T}$$

## Price for Call option
### Down-and-Out (and Down-and-In)

When $H\ge K$:

$$
\begin{equation}
\begin{split}
c_{do} = & S_0 N(x_1)e^{-qT}\\
& - K e^{-rT} N(x_1 - \sigma\sqrt{T})\\
& - S_0 e^{-qT} (H/S_0)^{2\lambda} N(y_1)\\
& + K e^{-rT} (H/S_0)^{2\lambda -2} N(y_1 - \sigma\sqrt{T})
\end{split}
\end{equation}
$$

$$ c_{di} = c-c_{do}$$

When $H\le K$:

$$
\begin{equation}
\begin{split}
c_{di} = & S_0 e^{-qT} (H/S_0)^{2\lambda} N(y)\\
& - K e^{-rT} (H/S_0)^{2\lambda -2} N(y - \sigma\sqrt{T})
\end{split}
\end{equation}
$$

$$ c_{do} = c-c_{di}$$



### Up-and-ot (and Up-and-In)

When $ H\ge K$:

$$ 
\begin{equation}
\begin{split}
c_{ui} & = S_0 N(x_1)e^{-qT}\\
& -Ke^{-rT}N(x_1- \sigma \sqrt{T}) \\
& -S_0e^{-qT} (H/S_0)^{2\lambda} [N(-y)-N(-y_1)]\\
& +Ke^{-rT}(H/S_0)^{2\lambda-2} [N(-y+\sigma\sqrt{T})-N(-y_1+\sigma\sqrt{T})] 
\end{split}
\end{equation}$$

$$ c_{uo} = c-c_{ui}$$

If $H\le K \rightarrow c_{uo}= 0, \quad c_{ui}=c$


## Price for Put Option
### Up-and_ot (and Up-and-In)

When $H\ge K$:

$$
\begin{equation}
\begin{split}
p_{ui} = & -S_0 e^{-qT} (H/S_0)^{2\lambda} N(-y)\\
& + K e^{-rT} (H/S_0)^{2\lambda -2} N(-y + \sigma\sqrt{T})
\end{split}
\end{equation}
$$

$$ p_{uo} = p-p_{ui}$$

When $ H\le K$:

$$ 
\begin{equation}
\begin{split}
p_{ui} & = -S_0 N(-x_1)e^{-qT}\\
& +Ke^{-rT}N(-x_1+ \sigma \sqrt{T}) \\
& +S_0e^{-qT} (H/S_0)^{2\lambda} N(-y_1)\\
& -Ke^{-rT}(H/S_0)^{2\lambda-2} N(-y_1+\sigma\sqrt{T})
\end{split}
\end{equation}$$

$$ p_{uo} = p-p_{ui}$$

### Down-and-Out (and Down-and-In) Put
When $H > K \rightarrow p_{do}=0,\quad p_{di} = p$.

Whem $H\le K$:

$$ 
\begin{equation}
\begin{split}
p_{di} & = -S_0 N(-x_1)e^{-qT}\\
& +Ke^{-rT}N(-x_1+ \sigma \sqrt{T}) \\
& +S_0e^{-qT} (H/S_0)^{2\lambda} [N(y)-N(y_1)]\\
& -Ke^{-rT}(H/S_0)^{2\lambda-2} [N(y-\sigma\sqrt{T})-N(y_1-\sigma\sqrt{T})] 
\end{split}
\end{equation}$$

$$ p_{do} = p-p_{di}$$

### Example usage 

Case $H\ge K$:

    bs_barrier(120,120,8/12,0.06,0.3,150)

    {'cui': 12.28,
     'cuo': 1.69,
     'cdi': 13.97,
     'cdo': 0,
     'pui': 0.34,
     'puo': 8.93,
     'pdi': 9.27,
     'pdo': 0}


![barrier_h_more_k](https://user-images.githubusercontent.com/2405291/203375771-e93a08d5-b85b-447b-b3ae-c1d939a7e936.png)

Case $H\le K$:

    bs_barrier(120,120,8/12,0.06,0.3,100)

    {'cui': 13.97,
     'cuo': 0,
     'cdi': 0.97,
     'cdo': 13.0,
     'pui': 9.27,
     'puo': 0,
     'pdi': 8.5,
     'pdo': 0.77}


![barrier_h_less_k](https://user-images.githubusercontent.com/2405291/203375876-588037a1-8275-4ee8-ba9d-f5695f177354.png)

Images from http://www.coggit.com/freetools
