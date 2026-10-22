"""External systems: ports and adapters.

For each row in docs/02-integrations.md with v1 mode = fake:

- app/integrations/<system>.py
    class <Capability>Port(Protocol): ...      # contract the services depend on
    class Fake<System>Adapter: ...             # in-process fake mirroring the real contract
    def get_<capability>() -> <Capability>Port # picks the adapter from settings.integrations_mode
- If the real system calls us back asynchronously (webhooks), the fake simulates it:
  a route in app/integrations/mock_providers.py schedules a BackgroundTask that sends the
  event over HTTP to OUR real inbound route — the production code path is exercised.
"""
