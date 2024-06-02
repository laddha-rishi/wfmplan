import pandas as pd
from math import ceil, exp, log
from scipy.special import loggamma


class Optimizer:
    # Unit: time in seconds
    def __init__(self, exp_vol: float, aht: float, interval: int, max_occupancy: float = 1.0, shrink=0.0, asa=None, sla=None, st=None, method='asa', patience: float = None, **kwargs):
        self.validate_inputs(exp_vol, aht, interval, max_occupancy, shrink, asa, sla, st, method) # data validation

        self.exp_vol = exp_vol
        self.aht = aht
        self.asa = asa
        self.sla = sla
        self.st = st
        self.interval = interval
        self.shrink = shrink
        self.max_occupancy = max_occupancy
        self.method = method
        self.patience = patience

    def validate_inputs(self, exp_vol, aht, interval, max_occupancy, shrink, asa, sla, st, method):
        if method == 'asa' and asa is None:
            raise ValueError("Please provide 'asa' targets because the optimization method selected is 'asa'( by default)")

        if method == 'sla' and (sla is None or st is None):
            raise ValueError("Please provide 'sla' and 'st' targets because the optimization method selected is 'sla'")

        if exp_vol <= 0:
            raise ValueError("Number of transactions must be greater than 0")

        if aht <= 0:
            raise ValueError("Average handling time must be greater than 0")

        if asa is not None and asa <= 0:
            raise ValueError("Average speed of answer must be greater than 0")

        if sla is not None and sla <= 0:
            raise ValueError("Service Level Agreement (SLA) must be greater than 0")

        if st is not None and st <= 0:
            raise ValueError("Service Target (ST) must be greater than 0")

        if interval <= 0:
            raise ValueError("Interval must be greater than 0")

        if not 0 <= shrink < 1:
            raise ValueError("Shrinkage must be in the range [0, 1)")

        if max_occupancy < 0 or max_occupancy > 1:
            raise ValueError("max_occupancy must be between 0 and 1")

    def prob_waiting(self, traffic_intensity, num_agents):
        if num_agents <= traffic_intensity:
            return 1  # If number of agents is less than or equal to traffic intensity, the probability of waiting is 1

        try:
            log_numerator = num_agents * log(traffic_intensity) - loggamma(num_agents + 1) + log(num_agents)
            log_denominator = log(num_agents - traffic_intensity)
            x = exp(log_numerator - log_denominator)

            y = 1
            for i in range(round(num_agents)):
                y += exp(i * log(traffic_intensity) - loggamma(i + 1))
            prob = x / (y + x)
        except OverflowError:
            prob = 1  # Fallback to 1 in case of overflow

        return prob

    def sla_optimization(self, prob_waiting, num_agents):
        try:
            result = 1 - (prob_waiting * exp(-((num_agents - self.intensity) * (self.st / self.aht))))
        except OverflowError:
            result = 0  # Fallback to 0 in case of overflow
        return result

    def asa_optimization(self, prob_waiting, num_agents):
        try:
            avg_wait_time_in_queue = (prob_waiting * self.aht) / (num_agents - self.intensity)
        except ZeroDivisionError:
            avg_wait_time_in_queue = float('inf')  # Fallback to infinity in case of division by zero
        return avg_wait_time_in_queue

    def predict(self):
        try:
            self.intensity = (self.exp_vol / self.interval) * self.aht  # arrival rate / service rate ~ typical server or resource usage during a given time
            n = ceil(max(self.intensity, 1))  # minimum number of agents required to attend at 100% occupancy without SLA/ASA target
            if n <= self.intensity:
                n = self.intensity + 1
            prob_waiting = self.prob_waiting(self.intensity, n)  # initializing values without optimal solution

            if self.method == 'sla':
                sla_calc = self.sla_optimization(prob_waiting, n)  # initializing values without optimal solution
                while sla_calc < self.sla:
                    n += 1
                    prob_waiting = self.prob_waiting(self.intensity, n)
                    sla_calc = self.sla_optimization(prob_waiting, n)

            elif self.method == 'asa':
                asa_calc = self.asa_optimization(prob_waiting, n)  # initializing values without optimal solution
                while asa_calc > self.asa:
                    n += 1
                    prob_waiting = self.prob_waiting(self.intensity, n)
                    asa_calc = self.asa_optimization(prob_waiting, n)

            process_occupancy = (self.intensity / n)

            if process_occupancy > self.max_occupancy:
                n = ceil(self.intensity / self.max_occupancy)

            prob_waiting = self.prob_waiting(self.intensity, n)
            average_speed_of_answer = (prob_waiting * self.aht) / (n - self.intensity)

            percent_calls_answered_immediately = (1 - prob_waiting)
            occupancy = (self.intensity / n)
            n_shrinkage = n / (1 - self.shrink)

            return {
                'agent_req': int(n),
                'agent_req_shrink': ceil(n_shrinkage),
                'pred_occupancy': round(occupancy, 2),
                'prob_waiting': prob_waiting,
                **({'pred_sla': round((self.sla_optimization(prob_waiting, n) * 100), 2), 'pred_st': round(average_speed_of_answer, 1)} if self.method == 'sla' else {}),
                **({'pred_asa': round(average_speed_of_answer, 1)} if self.method == 'asa' else {})
            }

        except Exception as e:
            print(f"Error occurred: {e}")
            print(f"Values -> exp_vol: {self.exp_vol}, intensity: {self.intensity}, n: {n}")
            return {}

