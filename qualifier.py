import typing
from dataclasses import dataclass


@dataclass(frozen=True)
class Request:
    scope: typing.Mapping[str, typing.Any]
    receive: typing.Callable[[], typing.Awaitable[object]]
    send: typing.Callable[[object], typing.Awaitable[None]]


class RestaurantManager:
    def __init__(self):
        """Instantiate the restaurant manager.
        This is called at the start of each day before any staff get on
        duty or any orders come in. You should do any setup necessary
        to get the system working before the day starts here; we have
        already defined a staff dictionary.
        """
        self.staff = {}

    async def __call__(self, request: Request):
        """Handle a request received.
        This is called for each request received by your application.
        In here is where most of the code for your system should go.
        :param request: request object
            Request object containing information about the sent
            request to your application.
        """
        if request.scope['type'] == 'staff.onduty':
            self.staff[request.scope['id']] = request
        elif request.scope['type'] == 'staff.offduty':
            self.staff.pop(request.scope['id'])
        else:
            for key, value in self.staff.items():
                if request.scope['speciality'] in value.scope['speciality']:
                    selected_staff = self.staff[key]
                    break
            order = await request.receive()
            await selected_staff.send(order)
            await request.send(await selected_staff.receive())
