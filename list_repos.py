import logging

from airflow.operators.python import PythonOperator
from airflow.providers.github.operators.github import GithubOperator
from airflow.providers.github.sensors.github import GithubSensor, GithubTagSensor
from airflow.models import DAG, Connection, Variable

from datetime import datetime, timedelta
from pprint import pprint

doc = """###The third task is expected to fail
          ### The first and second are expected to succeed
          ### To run this dag you first need to create a personal access token on github and 
          ### Then add that personal access token as a connection in airflow
          ### Once this is done you can run this dag
        """

def get_reposs(user):
    logged = logging.info(list(user.get_repos()))
    return [pprint(i) for i in logged]

with DAG(
    dag_id="list_gh_repos_try1",
    start_date=datetime(2022, 7, 7),
    schedule=timedelta(days=60),
    tags=["githubian"]
) as dag:

    list_repos = GithubOperator(
        tas    doc_md=doc,hub_method="get_user",
        github_method_args={},
        result_processor=lambda user: pprint((list(user.get_repos()))),
        # result_processor=get_reposs("tronlightracer"),
    )

    get_repo = GithubOperator(
        task_id="gh_get_singular_repo",
        github_method="get_user",
        github_method_args={},
        result_processor=lambda user: pprint(user.get_repo("spectrogram_fun"))
    )

    get_lang = GithubOperator(
        task_id="gh_get_repo_by_lang",
        github_method="get_user",
        github_method_args={},
        result_processor=lambda user: pprint(user.get_repos(query='language:shell'))
    )

list_repos >> get_repo >> get_lang

# logging.info(list(user.get_repos()))