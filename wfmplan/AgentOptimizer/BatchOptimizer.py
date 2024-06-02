import pandas as pd
from .Optimizer import Optimizer

class BatchOptimizer:
    def __init__(self, df: pd.DataFrame, operational_targets: dict):
        self.df = df
        self.operational_targets = operational_targets

    def calculate_interval(self, start_time, end_time):
        return (end_time - start_time).total_seconds()

    def run_optimization(self):
        results = []

        for index, row in self.df.iterrows():
            exp_vol = row['exp_vol']
            aht = row['exp_aht']
            interval_start_time = row['interval_start']
            interval_end_time = row['interval_end']
            
            interval = self.calculate_interval(interval_start_time, interval_end_time)
            
            optimizer = Optimizer(
                exp_vol=exp_vol,
                aht=aht,
                interval=interval,
                **self.operational_targets
            )
            result = optimizer.predict()
            result.update({
                'interval_start': interval_start_time,
                'interval_end': interval_end_time,
                'exp_vol': exp_vol,
                'exp_aht': aht
            })  # Include input data in results
            results.append(result)

        results_df = pd.DataFrame(results)
        columns_order = ['interval_start', 'interval_end', 'exp_vol', 'exp_aht'] + \
                        [col for col in results_df.columns if col not in ['interval_start', 'interval_end', 'exp_vol', 'exp_aht']]
        results_df = results_df[columns_order]

        return results_df
