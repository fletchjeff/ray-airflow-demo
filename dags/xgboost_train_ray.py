from airflow.decorators import dag

from datetime import datetime
from ray_provider.decorators.ray_decorators import ray_task

default_args = {"owner": "airflow"}
task_args = {"ray_conn_id": "ray_cluster_connection"}

@dag(
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2022, 9, 21),
    tags=["xgboost-pandas-only"],
    catchup=False,
)
def xgboost_train_ray():
    @ray_task(**task_args)
    def get_breast_cancer_data():
        import ray
        dataset = ray.data.read_csv("s3://anonymous@air-example-data/breast_cancer.csv")
        train_dataset, valid_dataset = dataset.train_test_split(test_size=0.3)
        return train_dataset, valid_dataset

    @ray_task(**task_args)
    def train_breast_cancer(data):
        from ray.air.config import ScalingConfig
        from ray.train.xgboost import XGBoostTrainer
        scaling_config = ScalingConfig(
            num_workers=2,
            use_gpu=False,
        )
        train_dataset, valid_dataset = data
        trainer = XGBoostTrainer(
            scaling_config=scaling_config,
            label_column="target",
            num_boost_round=20,
            params={
                "objective": "binary:logistic",
                "eval_metric": ["logloss", "error"],
            },
            datasets={"train": train_dataset, "valid": valid_dataset},
        )
        result = trainer.fit()
        print(result.metrics)
        return result.metrics

    breast_cancer_data = get_breast_cancer_data()
    model_results = train_breast_cancer(breast_cancer_data)

xgboost_train_ray = xgboost_train_ray()

 