output "vm_public_ip" {
  value = yandex_compute_instance.platform.network_interface[0].nat_ip_address
}

output "bucket_names" {
  value = keys(yandex_storage_bucket.lakehouse)
}

output "kafka_topics" {
  value = keys(yandex_mdb_kafka_topic.topics)
}
