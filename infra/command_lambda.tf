resource "aws_lambda_permission" "command_lambda_permission" {
  statement_id  = "AllowAPIInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "command_poll"
  principal     = "apigateway.amazonaws.com"

  # The /*/*/* part allows invocation from any stage, method and resource path
  # within API Gateway REST API.
  source_arn = "${aws_api_gateway_rest_api.command_poll.execution_arn}/*/*/*"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lambda_function" "command_poll" {
  function_name = "command_poll"
  description = "Secretary :: Slack Command Polling"

  filename = data.archive_file.project.output_path
  handler = "command_poll.lambda_handler"

  source_code_hash = data.archive_file.project.output_base64sha256
  runtime = "python3.9"
  timeout = 300

  role = aws_iam_role.secretary_for_lambda.arn
  layers = [
    aws_lambda_layer_version.secretary_package.arn,
    aws_lambda_layer_version.secretary_lib.arn
  ]
}

resource "aws_api_gateway_rest_api" "command_poll" {
  name = "command_poll"
  description = "Slack :: Command Action"
}

resource "aws_api_gateway_resource" "command_resource" {
  rest_api_id = aws_api_gateway_rest_api.command_poll.id
  parent_id = aws_api_gateway_rest_api.command_poll.root_resource_id
  path_part = "command_poll"
}

resource "aws_api_gateway_method" "command_method" {
  rest_api_id = aws_api_gateway_rest_api.command_poll.id
  resource_id = aws_api_gateway_resource.command_resource.id
  http_method = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "command_lambda" {
  rest_api_id = aws_api_gateway_rest_api.command_poll.id
  resource_id = aws_api_gateway_method.command_method.resource_id
  http_method = aws_api_gateway_method.command_method.http_method

  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = aws_lambda_function.command_poll.invoke_arn
}

resource "aws_api_gateway_deployment" "command" {
  depends_on = [aws_api_gateway_integration.command_lambda]

  rest_api_id = aws_api_gateway_rest_api.command_poll.id
  stage_name = "default"
}
