from pyspark.sql import SparkSession

from src.utils import create_spark_session


def test_create_spark_session_with_app_name():
    app_name = "test-spark-session"
    spark = create_spark_session(app_name)

    assert isinstance(spark, SparkSession)
    assert spark.conf.get("spark.app.name") == app_name


def test_create_spark_session_with_master():
    master = "local[2]"
    spark_default = create_spark_session().conf.get("spark.master")
    spark_with_master = create_spark_session(master=master).conf.get("spark.master")

    assert spark_default == "local[*]"
    assert spark_with_master == master
