import google.protobuf.message
import modal._resolver
import modal.client
import typing
import typing_extensions

O = typing.TypeVar("O", bound="_Object")

_BLOCKING_O = typing.TypeVar("_BLOCKING_O", bound="Object")

class _Object:
    _type_prefix: typing.ClassVar[typing.Union[str, None]]
    _prefix_to_type: typing.ClassVar[typing.Dict[str, type]]
    _load: typing.Union[typing.Callable[[O, modal._resolver.Resolver, typing.Union[str, None]], typing.Awaitable[None]], None]
    _preload: typing.Union[typing.Callable[[O, modal._resolver.Resolver, typing.Union[str, None]], typing.Awaitable[None]], None]
    _object_id: str
    _client: modal.client._Client
    _is_hydrated: bool

    @classmethod
    def __init_subclass__(cls, type_prefix: typing.Union[str, None] = None):
        ...

    def __init__(self):
        ...

    def _init(self, rep: str, load: typing.Union[typing.Callable[[O, modal._resolver.Resolver, typing.Union[str, None]], typing.Awaitable[None]], None] = None, is_persisted_ref: bool = False, preload: typing.Union[typing.Callable[[O, modal._resolver.Resolver, typing.Union[str, None]], typing.Awaitable[None]], None] = None):
        ...

    def _unhydrate(self):
        ...

    def _initialize_from_empty(self):
        ...

    def _hydrate(self, object_id: str, client: modal.client._Client, metadata: typing.Union[google.protobuf.message.Message, None]):
        ...

    def _hydrate_metadata(self, metadata: google.protobuf.message.Message):
        ...

    def _get_metadata(self) -> typing.Union[google.protobuf.message.Message, None]:
        ...

    def _init_from_other(self, other: O):
        ...

    @classmethod
    def _from_loader(cls, load: typing.Callable[[O, modal._resolver.Resolver, typing.Union[str, None]], typing.Awaitable[None]], rep: str, is_persisted_ref: bool = False, preload: typing.Union[typing.Callable[[O, modal._resolver.Resolver, typing.Union[str, None]], typing.Awaitable[None]], None] = None):
        ...

    @classmethod
    def _new_hydrated(cls: typing.Type[O], object_id: str, client: modal.client._Client, handle_metadata: typing.Union[google.protobuf.message.Message, None]) -> O:
        ...

    @classmethod
    async def from_id(cls: typing.Type[O], object_id: str, client: typing.Union[modal.client._Client, None] = None) -> O:
        ...

    async def _hydrate_from_app(self, app_name: str, tag: typing.Union[str, None] = None, namespace=1, client: typing.Union[modal.client._Client, None] = None, environment_name: typing.Union[str, None] = None):
        ...

    def _hydrate_from_other(self, other: O):
        ...

    def __repr__(self):
        ...

    @property
    def local_uuid(self):
        ...

    @property
    def object_id(self):
        ...

    def is_hydrated(self) -> bool:
        ...

    async def _deploy(self, label: str, namespace=1, client: typing.Union[modal.client._Client, None] = None, environment_name: typing.Union[str, None] = None) -> None:
        ...

    def persist(self, label: str, namespace=1, environment_name: typing.Union[str, None] = None):
        ...

    def _persist(self, label: str, namespace=1, environment_name: typing.Union[str, None] = None):
        ...

    @classmethod
    def from_name(cls: typing.Type[O], app_name: str, tag: typing.Union[str, None] = None, namespace=1, environment_name: typing.Union[str, None] = None) -> O:
        ...

    @classmethod
    async def lookup(cls: typing.Type[O], app_name: str, tag: typing.Union[str, None] = None, namespace=1, client: typing.Union[modal.client._Client, None] = None, environment_name: typing.Union[str, None] = None) -> O:
        ...

    @classmethod
    async def _exists(cls: typing.Type[O], app_name: str, tag: typing.Union[str, None] = None, namespace=1, client: typing.Union[modal.client._Client, None] = None) -> bool:
        ...


class Object:
    _type_prefix: typing.ClassVar[typing.Union[str, None]]
    _prefix_to_type: typing.ClassVar[typing.Dict[str, type]]
    _load: typing.Union[typing.Callable[[_BLOCKING_O, modal._resolver.Resolver, typing.Union[str, None]], None], None]
    _preload: typing.Union[typing.Callable[[_BLOCKING_O, modal._resolver.Resolver, typing.Union[str, None]], None], None]
    _object_id: str
    _client: modal.client.Client
    _is_hydrated: bool

    def __init__(self):
        ...

    @classmethod
    def __init_subclass__(cls, type_prefix: typing.Union[str, None] = None):
        ...

    class ___init_spec(typing_extensions.Protocol):
        def __call__(self, rep: str, load: typing.Union[typing.Callable[[_BLOCKING_O, modal._resolver.Resolver, typing.Union[str, None]], None], None] = None, is_persisted_ref: bool = False, preload: typing.Union[typing.Callable[[_BLOCKING_O, modal._resolver.Resolver, typing.Union[str, None]], None], None] = None):
            ...

        def aio(self, rep: str, load: typing.Union[typing.Callable[[_BLOCKING_O, modal._resolver.Resolver, typing.Union[str, None]], typing.Awaitable[None]], None] = None, is_persisted_ref: bool = False, preload: typing.Union[typing.Callable[[_BLOCKING_O, modal._resolver.Resolver, typing.Union[str, None]], typing.Awaitable[None]], None] = None):
            ...

    _init: ___init_spec

    def _unhydrate(self):
        ...

    def _initialize_from_empty(self):
        ...

    def _hydrate(self, object_id: str, client: modal.client.Client, metadata: typing.Union[google.protobuf.message.Message, None]):
        ...

    def _hydrate_metadata(self, metadata: google.protobuf.message.Message):
        ...

    def _get_metadata(self) -> typing.Union[google.protobuf.message.Message, None]:
        ...

    def _init_from_other(self, other: _BLOCKING_O):
        ...

    @classmethod
    def _from_loader(cls, load: typing.Callable[[_BLOCKING_O, modal._resolver.Resolver, typing.Union[str, None]], None], rep: str, is_persisted_ref: bool = False, preload: typing.Union[typing.Callable[[_BLOCKING_O, modal._resolver.Resolver, typing.Union[str, None]], None], None] = None):
        ...

    @classmethod
    def _new_hydrated(cls: typing.Type[_BLOCKING_O], object_id: str, client: modal.client.Client, handle_metadata: typing.Union[google.protobuf.message.Message, None]) -> _BLOCKING_O:
        ...

    @classmethod
    def from_id(cls: typing.Type[_BLOCKING_O], object_id: str, client: typing.Union[modal.client.Client, None] = None) -> _BLOCKING_O:
        ...

    class ___hydrate_from_app_spec(typing_extensions.Protocol):
        def __call__(self, app_name: str, tag: typing.Union[str, None] = None, namespace=1, client: typing.Union[modal.client.Client, None] = None, environment_name: typing.Union[str, None] = None):
            ...

        async def aio(self, *args, **kwargs):
            ...

    _hydrate_from_app: ___hydrate_from_app_spec

    def _hydrate_from_other(self, other: _BLOCKING_O):
        ...

    def __repr__(self):
        ...

    @property
    def local_uuid(self):
        ...

    @property
    def object_id(self):
        ...

    def is_hydrated(self) -> bool:
        ...

    class ___deploy_spec(typing_extensions.Protocol):
        def __call__(self, label: str, namespace=1, client: typing.Union[modal.client.Client, None] = None, environment_name: typing.Union[str, None] = None) -> None:
            ...

        async def aio(self, *args, **kwargs) -> None:
            ...

    _deploy: ___deploy_spec

    def persist(self, label: str, namespace=1, environment_name: typing.Union[str, None] = None):
        ...

    def _persist(self, label: str, namespace=1, environment_name: typing.Union[str, None] = None):
        ...

    @classmethod
    def from_name(cls: typing.Type[_BLOCKING_O], app_name: str, tag: typing.Union[str, None] = None, namespace=1, environment_name: typing.Union[str, None] = None) -> _BLOCKING_O:
        ...

    @classmethod
    def lookup(cls: typing.Type[_BLOCKING_O], app_name: str, tag: typing.Union[str, None] = None, namespace=1, client: typing.Union[modal.client.Client, None] = None, environment_name: typing.Union[str, None] = None) -> _BLOCKING_O:
        ...

    @classmethod
    def _exists(cls: typing.Type[_BLOCKING_O], app_name: str, tag: typing.Union[str, None] = None, namespace=1, client: typing.Union[modal.client.Client, None] = None) -> bool:
        ...
