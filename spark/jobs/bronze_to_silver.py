from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, to_timestamp, trim, lower


def normalizeBookings(frame: DataFrame) -> DataFrame:
    return (
        frame.dropDuplicates(["booking_id"])
        .withColumn("booking_date", to_timestamp("booking_date"))
        .withColumn("created_at", to_timestamp("created_at"))
        .withColumn("status", lower(trim(col("status"))))
        .filter(col("booking_id").isNotNull() & col("companion_id").isNotNull() & col("booking_date").isNotNull())
    )


def normalizeCompanions(frame: DataFrame) -> DataFrame:
    return frame.dropDuplicates(["companion_id"]).filter((col("age").between(18, 100)) & (col("price_per_hour") > 0))


def main() -> None:
    spark = SparkSession.builder.appName("companion-bronze-to-silver").config("spark.sql.catalog.companion", "org.apache.iceberg.spark.SparkCatalog").config("spark.sql.catalog.companion.type", "hadoop").config("spark.sql.catalog.companion.warehouse", "s3a://companion-silver/warehouse").getOrCreate()
    bookings = spark.read.parquet("s3a://companion-bronze/bookings/*")
    companions = spark.read.parquet("s3a://companion-bronze/companions/*")
    normalizeBookings(bookings).write.mode("overwrite").parquet("s3a://companion-silver/bookings")
    normalizeCompanions(companions).write.mode("overwrite").parquet("s3a://companion-silver/companions")
    spark.stop()


if __name__ == "__main__":
    main()
