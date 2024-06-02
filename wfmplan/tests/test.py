import pandas as pd
from ..AgentOptimizer import Optimizer,BatchOptimizer


def test_Optimizer():
    agent_requirement=Optimizer(exp_vol=1000,aht=500,interval=3600,max_occupancy=0.95,shrink=0.3,asa=30,st=30,sla=0.95,patience=120,method='sla')
    agent_requirement.predict()

def test_BatchOptimizer():
    df = pd.DataFrame({
        'volume_expected': [1000, 1500, 2000],
        'avg_handle_time': [300, 200, 250],
        'start_time': pd.to_datetime(['2024-06-01 08:00:00', '2024-06-01 09:00:00', '2024-06-01 10:00:00']),
        'end_time': pd.to_datetime(['2024-06-01 09:00:00', '2024-06-01 10:00:00', '2024-06-01 11:00:00'])
    })
    operational_targets = {
        'max_occupancy': 0.9,
        'shrink': 0.1,
        'asa': 20,
        'method': 'asa'
    }
    batch_optimizer = BatchOptimizer(df, operational_targets)
    result_df = batch_optimizer.run_optimization()
    result_df

if __name__ == '__main__':
    test_Optimizer()
    test_BatchOptimizer()

