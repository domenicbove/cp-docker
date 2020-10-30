class FilterModule(object):
    def filters(self):
        return {
            'normalize_authentication': self.normalize_authentication,
            'kafka_protocol_normalized': self.kafka_protocol_normalized,
            'kafka_protocol': self.kafka_protocol,
            'kafka_client_properties': self.kafka_client_properties
        }

    def normalize_authentication(self, authentication):
        # Returns standardized value for an authentication
        normalized = 'GSSAPI' if authentication.lower() == 'kerberos' \
            else 'SCRAM-SHA-512' if authentication.upper() == 'SCRAM' \
            else 'PLAIN' if authentication.upper() == 'PLAIN' \
            else 'OAUTHBEARER' if authentication.upper() == 'OAUTH' \
            else 'none'
        return normalized

    def kafka_protocol_normalized(self, authentication_normalized, tls_enabled):
        # Joins a normalized authentication and tls setting to return a kafka protocol
        kafka_protocol = 'SASL_SSL' if tls_enabled == True and authentication_normalized in ['GSSAPI', 'PLAIN', 'SCRAM-SHA-512', 'OAUTHBEARER'] \
            else 'SASL_PLAINTEXT' if tls_enabled == False and authentication_normalized in ['GSSAPI', 'PLAIN', 'SCRAM-SHA-512', 'OAUTHBEARER'] \
            else 'SSL' if tls_enabled == True and authentication_normalized == 'none' \
            else 'PLAINTEXT'
        return kafka_protocol

    def kafka_protocol(self, tls_enabled, authentication):
        # Joins an authentication and tls setting to return a kafka protocol
        authentication_normalized = self.normalize_authentication(authentication)
        kafka_protocol = self.kafka_protocol_normalized(authentication_normalized, tls_enabled)
        return kafka_protocol

    def kafka_client_properties(self, config_prefix, tls_enabled, authentication,
            truststore_location, truststore_password, keystore_location, keystore_password, key_password):
        # Returns client properties given listener requirements
        final_dict = {
            config_prefix + 'SECURITY_PROTOCOL': self.kafka_protocol(tls_enabled, authentication)
        }
        if tls_enabled:
            final_dict[config_prefix + 'SSL_TRUSTSTORE_LOCATION'] = truststore_location
            final_dict[config_prefix + 'SSL_TRUSTSTORE_PASSWORD'] = truststore_password
        if authentication == 'mtls':
            final_dict[config_prefix + 'SSL_KEYSTORE_LOCATION'] = keystore_location
            final_dict[config_prefix + 'SSL_KEYSTORE_PASSWORD'] = keystore_password
            final_dict[config_prefix + 'SSL_KEY_PASSWORD'] = key_password

        return final_dict

    # def get_sasl_mechanisms(self, listeners_dict, default_sasl_protocol):
    #     # Loops over listeners dictionary and returns list of sasl mechanisms
    #     mechanisms = []
    #     for listener in listeners_dict:
    #         sasl_protocol = listeners_dict[listener].get('sasl_protocol', default_sasl_protocol)
    #         mechanisms = mechanisms + [self.normalize_sasl_protocol(sasl_protocol)]
    #     return mechanisms

    # def get_hostnames(self, listeners_dict, default_hostname):
    #     # Loops over listeners dictionary and returns all hostnames attached to a listener
    #     hostnames = []
    #     for listener in listeners_dict:
    #         hostname = listeners_dict[listener].get('hostname', default_hostname)
    #         hostnames = hostnames + [hostname]
    #     return hostnames

    # def cert_extension(self, hostnames):
    #     # Joins a list of hostnames to be added to SAN of certificate
    #     extension = 'dns:'+",dns:".join(hostnames)
    #     return extension

    # def ssl_required(self, listeners_dict, default_tls_enabled):
    #     # Loops over listeners dictionary and returns True if any have TLS encryption enabled
    #     ssl_required = False
    #     for listener in listeners_dict:
    #         ssl_enabled = listeners_dict[listener].get('ssl_enabled', default_tls_enabled)
    #         ssl_required = ssl_required == True or ssl_enabled == True
    #     return ssl_required
