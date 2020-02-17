# Changelog

## 1.1.0
  * Added a logging config file to fallback to in case LOGGING_CONF_FILE env variable is not defined. This is to 
  respect the singer specs that requires the logs to be sent to stderr and not stdout.

## 1.0.0
  * Initial version (fork of https://github.com/singer-io/singer-python version 5.9.0)
