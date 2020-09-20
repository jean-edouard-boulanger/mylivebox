# mylivebox

(Non-official) pure Python API that allows access [Livebox](https://en.wikipedia.org/wiki/Orange_Livebox) data and
perform basic operations.

## Basic usage

```python
from mylivebox import Livebox, BasicCredentials
livebox = Livebox(BasicCredentials("admin", "123456789"))
print(livebox.wan_status)
```

```json
{
    "WanState": "up",
    "LinkType": "dsl",
    "LinkState": "up",
    "MACAddress": "44:A6:1E:51:06:E5",
    "Protocol": "dhcp",
    "ConnectionState": "Bound",
    "LastConnectionError": "None",
    "IPAddress": "86.225.151.244",
    "RemoteGateway": "86.225.144.1",
    "DNSServers": "80.10.246.7,81.253.149.14",
    "IPv6Address": "2a01:cb0d:27c:f600:46a6:1eff:fe51:6e5",
    "IPv6DelegatedPrefix": "2a01:cb0d:27c:f600::/56"
}
```