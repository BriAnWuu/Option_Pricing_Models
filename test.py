from datetime import date

# from option_pricing_models.vanilla import BlackScholesMerton, BinomialModel, MonteCarloSimulation

from option_pricing_models import Vanilla, American

instrument = 'AAPL'
option_type = 'put'
spot = 95
strike = 100
rate = 0.03
sigma = 0.2
dividend = 0.01
t = 30
start = date(2024, 1, 13)
# start = None
end = date(2024, 2, 13)
time_steps = 1000
simulations = 100_000


BSM = Vanilla.BlackScholesMerton(
    instrument, 
    option_type,
    spot,
    strike, 
    rate,
    sigma,
    dividend,
    None,
    start,
    end
)

print('Black Scholes Merton:\n', BSM.option_price())


BT = Vanilla.BinomialModel(
    instrument, 
    option_type,
    spot,
    strike, 
    rate,
    sigma,
    dividend,
    None,
    start,
    end,
    time_steps
)

print('Binomial Tree:\n', BT.option_price())


MC = Vanilla.MonteCarloSimulation(
    instrument, 
    option_type,
    spot,
    strike, 
    rate,
    sigma,
    dividend,
    None,
    start,
    end,
    time_steps,
    simulations
)

# print('Monte Carlo:\n', MC.option_price())

American_BT = American.BinomialModel(
    instrument, 
    option_type,
    spot,
    strike, 
    rate,
    sigma,
    dividend,
    None,
    start,
    end,
    time_steps
)

print('American Binomial:\n', American_BT.option_price())