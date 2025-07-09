---
name: "Test Windsurf Cascade Integration"
description: "A test workflow to verify the BMAD integration with Windsurf Cascade. This workflow performs basic operations to ensure the environment is properly configured."
tags:
  - test
  - test-windsurf-integration
---

# Test Windsurf Cascade Integration

## Workflow Metadata

- **ID:** test-windsurf-integration
- **Type:** test
- **Project Types:** 

## Description

A test workflow to verify the BMAD integration with Windsurf Cascade. This workflow performs basic operations to ensure the environment is properly configured.

## Workflow Steps

### environment_check

- **Agent:** system
- **Action:** check_environment
- **Notes:**
  Verify that the Windsurf Cascade environment is properly configured:
  - Check for required tools and dependencies
  - Verify file system access
  - Check network connectivity

### create_test_files

- **Agent:** windsurf-cascade-agent
- **Action:** create_test_files
- **Notes:**
  Create test files to verify file system operations:
  - Create a test directory structure
  - Generate sample files
  - Verify file creation

### code_generation_test

- **Agent:** windsurf-cascade-agent
- **Action:** generate_test_code
- **Notes:**
  Test code generation capabilities:
  - Generate a simple function
  - Create a test case
  - Verify the generated code

### documentation_test

- **Agent:** windsurf-cascade-agent
- **Action:** generate_documentation
- **Notes:**
  Test documentation generation:
  - Generate API documentation
  - Create a README file
  - Verify documentation format

### cleanup

- **Agent:** system
- **Action:** cleanup_test_files
- **Notes:**
  Clean up test files and temporary data:
  - Remove test directories
  - Clean up any temporary files
  - Verify cleanup

## Hooks

### Pre_Execution Hooks

- **setup_environment**
  - Script: `scripts/test/setup.sh`


### Post_Execution Hooks

- **generate_report**
  - Script: `scripts/test/generate_report.sh`

