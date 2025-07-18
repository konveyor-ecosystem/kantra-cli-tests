"""This module defines project-level constants."""

# env variables
KANTRA_CLI_PATH = "KANTRA_CLI_PATH"
REPORT_OUTPUT_PATH = "REPORT_OUTPUT_PATH"
PROJECT_PATH = "PROJECT_PATH"
GIT_USERNAME = "GIT_USERNAME"
GIT_PASSWORD = "GIT_PASSWORD"
ASSET_GENERATION_OUTPUT = "ASSET_GENERATION_OUTPUT"

# YAML RULE SCHEMA
CUSTOM_RULE_YAML_SCHEMA = """
type: array
items:
  type: object
  properties:
    category:
      type: string
    customVariables:
      type: array
      items:
        type: object
    description:
      type: string
    effort:
      type: number
    labels:
      type: array
      items:
        type: string
    links:
      type: array
      items:
        type: object
        properties:
          title:
            type: string
          url:
            type: string
    message:
      type: string
    ruleID:
      type: string
    when:
      type: object
      properties:
        java.referenced:
          type: object
          properties:
            location:
              type: string
            pattern:
              type: string
"""
