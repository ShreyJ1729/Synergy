import asyncio.locks
import modal.object
import modal_proto.api_pb2
import typing
import typing_extensions

class _Volume(modal.object._Object):
    _lock: asyncio.locks.Lock

    def _initialize_from_empty(self):
        ...

    @staticmethod
    def new() -> _Volume:
        ...

    @staticmethod
    def persisted(label: str, namespace=1, environment_name: typing.Union[str, None] = None) -> _Volume:
        ...

    async def _do_reload(self, lock=True):
        ...

    async def commit(self):
        ...

    async def reload(self):
        ...

    def iterdir(self, path: str) -> typing.AsyncIterator[modal_proto.api_pb2.VolumeListFilesEntry]:
        ...

    async def listdir(self, path: str) -> typing.List[modal_proto.api_pb2.VolumeListFilesEntry]:
        ...


class Volume(modal.object.Object):
    _lock: asyncio.locks.Lock

    def __init__(self):
        ...

    def _initialize_from_empty(self):
        ...

    @staticmethod
    def new() -> Volume:
        ...

    @staticmethod
    def persisted(label: str, namespace=1, environment_name: typing.Union[str, None] = None) -> Volume:
        ...

    class ___do_reload_spec(typing_extensions.Protocol):
        def __call__(self, lock=True):
            ...

        async def aio(self, *args, **kwargs):
            ...

    _do_reload: ___do_reload_spec

    class __commit_spec(typing_extensions.Protocol):
        def __call__(self):
            ...

        async def aio(self, *args, **kwargs):
            ...

    commit: __commit_spec

    class __reload_spec(typing_extensions.Protocol):
        def __call__(self):
            ...

        async def aio(self, *args, **kwargs):
            ...

    reload: __reload_spec

    class __iterdir_spec(typing_extensions.Protocol):
        def __call__(self, path: str) -> typing.Iterator[modal_proto.api_pb2.VolumeListFilesEntry]:
            ...

        def aio(self, path: str) -> typing.AsyncIterator[modal_proto.api_pb2.VolumeListFilesEntry]:
            ...

    iterdir: __iterdir_spec

    class __listdir_spec(typing_extensions.Protocol):
        def __call__(self, path: str) -> typing.List[modal_proto.api_pb2.VolumeListFilesEntry]:
            ...

        async def aio(self, *args, **kwargs) -> typing.List[modal_proto.api_pb2.VolumeListFilesEntry]:
            ...

    listdir: __listdir_spec
