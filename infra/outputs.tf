output "event_invoke_url" {
  value = "${aws_api_gateway_deployment.event.invoke_url}${aws_api_gateway_resource.event_resource.path}"
}
