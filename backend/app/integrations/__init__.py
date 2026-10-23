"""External capabilities: ports and adapters (D-01).

For each row in the capability register (docs/03-architecture.md) with v0 = fake:

- app/integrations/<capability>.py
    class <Capability>Port(Protocol): ...      # contract the services depend on — named after
                                               # the capability, never after a vendor
    class Fake<Capability>Adapter: ...         # in-process fake mirroring the contract shape
    def get_<capability>() -> <Capability>Port # picks the adapter from settings.integrations_mode
- If the real system calls us back asynchronously (webhooks), the fake simulates it:
  a route in app/integrations/mock_providers.py schedules a BackgroundTask that sends the
  event over HTTP to OUR real inbound route — the production code path is exercised.
- Real vendor adapters arrive with v1, once the vendor decision is accepted in decisions.md.
"""
