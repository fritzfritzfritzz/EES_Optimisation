import pulp
import numpy as np

def decompose_demand_after_solar(demand_after_solar: np.ndarray):
    '''
    Takes demand_after_solar, which is the sum of the demand/consumption of the client
    and the solar generation.
    Decomposes it into the positive demand (demand if demand > solar generation else 0) &
    solar surplus (0 if demand >= solar generation else -(demand - solar generation))
    '''
    positive_demand = np.where(demand_after_solar > 0, demand_after_solar, 0)
    solar_surplus = np.where(demand_after_solar < 0, -demand_after_solar, 0)
    return positive_demand, solar_surplus

def optimize_charging_schedule(price: np.ndarray,
                            demand_after_solar: np.ndarray,
                            state_of_charge: float,
                            capacity: float,
                            charging_efficiency: float,
                            discharging_efficiency: float,
                            charging_power: float,
                            discharging_power: float,
                            window: int = 96) -> np.ndarray: #window default of 96 matches a day in 15 min time steps (4*24)
    '''
    The `optimize_charging_schedule` function is solving an optimization problem to determine the optimal
    charging and discharging strategy for a battery system. Time series data has to be passed in 15 min resolution!
    Otherwise changes to the capacity must be applied. 

        Args:
            price (numpy.ndarray): array containing electricity prices in 15 min resolution -> [currency/kWh]
            demand after solar generation (numpy.ndarray): array containing the left-over demand after solar generation has been subtracted (can be negative if there is a solar surplus) in 15 min resolution -> [kW]
            capacity (float): battery capacity -> [kWh]
            charging_efficiency and discharging_efficiency (both float):
            charging_power and discharging_power (both float):
            window (float): default = 96 -> 4 * 24 15-min time steps during a day

        Returns:
            optimal_charging_schedule (numpy.ndarray): array containing the optimized charge-discharge decisions for the time span specified by window argument
            status: 
        
    '''
    #check if provided arrays are long enough for chosen window size
    if len(price) < window or len(demand_after_solar) < window:
        raise ValueError("Length of 'price' or 'demand_after_solar' is not equal or greater than 'window'.")
    #check if state_of_charge is some value between 0 and 1
    if not 0 <= state_of_charge <= 1:
        raise ValueError("Value of 'state_of_charge' is not element of range[0,1]")
    
    # convert capacity from kWh to kWh/4
    capacity = capacity * 4

    #decompose demand_after_solar
    positive_demand, solar_surplus = decompose_demand_after_solar(demand_after_solar)

    # Create the Linear Programming problem instance
    prob = pulp.LpProblem("BatterySchedule", pulp.LpMaximize)

    ## Define decision variables
    # We differentiate between charging and discharging, since they might have differing constraints on power and efficiency
    # They are therefore both positive -> lowBound = 0 and cannot be larger than their respective power -> upBound
    charge = pulp.LpVariable.dicts("Charge", range(window), lowBound=0, upBound=charging_power)
    discharge = pulp.LpVariable.dicts("Discharge", range(window), lowBound=0, upBound=discharging_power)
    # The State Of Charge (SOC) indicated the relative charge compared to the total capacity of the battery in %
    # Since we start with an additional initial SOC[0] its length is window + 1
    soc = pulp.LpVariable.dicts("SOC", range(window+1), lowBound=0, upBound=1)
    # We introduce solar as a separate variable since it can be used to charge the battery without being part of the objective function (price of solar = 0)
    solar = pulp.LpVariable.dicts("Solar surplus", range(window), lowBound=0)

    # Set the objective function
    # This function is maximized by the algorithm
    prob += pulp.lpSum(price[t] * discharge[t] - price[t] * charge[t] for t in range(window))
    
    # Set initial SOC
    prob += soc[0] == state_of_charge
    
    # Set constraints
    for t in range(window):
        # Battery state update
        # Running at charge[t] kW for 15 mins results in charge[t] kWh/4 increase in stored energy
        prob += soc[t+1] == soc[t] + (charging_efficiency * (charge[t] + solar[t]) - discharge[t] * (1/discharging_efficiency))*(1/(capacity))

        # Power constraints
        # Solar constraint, i.e. cannot use more solar than what is available from the surplus
        prob += solar[t] <= solar_surplus[t]
        prob += solar[t] + charge[t] <= charging_power #power constraint for discharge is already given when declaring the discharge variable with upBound=discharge_power
        prob += discharge[t] <= positive_demand[t] # We are not selling back to the grid, so we can only discharge as much as can be used by the demand
    
    # Solve the problem
    status = prob.solve(pulp.GLPK(msg = 0))

    # solution status
    #print("Status:", pulp.LpStatus[status])
    status_msg = pulp.LpStatus[status]

    # Print the optimal values of variables
    #for var in prob.variables():
    #    print(var.name, "=", var.varValue)
    
    # optimal objective value
    #print("Optimal value =", pulp.value(prob.objective))
    objective_value = pulp.value(prob.objective)

    # Retrieve the optimal solution
    optimal_buy = np.array([pulp.value(charge[t]) for t in range(window)])
    optimal_sell = np.array([pulp.value(discharge[t]) for t in range(window)])
    optimal_charge = np.array([pulp.value(charge[t]) + pulp.value(solar[t]) for t in range(window)])
    optimal_soc = np.array([pulp.value(soc[t]) for t in range(window)])

    return optimal_charge, optimal_buy, optimal_sell, optimal_soc, objective_value, status_msg