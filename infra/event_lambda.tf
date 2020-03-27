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

resource "aws_lambda_permission" "lambda_permission" {
  statement_id  = "AllowAPIInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "event_poll"
  principal     = "apigateway.amazonaws.com"

  # The /*/*/* part allows invocation from any stage, method and resource path
  # within API Gateway REST API.
  source_arn = "${aws_api_gateway_rest_api.event_poll.execution_arn}/*/*/*"
}

resource "aws_iam_role_policy_attachment" "admin_access" {
  role = aws_iam_role.secretary_for_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

resource "aws_lambda_layer_version" "secretary_package" {
  layer_name = "secretary_package"
  filename = data.archive_file.package.output_path
  source_code_hash = data.archive_file.package.output_base64sha256
  compatible_runtimes = ["python3.8"]
}

resource "aws_lambda_layer_version" "secretary_lib" {
  layer_name = "secretary_lib"
  filename = data.archive_file.lib.output_path
  source_code_hash = data.archive_file.lib.output_base64sha256
  compatible_runtimes = ["python3.8"]
}

resource "aws_lambda_function" "event_poll" {
  function_name = "event_poll"
  description = "Secretary :: Slack Event Polling"

  filename = data.archive_file.project.output_path
  handler = "event_poll.lambda_handler"

  source_code_hash = data.archive_file.project.output_base64sha256
  runtime = "python3.8"
  timeout = 300

  role = aws_iam_role.secretary_for_lambda.arn
  layers = [
    aws_lambda_layer_version.secretary_package.arn,
    aws_lambda_layer_version.secretary_lib.arn
  ]
}

resource "aws_api_gateway_rest_api" "event_poll" {
  name = "event_poll"
  description = "Slack :: Event Subscription"
}

resource "aws_api_gateway_resource" "event_resource" {
  rest_api_id = aws_api_gateway_rest_api.event_poll.id
  parent_id = aws_api_gateway_rest_api.event_poll.root_resource_id
  path_part = "event_poll"
}

resource "aws_api_gateway_method" "event_method" {
  rest_api_id = aws_api_gateway_rest_api.event_poll.id
  resource_id = aws_api_gateway_resource.event_resource.id
  http_method = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id = aws_api_gateway_rest_api.event_poll.id
  resource_id = aws_api_gateway_method.event_method.resource_id
  http_method = aws_api_gateway_method.event_method.http_method

  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = aws_lambda_function.event_poll.invoke_arn
}

resource "aws_api_gateway_deployment" "event" {
  depends_on = [aws_api_gateway_integration.lambda]

  rest_api_id = aws_api_gateway_rest_api.event_poll.id
  stage_name = "default"
}
