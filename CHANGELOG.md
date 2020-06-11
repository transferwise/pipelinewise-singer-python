# Changelog

## 1.1.3 (2020-06-11)
  * Bump jsonschema to 3.2.0

## 1.1.2 (2020-04-29)
  * Bump pytz to 2020.1

## 1.1.1 (2020-03-19)
  * Bump pytz to 2019.3

## 1.1.0 (2020-02-17)
  * Added a logging config file to fallback to in case LOGGING_CONF_FILE env variable is not defined. This is to 
  respect the singer specs that requires the logs to be sent to stderr and not stdout.

## 1.0.0 (2020-02-06)
  * Initial version (fork of https://github.com/singer-io/singer-python version 5.9.0)
