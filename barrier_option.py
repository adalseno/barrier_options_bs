import numpy as np
import scipy.stats as ss 

def bs_option(
    S0: float, K: float, T: float, r: float, sigma: float, option_type: str
) -> tuple[float, dict]:
    """
    Compute European Option price and Greeks according to Black & Scholes model
    for non -dividend paying options

    Parameters:
    S0: float # spot price
    K: float # Strike price
    T: float # maturity in years
    r: float # free risk rate
    sigma: float # annualized volatility
    option_type: str # Type of option: C for Call and P for Put

    return option_price: float, Greeks: dict[float]
    """
    # Check option type
    if option_type.upper() not in ["C", "P"]:
        raise ValueError(f"Option type must be C or P, not {option_type}")

    # Local variables
    ds = np.exp(-r * T)  # discount rate
    sigma_t = sigma * np.sqrt(T)  # for conveninece
    mu = r + 0.5 * np.power(sigma, 2)  # mu

    # Compute d1 and d2
    d1 = (np.log(S0 / K) + mu * T) / sigma_t
    d2 = d1 - sigma_t

    # Greeks dict
    greeks = {}

    if option_type.upper() == "C":  # Call

        Opt_Price = S0 * ss.norm.cdf(d1) - K * ds * ss.norm.cdf(d2)

        greeks["Delta"] = ss.norm.cdf(d1)
        greeks["Gamma"] = ss.norm.pdf(d1) / (S0 * sigma_t)
        greeks["Vega"] = S0 * ss.norm.pdf(d1) * np.sqrt(T)
        greeks["Theta"] = -(S0 * ss.norm.pdf(d1) * sigma) / (
            2 * np.sqrt(T)
        ) - r * K * sigma_t * ss.norm.cdf(d2)
        greeks["Rho"] = K * T * ds * ss.norm.cdf(d2)

    else:  # Put

        Opt_Price = K * ds * ss.norm.cdf(-d2) - S0 * ss.norm.cdf(-d1)

        greeks["Delta"] = -ss.norm.cdf(-d1)
        greeks["Gamma"] = ss.norm.pdf(d1) / (S0 * sigma * np.sqrt(T))
        greeks["Vega"] = S0 * ss.norm.pdf(d1) * np.sqrt(T)
        greeks["Theta"] = -(S0 * ss.norm.pdf(d1) * sigma) / (
            2 * np.sqrt(T)
        ) + r * K * ds * ss.norm.cdf(-d2)
        greeks["Rho"] = -K * T * ds * ss.norm.cdf(-d2)

    # Round return values
    Opt_Price = np.round(Opt_Price, 2)

    for k, v in greeks.items():
        greeks[k] = np.round(v, 4)

    return Opt_Price, greeks
  
 def bs_barrier(
    S0: float, K: float, T: float, r: float, sigma: float, H: float, q: float = 0
) -> dict[float]:
    """
    Compute varrier option prices according to
    Black & Scholes closed formula

    Parameters:

    S0: float # spot price of the asset
    K: float # the strike price
    T.float # time, in year
    r: float # free risk rate
    sigma: float # annualized volatility
    H: float # the barrier value
    q:float # dividend if any
    return dict{float} # option prices
    """

    sigma_t = sigma * np.sqrt(T)  # for convenience

    # Compute lambda and y
    la = (r - q + np.power(sigma, 2) / 2) / np.power(sigma, 2)
    y = (np.log(np.power(H, 2) / (S0 * K))) / sigma_t + (la * sigma_t)

    # Compute x1 and y1
    x1 = np.log(S0 / H) / sigma_t + la * sigma_t
    y1 = np.log(H / S0) / sigma_t + la * sigma_t

    # Create return dict
    ret_val = {
        "cui": -1,
        "cuo": -1,
        "cdi": -1,
        "cdo": -1,
        "pui": -1,
        "puo": -1,
        "pdi": -1,
        "pdo": -1,
    }

    # Compute Vanilla prices
    c = bs_option(S0, K, T, r, sigma, "C")[0]  # Call price
    p = bs_option(S0, K, T, r, sigma, "P")[0]  # Put price

    if H >= K:
        # Compute values for Call
        # DAO - DAI
        cdo = max(
            (
                S0 * np.exp(-q * T) * ss.norm.cdf(x1)
                - K * np.exp(-r * T) * ss.norm.cdf(x1 - sigma_t)
                - S0 * np.exp(-q * T) * np.power(H / S0, 2 * la) * ss.norm.cdf(y1)
                + K
                * np.exp(-r * T)
                * np.power(H / S0, 2 * la - 2)
                * ss.norm.cdf(y1 - sigma_t)
            ),
            0,
        )
        cdi = c - cdo

        # UAO, UAI
        cui = max(
            (
                S0 * np.exp(-q * T) * ss.norm.cdf(x1)
                - K * np.exp(-r * T) * ss.norm.cdf(x1 - sigma_t)
                - S0
                * np.exp(-q * T)
                * np.power(H / S0, 2 * la)
                * (ss.norm.cdf(-y) - ss.norm.cdf(-y1))
                + K
                * np.exp(-r * T)
                * np.power(H / S0, 2 * la - 2)
                * (ss.norm.cdf(-y + sigma_t) - ss.norm.cdf(-y1 + sigma_t))
            ),
            0,
        )
        cuo = c - cui

        # Compute values for put
        # UAO, UAI
        pui = max(
            (
                -S0 * np.exp(-q * T) * np.power(H / S0, 2 * la) * ss.norm.cdf(-y)
                + K
                * np.exp(-r * T)
                * np.power(H / S0, 2 * la - 2)
                * ss.norm.cdf(-y + sigma_t)
            ),
            0,
        )
        puo = p - pui

        # DAO, DAI
        pdo = 0
        pdi = p

    else:
        # Call
        # DAO, DAI
        cdi = max(
            (
                S0 * np.exp(-q * T) * np.power(H / S0, 2 * la) * ss.norm.cdf(y)
                - K
                * np.exp(-r * T)
                * np.power(H / S0, 2 * la - 2)
                * ss.norm.cdf(y - sigma_t)
            ),
            0,
        )
        cdo = c - cdi

        # UOA, UAI
        cuo = 0
        cui = c - cuo

        # Put
        # UAO, UAI
        puo = max(
            (
                -S0 * np.exp(-q * T) * ss.norm.cdf(-x1)
                + K * np.exp(-r * T) * ss.norm.cdf(-x1 + sigma_t)
                - S0 * np.exp(-q * T) * np.power(H / S0, 2 * la) * ss.norm.cdf(-y)
                - K
                * np.exp(-r * T)
                * np.power(H / S0, 2 * la - 2)
                * ss.norm.cdf(-y1 + sigma_t)
            ),
            0,
        )
        pui = p - puo

        # DAO, DAI
        pdi = max(
            (
                -S0 * np.exp(-q * T) * ss.norm.cdf(-x1)
                + K * np.exp(-r * T) * ss.norm.cdf(-x1 + sigma_t)
                + S0
                * np.exp(-q * T)
                * np.power(H / S0, 2 * la)
                * (ss.norm.cdf(y) - ss.norm.cdf(y1))
                - K
                * np.exp(-r * T)
                * np.power(H / S0, 2 * la - 2)
                * (ss.norm.cdf(y - sigma_t) - ss.norm.cdf(y1 - sigma_t))
            ),
            0,
        )
        pdo = p - pdi

    # Set return values rounded at two decimal places
    ret_val["cdi"] = np.round(cdi, 2)
    ret_val["cdo"] = np.round(cdo, 2)
    ret_val["cui"] = np.round(cui, 2)
    ret_val["cuo"] = np.round(cuo, 2)
    ret_val["pui"] = np.round(pui, 2)
    ret_val["puo"] = np.round(puo, 2)
    ret_val["pdi"] = np.round(pdi, 2)
    ret_val["pdo"] = np.round(pdo, 2)

    return ret_val
  
  
