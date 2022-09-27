FROM quay.io/astronomer/astro-runtime:5.0.8
#COPY include/airflow-provider-ray tmp/airflow-provider-ray

#RUN python /usr/local/include/airflow-provider-ray/setup.py install

#ENV PYTHONPATH=/usr/local/airflow:/usr/local/airflow/dags

#USER root
#RUN python /usr/local/airflow/include/airflow-provider-ray/setup.py install
#USER root
#RUN pip uninstall astronomer-airflow-version-check -y
#USER astro
#ENV AIRFLOW__CORE__XCOM_BACKEND=ray_provider.xcom.ray_backend.RayBackend

