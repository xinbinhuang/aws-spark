from pyspark.sql import SparkSession


def create_spark_session(
    name: str = "SparkShell", master: str = "local[*]"
) -> SparkSession:
    """Create a Spark Session

    :param name: Name of the Spark Application
    :param master: Spark master URL. Default local mode using all the threads available
    :return: A contructed SparkSession
    """
    spark = SparkSession.builder.appName(name).master(master).getOrCreate()
    return spark
