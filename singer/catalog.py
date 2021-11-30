'''Provides an object model for a Singer Catalog.'''
import orjson
import sys
from typing import Iterable, Optional, List, Any, cast

from . import metadata as metadata_module
from .bookmarks import get_currently_syncing
from .logger import get_logger
from .schema import Schema

LOGGER = get_logger()


def write_catalog(catalog: "Catalog") -> None:
    # If the catalog has no streams, log a warning
    if not catalog.streams:
        LOGGER.warning('Catalog being written with no streams.')

    catalog_json = orjson.dumps(catalog.to_dict(), option=orjson.OPT_INDENT_2)
    sys.stdout.buffer.write(catalog_json)
    sys.stdout.buffer.flush()

# pylint: disable=too-many-instance-attributes
class CatalogEntry():

    def __init__(
        self,
        tap_stream_id: Optional[str] = None,
        stream: Optional[str] = None,
        key_properties: Optional[List[str]] = None,
        schema: Optional[Schema] = None,
        replication_key: Optional[str] = None,
        is_view: Optional[bool] = None,
        database: Optional[str] = None,
        table: Optional[str] = None,
        row_count: Optional[int] = None,
        stream_alias: Optional[str] = None,
        metadata: Optional[dict] = None,
        replication_method: Optional[str] = None
    ) -> None:

        self.tap_stream_id = tap_stream_id
        self.stream = stream
        self.key_properties = key_properties
        self.schema = schema
        self.replication_key = replication_key
        self.replication_method = replication_method
        self.is_view = is_view
        self.database = database
        self.table = table
        self.row_count = row_count
        self.stream_alias = stream_alias
        self.metadata = metadata

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def is_selected(self):
        mdata = metadata_module.to_map(self.metadata)
        # pylint: disable=no-member
        return self.schema.selected or metadata_module.get(mdata, (), 'selected')

    def to_dict(self):
        result = {}
        if self.tap_stream_id:
            result['tap_stream_id'] = self.tap_stream_id
        if self.database:
            result['database_name'] = self.database
        if self.table:
            result['table_name'] = self.table
        if self.replication_key is not None:
            result['replication_key'] = self.replication_key
        if self.replication_method is not None:
            result['replication_method'] = self.replication_method
        if self.key_properties is not None:
            result['key_properties'] = self.key_properties
        if self.schema is not None:
            schema = self.schema.to_dict()  # pylint: disable=no-member
            result['schema'] = schema
        if self.is_view is not None:
            result['is_view'] = self.is_view
        if self.stream is not None:
            result['stream'] = self.stream
        if self.row_count is not None:
            result['row_count'] = self.row_count
        if self.stream_alias is not None:
            result['stream_alias'] = self.stream_alias
        if self.metadata is not None:
            result['metadata'] = self.metadata
        return result


class Catalog():

    def __init__(self, streams: List[CatalogEntry]) -> None:
        self.streams = streams

    def __str__(self) -> str:
        return str(self.__dict__)

    def __eq__(self, other: Any) -> bool:
        return cast(bool, self.__dict__ == other.__dict__)

    @classmethod
    def load(cls, filename: str) -> "Catalog":
        with open(filename, encoding='utf-8') as fp:  # pylint: disable=invalid-name
            return Catalog.from_dict(orjson.loads(fp.read()))

    @classmethod
    def from_dict(cls, data: dict) -> "Catalog":
        # TODO: We may want to store streams as a dict where the key is a
        # tap_stream_id and the value is a CatalogEntry. This will allow
        # faster lookup based on tap_stream_id. This would be a breaking
        # change, since callers typically access the streams property
        # directly.
        streams = []
        for stream in data['streams']:
            entry = CatalogEntry()
            entry.tap_stream_id = stream.get('tap_stream_id')
            entry.stream = stream.get('stream')
            entry.replication_key = stream.get('replication_key')
            entry.key_properties = stream.get('key_properties')
            entry.database = stream.get('database_name')
            entry.table = stream.get('table_name')
            entry.schema = Schema.from_dict(stream.get('schema'))
            entry.is_view = stream.get('is_view')
            entry.stream_alias = stream.get('stream_alias')
            entry.metadata = stream.get('metadata')
            entry.replication_method = stream.get('replication_method')
            streams.append(entry)
        return Catalog(streams)

    def to_dict(self) -> dict:
        return {'streams': [stream.to_dict() for stream in self.streams]}

    def dump(self) -> None:
        write_catalog(self)

    def get_stream(self, tap_stream_id: str) -> Optional[CatalogEntry]:
        for stream in self.streams:
            if stream.tap_stream_id == tap_stream_id:
                return stream
        return None

    def _shuffle_streams(self, state: dict) -> List[CatalogEntry]:
        currently_syncing = get_currently_syncing(state)

        if currently_syncing is None:
            return self.streams

        matching_index = 0
        for i, catalog_entry in enumerate(self.streams):
            if catalog_entry.tap_stream_id == currently_syncing:
                matching_index = i
                break
        top_half = self.streams[matching_index:]
        bottom_half = self.streams[:matching_index]
        return top_half + bottom_half


    def get_selected_streams(self, state: dict) -> Iterable[CatalogEntry]:
        for stream in self._shuffle_streams(state):
            if not stream.is_selected():
                LOGGER.info('Skipping stream: %s', stream.tap_stream_id)
                continue

            yield stream
