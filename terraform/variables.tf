variable "cloud_id" {
  type = string
}

variable "folder_id" {
  type = string
}

variable "zone" {
  type    = string
  default = "ru-central1-a"
}

variable "ssh_user" {
  type    = string
  default = "ubuntu"
}

variable "public_key" {
  type = string
}

variable "ubuntu_2204_image_id" {
  type        = string
  description = "Ubuntu 22.04 image id from Yandex Cloud Marketplace"
}
