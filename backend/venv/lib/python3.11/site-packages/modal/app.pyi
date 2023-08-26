import google.protobuf.message
import modal._output
import modal._resolver
import modal.client
import modal.gpu
import modal.image
import modal.mount
import modal.object
import modal.sandbox
import modal.secret
import typing
import typing_extensions

Tree = typing.TypeVar("Tree")

class _App:
    _tag_to_object: typing.Dict[str, modal.object._Object]
    _tag_to_object_id: typing.Dict[str, str]
    _tag_to_handle_metadata: typing.Dict[str, google.protobuf.message.Message]
    _client: modal.client._Client
    _app_id: str
    _app_page_url: str
    _resolver: typing.Union[modal._resolver.Resolver, None]
    _environment_name: str
    _output_mgr: typing.Union[modal._output.OutputManager, None]
    _associated_stub: typing.Union[typing.Any, None]

    def __init__(self, client: modal.client._Client, app_id: str, app_page_url: str, output_mgr: typing.Union[modal._output.OutputManager, None], tag_to_object: typing.Union[typing.Dict[str, modal.object._Object], None] = None, tag_to_object_id: typing.Union[typing.Dict[str, str], None] = None, stub_name: typing.Union[str, None] = None, environment_name: typing.Union[str, None] = None):
        ...

    @property
    def client(self) -> modal.client._Client:
        ...

    @property
    def app_id(self) -> str:
        ...

    def _associate_stub(self, stub):
        ...

    async def _create_all_objects(self, blueprint: typing.Dict[str, modal.object._Object], new_app_state: int, environment_name: str, shell: bool = False):
        ...

    def _uncreate_all_objects(self):
        ...

    async def disconnect(self):
        ...

    async def stop(self):
        ...

    def log_url(self):
        ...

    def __getitem__(self, tag: str) -> modal.object._Object:
        ...

    def __contains__(self, tag: str) -> bool:
        ...

    def __getattr__(self, tag: str) -> modal.object._Object:
        ...

    def _get_object(self, tag: str) -> typing.Union[modal.object._Object, None]:
        ...

    async def _init_container(self, client: modal.client._Client, app_id: str, stub_name: str):
        ...

    @staticmethod
    async def init_container(client: modal.client._Client, app_id: str, stub_name: str = '') -> _App:
        ...

    @staticmethod
    async def _init_existing(client: modal.client._Client, existing_app_id: str, output_mgr: typing.Union[modal._output.OutputManager, None] = None) -> _App:
        ...

    @staticmethod
    async def _init_new(client: modal.client._Client, description: typing.Union[str, None] = None, detach: bool = False, deploying: bool = False, environment_name: str = '', output_mgr: typing.Union[modal._output.OutputManager, None] = None) -> _App:
        ...

    @staticmethod
    async def _init_from_name(client: modal.client._Client, name: str, namespace, environment_name: str = '', output_mgr: typing.Union[modal._output.OutputManager, None] = None):
        ...

    async def create_one_object(self, obj: modal.object._Object, environment_name: str) -> None:
        ...

    async def deploy(self, name: str, namespace, object_entity: str) -> str:
        ...

    async def spawn_sandbox(self, *entrypoint_args: str, image: typing.Union[modal.image._Image, None] = None, mounts: typing.Sequence[modal.mount._Mount] = (), secrets: typing.Sequence[modal.secret._Secret] = (), timeout: typing.Union[int, None] = None, workdir: typing.Union[str, None] = None, gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None, cloud: typing.Union[str, None] = None, cpu: typing.Union[float, None] = None, memory: typing.Union[int, None] = None) -> modal.sandbox._Sandbox:
        ...

    @staticmethod
    def _reset_container():
        ...


class App:
    _tag_to_object: typing.Dict[str, modal.object.Object]
    _tag_to_object_id: typing.Dict[str, str]
    _tag_to_handle_metadata: typing.Dict[str, google.protobuf.message.Message]
    _client: modal.client.Client
    _app_id: str
    _app_page_url: str
    _resolver: typing.Union[modal._resolver.Resolver, None]
    _environment_name: str
    _output_mgr: typing.Union[modal._output.OutputManager, None]
    _associated_stub: typing.Union[typing.Any, None]

    def __init__(self, client: modal.client.Client, app_id: str, app_page_url: str, output_mgr: typing.Union[modal._output.OutputManager, None], tag_to_object: typing.Union[typing.Dict[str, modal.object.Object], None] = None, tag_to_object_id: typing.Union[typing.Dict[str, str], None] = None, stub_name: typing.Union[str, None] = None, environment_name: typing.Union[str, None] = None):
        ...

    @property
    def client(self) -> modal.client.Client:
        ...

    @property
    def app_id(self) -> str:
        ...

    def _associate_stub(self, stub):
        ...

    class ___create_all_objects_spec(typing_extensions.Protocol):
        def __call__(self, blueprint: typing.Dict[str, modal.object.Object], new_app_state: int, environment_name: str, shell: bool = False):
            ...

        async def aio(self, *args, **kwargs):
            ...

    _create_all_objects: ___create_all_objects_spec

    def _uncreate_all_objects(self):
        ...

    class __disconnect_spec(typing_extensions.Protocol):
        def __call__(self):
            ...

        async def aio(self, *args, **kwargs):
            ...

    disconnect: __disconnect_spec

    class __stop_spec(typing_extensions.Protocol):
        def __call__(self):
            ...

        async def aio(self, *args, **kwargs):
            ...

    stop: __stop_spec

    def log_url(self):
        ...

    def __getitem__(self, tag: str) -> modal.object.Object:
        ...

    def __contains__(self, tag: str) -> bool:
        ...

    def __getattr__(self, tag: str) -> modal.object.Object:
        ...

    def _get_object(self, tag: str) -> typing.Union[modal.object.Object, None]:
        ...

    class ___init_container_spec(typing_extensions.Protocol):
        def __call__(self, client: modal.client.Client, app_id: str, stub_name: str):
            ...

        async def aio(self, *args, **kwargs):
            ...

    _init_container: ___init_container_spec

    class __init_container_spec(typing_extensions.Protocol):
        def __call__(self, client: modal.client.Client, app_id: str, stub_name: str = '') -> App:
            ...

        async def aio(self, *args, **kwargs) -> App:
            ...

    init_container: __init_container_spec

    class ___init_existing_spec(typing_extensions.Protocol):
        def __call__(self, client: modal.client.Client, existing_app_id: str, output_mgr: typing.Union[modal._output.OutputManager, None] = None) -> App:
            ...

        async def aio(self, *args, **kwargs) -> App:
            ...

    _init_existing: ___init_existing_spec

    class ___init_new_spec(typing_extensions.Protocol):
        def __call__(self, client: modal.client.Client, description: typing.Union[str, None] = None, detach: bool = False, deploying: bool = False, environment_name: str = '', output_mgr: typing.Union[modal._output.OutputManager, None] = None) -> App:
            ...

        async def aio(self, *args, **kwargs) -> App:
            ...

    _init_new: ___init_new_spec

    class ___init_from_name_spec(typing_extensions.Protocol):
        def __call__(self, client: modal.client.Client, name: str, namespace, environment_name: str = '', output_mgr: typing.Union[modal._output.OutputManager, None] = None):
            ...

        async def aio(self, *args, **kwargs):
            ...

    _init_from_name: ___init_from_name_spec

    class __create_one_object_spec(typing_extensions.Protocol):
        def __call__(self, obj: modal.object.Object, environment_name: str) -> None:
            ...

        async def aio(self, *args, **kwargs) -> None:
            ...

    create_one_object: __create_one_object_spec

    class __deploy_spec(typing_extensions.Protocol):
        def __call__(self, name: str, namespace, object_entity: str) -> str:
            ...

        async def aio(self, *args, **kwargs) -> str:
            ...

    deploy: __deploy_spec

    class __spawn_sandbox_spec(typing_extensions.Protocol):
        def __call__(self, *entrypoint_args: str, image: typing.Union[modal.image.Image, None] = None, mounts: typing.Sequence[modal.mount.Mount] = (), secrets: typing.Sequence[modal.secret.Secret] = (), timeout: typing.Union[int, None] = None, workdir: typing.Union[str, None] = None, gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None, cloud: typing.Union[str, None] = None, cpu: typing.Union[float, None] = None, memory: typing.Union[int, None] = None) -> modal.sandbox.Sandbox:
            ...

        async def aio(self, *args, **kwargs) -> modal.sandbox.Sandbox:
            ...

    spawn_sandbox: __spawn_sandbox_spec

    @staticmethod
    def _reset_container():
        ...


_container_app: _App

container_app: App

def is_local() -> bool:
    ...
