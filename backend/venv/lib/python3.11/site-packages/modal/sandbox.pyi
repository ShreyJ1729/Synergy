import modal.client
import modal.gpu
import modal.image
import modal.mount
import modal.object
import modal.secret
import modal_proto.api_pb2
import typing
import typing_extensions

class _LogsReader:
    def __init__(self, file_descriptor: int, sandbox_id: str, client: modal.client._Client) -> None:
        ...

    async def read(self) -> str:
        ...


class LogsReader:
    def __init__(self, file_descriptor: int, sandbox_id: str, client: modal.client.Client) -> None:
        ...

    class __read_spec(typing_extensions.Protocol):
        def __call__(self) -> str:
            ...

        async def aio(self, *args, **kwargs) -> str:
            ...

    read: __read_spec


class _Sandbox(modal.object._Object):
    _result: typing.Union[modal_proto.api_pb2.GenericResult, None]
    _stdout: _LogsReader
    _stderr: _LogsReader

    @staticmethod
    def _new(entrypoint_args: typing.Sequence[str], image: modal.image._Image, mounts: typing.Sequence[modal.mount._Mount], secrets: typing.Sequence[modal.secret._Secret], timeout: typing.Union[int, None] = None, workdir: typing.Union[str, None] = None, gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None, cloud: typing.Union[str, None] = None, cpu: typing.Union[float, None] = None, memory: typing.Union[int, None] = None) -> _Sandbox:
        ...

    async def wait(self):
        ...

    @property
    def stdout(self) -> _LogsReader:
        ...

    @property
    def stderr(self) -> _LogsReader:
        ...

    @property
    def returncode(self) -> typing.Union[int, None]:
        ...


class Sandbox(modal.object.Object):
    _result: typing.Union[modal_proto.api_pb2.GenericResult, None]
    _stdout: LogsReader
    _stderr: LogsReader

    def __init__(self):
        ...

    @staticmethod
    def _new(entrypoint_args: typing.Sequence[str], image: modal.image.Image, mounts: typing.Sequence[modal.mount.Mount], secrets: typing.Sequence[modal.secret.Secret], timeout: typing.Union[int, None] = None, workdir: typing.Union[str, None] = None, gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None, cloud: typing.Union[str, None] = None, cpu: typing.Union[float, None] = None, memory: typing.Union[int, None] = None) -> Sandbox:
        ...

    class __wait_spec(typing_extensions.Protocol):
        def __call__(self):
            ...

        async def aio(self, *args, **kwargs):
            ...

    wait: __wait_spec

    @property
    def stdout(self) -> LogsReader:
        ...

    @property
    def stderr(self) -> LogsReader:
        ...

    @property
    def returncode(self) -> typing.Union[int, None]:
        ...
