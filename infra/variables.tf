variable "create_package_script" {
  type = string
  default = "../scripts/create_package.sh"
}

variable "create_custom_layer_script" {
  type = string
  default = "../scripts/create_custom_layer.sh"
}

variable "package_layer_zip" {
  type = string
  default = "../data/secretary_package.zip"
}

variable "lib_layer_zip" {
  type = string
  default = "../data/secretary_lib.zip"
}

variable "project_zip" {
  type = string
  default = "../data/secretary.zip"
}
