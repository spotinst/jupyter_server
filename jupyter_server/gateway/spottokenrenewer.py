import typing as ty

import logging
from jupyter_server.gateway.gateway_client import GatewayTokenRenewerBase, GatewayTokenRenewerMeta
import jupyter_server.base.handlers
import jupyter_server.serverapp


def get_header_value(request: ty.Any, header: str) -> str:
    if header not in request.headers:
        logging.error(f'Header "{header}" is missing')
        return ""
    logging.debug(f'Getting value from header "{header}"')
    value: str = request.headers[header]
    if len(value) == 0:
        logging.error(f'Header "{header}" is empty')
        return ""
    return value


class SpotTokenRenewer(GatewayTokenRenewerBase): # type:ignore[misc]

    def get_token(
            self,
            auth_header_key: str,
            auth_scheme: ty.Union[str, None],
            auth_token: str,
            **kwargs: ty.Any,
    ) -> str:
        request = jupyter_server.base.handlers.get_latest_request()
        if request is None:
            logging.error("Could not get current request")
            return auth_token

        auth_header_value = get_header_value(request, auth_header_key)
        if auth_header_value:
            try:
                # We expect the header value to be of the form "Bearer: XXX"
                auth_token = auth_header_value.split(" ", maxsplit=1)[1]
            except Exception as e:
                logging.error(f"Could not read token from auth header: {str(e)}")

        logging.info("Auth token refreshed")
        return auth_token
