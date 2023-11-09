#!/usr/bin/env python3
""" Check response
"""

if __name__ == "__main__":
    from api.v1.auth.auth import Auth

    a = Auth()
    res = a.require_auth("/api/v1/status/", ["/api/v1/status/"])
    if res:
        print("require_auth must return False")
        exit(1)
    print("OK", end="")
