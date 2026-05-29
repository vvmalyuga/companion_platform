terraform {
  required_version = ">= 1.6.0"
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = "~> 0.118"
    }
  }
}

provider "yandex" {
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
  zone      = var.zone
}

resource "yandex_storage_bucket" "lakehouse" {
  for_each = toset(["companion-bronze", "companion-silver", "companion-gold", "companion-ml", "companion-logs"])
  bucket   = each.key
  acl      = "private"
}

resource "yandex_vpc_network" "companion" {
  name = "companion-network"
}

resource "yandex_vpc_subnet" "companion" {
  name           = "companion-subnet"
  zone           = var.zone
  network_id     = yandex_vpc_network.companion.id
  v4_cidr_blocks = ["10.10.0.0/24"]
}


resource "yandex_vpc_security_group" "platform" {
  name       = "companion-platform-sg"
  network_id = yandex_vpc_network.companion.id

  dynamic "ingress" {
    for_each = toset(["22", "8080", "3000", "9092", "5432", "8123", "9000"])
    content {
      protocol       = "TCP"
      description    = "companion-${ingress.value}"
      v4_cidr_blocks = ["0.0.0.0/0"]
      port           = tonumber(ingress.value)
    }
  }

  egress {
    protocol       = "ANY"
    v4_cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "yandex_mdb_kafka_cluster" "companion" {
  name        = "companion-kafka"
  environment = "PRESTABLE"
  network_id  = yandex_vpc_network.companion.id

  config {
    version       = "3.5"
    brokers_count = 1
    zones         = [var.zone]

    kafka {
      resources {
        resource_preset_id = "s2.micro"
        disk_type_id       = "network-ssd"
        disk_size          = 10
      }
    }
  }
}

resource "yandex_mdb_kafka_topic" "topics" {
  for_each           = toset(["booking-events", "user-events", "chat-events", "companion-events", "analytics-events"])
  cluster_id         = yandex_mdb_kafka_cluster.companion.id
  name               = each.key
  partitions         = 3
  replication_factor = 1
}

resource "yandex_compute_instance" "platform" {
  name        = "companion-data-platform"
  platform_id = "standard-v3"

  resources {
    cores  = 2
    memory = 4
  }

  boot_disk {
    initialize_params {
      image_id = var.ubuntu_2204_image_id
      size     = 50
    }
  }

  network_interface {
    subnet_id          = yandex_vpc_subnet.companion.id
    nat                = true
    security_group_ids = [yandex_vpc_security_group.platform.id]
  }

  metadata = {
    user-data = templatefile("${path.module}/cloud-init.yaml", {
      ssh_user   = var.ssh_user
      public_key = var.public_key
    })
  }
}
