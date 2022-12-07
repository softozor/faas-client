# faas-client

A simple wrapper around [faas-cli](https://docs.openfaas.com/cli/install/).

## Usage

```python
faas_port = 8080
faas_client_factory = FaasClientFactory(faas_port)
username = "the-username"
password = "the-password"
hostname = "the-hostname"
faas_client = faas_client_factory.create(hostname, username, password)
faas_client.login()
faas_client.build("faas.yml", "my-function")
```
