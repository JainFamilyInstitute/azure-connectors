# azure-connectors
Python connectors for passwordless login to Azure storage services (SQL, ADLSv2, blob, tables), suitable for local and containerized projects.

## Overview
For compatibility with Container Apps and Azure Functions, settings are passed as environment variables. For local development, create or extend a `.env` file in the project root. For deployment, ensure that the environment variables are set in the app. Example settings are in the `example_envs` folder.

No environment variables should contain secrets!

## Authentication
Authentication to Azure services is passwordless, using Entra ID (aka Azure AD). For local development, specify 