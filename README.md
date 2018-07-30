# zabbix-jolokia

This is a module to query a jolokia endpoint with some optional domains/beans to filter the output.

The result will be a json structure of key value pairs where the keys are flattened and made zabbix key compatible.

This module is intended to be used with zabbix-sidecar
