from datetime import datetime

import numpy as np
from scipy.stats import norm

from .option import OptionPricingModel

class BlackScholesMerton(OptionPricingModel):

    def __init__(self, instrument:str, option_type: str, spot_price: float, strike_price: float, risk_free_rate: float, sigma: float, dividend:float=0, days_to_maturity: float=None, start_date: datetime=None, end_date: datetime=None):
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

    @property
    def T(self) -> float:
        """
        Time to maturity (annualized)
        """
        return self._get_time_to_maturity(self.days_to_maturity, self.start_date, self.end_date)

    def _get_option_price(self) -> float:
        self._check_option_type(self.option_type)
        self._check_positive(self.T, 'Time to maturity')

        if self.option_type == 'put':
            return self.__put_option_price()
        else:
            return self.__call_option_price()

    def __get_d1_d2(self) -> tuple[float, float]:
        """
        
        """
        d1 = (np.log(self.S / self.K) + (self.r - self.dividend + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        
        return (d1, d1 - self.sigma * np.sqrt(self.T))

    def __call_option_price(self) -> float:
        """
        
        """
        d1, d2 = self.__get_d1_d2()

        return self.S * np.exp(-self.dividend * self.T) * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)

    def __put_option_price(self) -> float:
        """
        
        """
        d1, d2 = self.__get_d1_d2()

        return self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * np.exp(-self.dividend * self.T) * norm.cdf(-d1)
        