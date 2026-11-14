
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

default_args = {
    'owner': 'retailpulse',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def check_drift():
    # In production, this queries the Evidently AI metric or database
    print("Checking data drift via Evidently AI...")
    # If drift_score > 0.30, return True to trigger next task
    return True 

def retrain_model():
    print("Triggering model retraining script...")
    subprocess.run(["python", "scripts/retrain_churn_model.py"])

def register_model():
    print("Registering new model version in MLflow...")

with DAG(
    'retailpulse_churn_retraining',
    default_args=default_args,
    description='Automated retraining pipeline based on drift detection',
    schedule_interval='@daily',
    catchup=False,
) as dag:

    task_check_drift = PythonOperator(
        task_id='check_data_drift',
        python_callable=check_drift,
    )

    task_retrain = PythonOperator(
        task_id='retrain_churn_model',
        python_callable=retrain_model,
    )

    task_register = PythonOperator(
        task_id='register_new_model',
        python_callable=register_model,
    )

    # Define the order of execution
    task_check_drift >> task_retrain >> task_register
