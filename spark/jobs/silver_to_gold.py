from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import avg, col, count, countDistinct, expr, sum as spark_sum


def buildTopCompanions(bookings: DataFrame, companions: DataFrame) -> DataFrame:
    metrics = bookings.groupBy("companion_id").agg(count("booking_id").alias("booking_count"), avg("rating").alias("avg_rating"), spark_sum("amount").alias("revenue"))
    return metrics.join(companions, "companion_id", "left").orderBy(col("avg_rating").desc(), col("booking_count").desc())


def buildBusinessAggregates(bookings: DataFrame) -> DataFrame:
    return bookings.agg(
        countDistinct("customer_id").alias("active_users"),
        count("booking_id").alias("booking_count"),
        avg("rating").alias("average_rating"),
        (spark_sum(expr("case when status = 'completed' then 1 else 0 end")) / count("booking_id")).alias("booking_conversion"),
    )


def buildFeatureFrames(bookings: DataFrame) -> tuple[DataFrame, DataFrame]:
    userFeatures = bookings.groupBy("customer_id").agg(count("booking_id").alias("total_bookings"), avg("rating").alias("avg_rating_given"), countDistinct("category").alias("preferred_categories"), countDistinct(expr("to_date(booking_date)")).alias("active_days"))
    companionFeatures = bookings.groupBy("companion_id").agg(avg("rating").alias("avg_rating"), count("booking_id").alias("booking_frequency"), (spark_sum(expr("case when status = 'cancelled' then 1 else 0 end")) / count("booking_id")).alias("cancellation_rate"))
    return userFeatures, companionFeatures


def main() -> None:
    spark = SparkSession.builder.appName("companion-silver-to-gold").getOrCreate()
    bookings = spark.read.parquet("s3a://companion-silver/bookings")
    companions = spark.read.parquet("s3a://companion-silver/companions")
    buildTopCompanions(bookings, companions).write.mode("overwrite").parquet("s3a://companion-gold/top_companions")
    buildBusinessAggregates(bookings).write.mode("overwrite").parquet("s3a://companion-gold/business_metrics")
    userFeatures, companionFeatures = buildFeatureFrames(bookings)
    userFeatures.write.mode("overwrite").parquet("s3a://companion-ml/user_features")
    companionFeatures.write.mode("overwrite").parquet("s3a://companion-ml/companion_features")
    spark.stop()


if __name__ == "__main__":
    main()
