import sys
import logging

from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql import functions as F


INPUT_PATH = "s3://amazon-reviews-pds/parquet/product_category=Books/*.parquet"
OUTPUT_PATH = sys.argv[1]


def create_spark_session() -> SparkSession:
    """Create spark session.

    Returns:
        spark (SparkSession) - spark session connected to AWS EMR
            cluster
    """
    spark = SparkSession.builder.config(
        "spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0"
    ).getOrCreate()
    return spark


def extract_book_data(spark: SparkSession, input_path: str) -> DataFrame:
    """ Read in book review data source from S3 bucket

    Arguments:
        spark (SparkSession): spark session connected to AWS EMR
            cluster
        input_path (str): AWS S3 bucket path for source data

    Returns:
        df (DataFrame): A Spark DataFrame extracted from the source data
    """
    df = spark.read.parquet(input_path)
    return df


def transform_book_data(df: DataFrame) -> DataFrame:
    """Process the book review data and write to S3.

    Arguments:
        df (DataFrame): A Spark DataFrame from the source

    Returns:
        df (DataFrame): A Spark DataFrame after applying transformation
    """
    # Apply some basic filters and aggregate by product_title.
    book_agg = (
        df.filter(df.verified_purchase == "Y")
        .groupBy("product_title")
        .agg({"star_rating": "avg", "review_id": "count"})
        .filter(F.col("count(review_id)") >= 500)
        .sort(F.desc("avg(star_rating)"))
        .select(
            F.col("product_title").alias("book_title"),
            F.col("count(review_id)").alias("review_count"),
            F.col("avg(star_rating)").alias("review_avg_stars"),
        )
    )

    return book_agg


def load_data(df: DataFrame, output_path: str) -> None:
    """Load the aggregated book revie data into a S3 bucket

    Arguments
        output_path (str) - AWS S3 bucket for writing processed data
    """
    df.write.mode("overwrite").save(output_path)


def main():
    logging.basicConfig(level=logging.INFO)
    spark = create_spark_session()
    logging.info("Extract book review data from source {}".format(INPUT_PATH))
    data_extracted = extract_book_data(spark, INPUT_PATH)
    logging.info("Transforming book review data")
    data_transformed = transform_book_data(data_extracted)
    logging.info("Loading book review data to target: {}".format(OUTPUT_PATH))
    load_data(data_transformed, OUTPUT_PATH)


if __name__ == "__main__":
    sys.exit(main())
