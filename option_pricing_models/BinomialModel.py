from datetime import datetime

import numpy as np

from .option import OptionPricingModel

class BinomialModel(OptionPricingModel):

    def __init__(self, instrument:str, option_type: str, spot_price: float, strike_price: float, risk_free_rate: float, sigma: float, dividend:float=0, days_to_maturity: float=None, start_date: datetime=None, end_date: datetime=None, time_steps: int=1000):
        """
        
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
    
    @property
    def u(self) -> float: 
        """
        Asset price up factor (CRR model)
        """
        return np.exp(self.sigma * np.sqrt(self.dT))
    
    @property
    def d(self) -> float:
        """
        Asset price down factor (CRR model)
        """
        return np.exp(-self.sigma * np.sqrt(self.dT))
    
    @property
    def q(self) -> float:
        """
        Risk neutral up probability (down probability = 1 - q)
        """
        return (np.exp((self.r - self.dividend) * self.dT) - self.d) / (self.u - self.d)
    
    def _get_option_price(self) -> float:
        self._check_option_type(self.option_type)

        if self.option_type == 'put':
            return self.__put_option_price()
        else:
            return self.__call_option_price()

    def __asset_price_tree(self) -> np.array:
        """
        
        """
        self._check_positive(self.time_steps, 'Time steps')

        # Price at maturity
        S_T = np.array( [self.S * self.u**i * self.d**(self.time_steps - i) for i in range(self.time_steps + 1)] )
        return S_T

    def __call_option_price(self) -> float:
        """
        
        """
        # Initialize price vector
        V = np.zeros(self.time_steps + 1)

        # Option value at maturity T
        V[:] = np.maximum(self.__asset_price_tree() - self.K, 0)

        # Calculate option value at each time step
        for i in range(self.time_steps - 1, -1, -1):
            V[:-1] = np.exp(-self.r * self.dT) * (self.q * V[1:] + (1 - self.q) * V[:-1])
        
        return V[0]

    def __put_option_price(self) -> float:
        """
        
        """
        # Initialize price vector
        V = np.zeros(self.time_steps + 1)

        # Option value at maturity T
        V[:] = np.maximum(self.K - self.__asset_price_tree(), 0)

        # Calculate option value at each time step
        for i in range(self.time_steps - 1, -1, -1):
            V[:-1] = np.exp(-self.r * self.dT) * (self.q * V[1:] + (1 - self.q) * V[:-1])
        
        return V[0]