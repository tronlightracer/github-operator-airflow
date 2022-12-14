FROM quay.io/astronomer/astro-runtime:6.0.2
RUN pip install apache-airflow-providers-ssh==3.3.0
RUN pip install apache-airflow-providers-github==2.2.0