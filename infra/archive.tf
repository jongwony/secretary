data "external" "package_hash" {
  program = [
    "../scripts/hash_checksum.py",
    "../requirements.txt"
  ]
}

data "external" "package" {
  program = [
    "../scripts/create_package.sh",
    "../data/secretary_package",
    "../requirements.txt"
  ]
}

resource "null_resource" "package" {
  triggers = {
    hash = data.external.package_hash.result.hash
  }
}

data "archive_file" "package" {
  type        = "zip"
  source_dir = data.external.package.result.source_dir
  output_path = data.external.package.result.filename

  depends_on = [
    null_resource.package
  ]
}

data "external" "lib_hash" {
  program = [
    "../scripts/hash_checksum.py",
    "../lib"
  ]
}

data "external" "lib" {
  program = [
    "../scripts/create_custom_layer.sh",
    "../data/secretary_lib",
    "../lib"
  ]
  query = {
  }
}

resource "null_resource" "lib" {
  triggers = {
    hash = data.external.lib_hash.result.hash
  }
}

data "archive_file" "lib" {
  type        = "zip"
  source_dir = data.external.lib.result.source_dir
  output_path = data.external.lib.result.filename

  depends_on = [
    null_resource.lib
  ]
}

data "archive_file" "project" {
  type = "zip"
  source_dir = "../lambda"
  output_path = var.project_zip
}
