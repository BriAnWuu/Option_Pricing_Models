from datetime import datetime

import numpy as np

from ..option import OptionPricingModel

class MonteCarloSimulation(OptionPricingModel):

    def __init__(self, instrument:str, option_type: str, spot_price: float, strike_price: float, risk_free_rate: float, sigma: float, dividend:float=0, days_to_maturity: float=None, start_date: datetime=None, end_date: datetime=None, time_steps: int=1000, simulations: int=100_000):
        """
        Longstaff Schwartz Monte Carlo
        """
        self.instrument = instrument
        self.option_type = option_type.lower()
        self.S = spot_price
        self.K = strike_price
        self.r = risk_free_rate
        self.sigma = sigma
        self.dividend = dividend # dividend yield %
        self.days_to_maturity = days_to_maturity
        self.start_date = start_date
        self.end_date = end_date
        self.time_steps = time_steps
        self.simulations = simulations

    @property
    def T(self) -> float:
        """
        Time to maturity (annualized)
        """
        return self._get_time_to_maturity(self.days_to_maturity, self.start_date, self.end_date)

    @property
    def dT(self) -> float:
        """
        Delta T
        """
        self._check_positive(self.T, 'Time to maturity')
        return self.T / self.time_steps

    def _get_option_price(self) -> float:
        self._check_option_type(self.option_type)

        if self.option_type == 'put':
            return self.__put_option_price()
        else:
            return self.__call_option_price()
    
    def __simulate_asset_price(self) -> np.array:
        """
        assume risk-neutral world and underlying asset follows Geometric Brownian Motion
        """
        self._check_positive(self.time_steps, 'Time steps')
        self._check_positive(self.simulations, 'Number of simulations')

        # Initialize price vector, dimension: (time steps, number of simulations)
        S_t = np.zeros((self.time_steps + 1, self.simulations))

        # Set spot price at t = 0
        S_t[0] = self.S

        np.random.seed(123)
        for i in range(1, self.time_steps + 1):

            # ST = St * exp[(drift) + sigma * sqrt(dT) * diffusion]
            S_t[i] = S_t[i-1] * np.exp((self.r - self.dividend - 0.5 * self.sigma**2) * self.dT + self.sigma * np.sqrt(self.dT) * np.random.normal(size=self.simulations))

        return S_t[-1]

    def __call_option_price(self) -> float:
        """
        
        """
        return np.exp(-self.r * self.T) * np.sum(np.maximum(self.__simulate_asset_price() - self.K, 0)) / self.simulations

    def __put_option_price(self) -> float:
        """
        
        """
        return np.exp(-self.r * self.T) * np.sum(np.maximum(self.K - self.__simulate_asset_price(), 0)) / self.simulations