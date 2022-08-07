resource "aws_iam_role" "secretary_for_lambda" {
  name = "secretary_for_lambda"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": [
          "lambda.amazonaws.com",
          "s3.amazonaws.com",
          "apigateway.amazonaws.com"
        ]
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "admin_access" {
  role = aws_iam_role.secretary_for_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

resource "aws_lambda_layer_version" "secretary_package" {
  layer_name = "secretary_package"
  filename = data.archive_file.package.output_path
  source_code_hash = data.archive_file.package.output_base64sha256
  compatible_runtimes = ["python3.10"]
}

resource "aws_lambda_layer_version" "secretary_lib" {
  layer_name = "secretary_lib"
  filename = data.archive_file.lib.output_path
  source_code_hash = data.archive_file.lib.output_base64sha256
  compatible_runtimes = ["python3.10"]
}

