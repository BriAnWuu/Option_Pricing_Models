from abc import ABC, abstractmethod

class OptionPricingModel(ABC):

    def option_price(self) -> float:
        return self._get_option_price()
    
    @classmethod
    @abstractmethod
    def _get_option_price(self) -> float:
        """
        Calculate option price
        """
        pass
    
    @staticmethod
    def _get_time_to_maturity(days_to_maturity, start_date, end_date) -> float:
        if start_date and end_date:
            return (end_date - start_date).days / 365
        
        elif days_to_maturity:
            return days_to_maturity / 365

        else:
            raise ValueError('Error in fetching time_to_maturity data. Both start_date and end_date must be valid, or days_to_maturity must be entered.')

    @staticmethod
    def _check_positive(parameter: float, message='') -> None:
        if parameter < 0:
            raise ValueError(message + ' must be non-negative.')
        
    @staticmethod
    def _check_option_type(option_type: str) -> None:
        if option_type not in ('call', 'put'):
            raise ValueError('Option type should be either "call" or "put"')