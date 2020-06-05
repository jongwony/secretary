resource "aws_lambda_permission" "event_lambda_permission" {
  statement_id  = "AllowAPIInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "event_poll"
  principal     = "apigateway.amazonaws.com"

  # The /*/*/* part allows invocation from any stage, method and resource path
  # within API Gateway REST API.
  source_arn = "${aws_api_gateway_rest_api.event_poll.execution_arn}/*/*/*"
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

resource "aws_api_gateway_integration" "event_lambda" {
  rest_api_id = aws_api_gateway_rest_api.event_poll.id
  resource_id = aws_api_gateway_method.event_method.resource_id
  http_method = aws_api_gateway_method.event_method.http_method

  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = aws_lambda_function.event_poll.invoke_arn
}

resource "aws_api_gateway_deployment" "event" {
  depends_on = [aws_api_gateway_integration.event_lambda]

  rest_api_id = aws_api_gateway_rest_api.event_poll.id
  stage_name = "default"
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

resource "aws_lambda_function" "event_message_changed" {
  function_name = "event_message_changed"
  description = "Secretary :: subtype message_changed from event_poll"

  filename = data.archive_file.project.output_path
  handler = "event_message_changed.lambda_handler"

  source_code_hash = data.archive_file.project.output_base64sha256
  runtime = "python3.8"
  timeout = 300

  role = aws_iam_role.secretary_for_lambda.arn
  layers = [
    aws_lambda_layer_version.secretary_package.arn,
    aws_lambda_layer_version.secretary_lib.arn
  ]
}

resource "aws_lambda_function" "event_bot_message" {
  function_name = "event_bot_message"
  description = "Secretary :: subtype bot_message from event_poll"

  filename = data.archive_file.project.output_path
  handler = "event_bot_message.lambda_handler"

  source_code_hash = data.archive_file.project.output_base64sha256
  runtime = "python3.8"
  timeout = 300

  role = aws_iam_role.secretary_for_lambda.arn
  layers = [
    aws_lambda_layer_version.secretary_package.arn,
    aws_lambda_layer_version.secretary_lib.arn
  ]
}
