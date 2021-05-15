from typing import Any, Dict, Optional, Tuple, List

Breadcrumb = Tuple[str, ...]
CompiledMetadata = Dict[Breadcrumb, dict]

def new() -> CompiledMetadata:
    return {}

def to_map(raw_metadata: List[dict]) -> CompiledMetadata:
    return {tuple(md['breadcrumb']): md['metadata'] for md in raw_metadata}

def to_list(compiled_metadata: CompiledMetadata) -> List[dict]:
    return [{'breadcrumb': k, 'metadata': v} for k, v in compiled_metadata.items()]

def delete(
    compiled_metadata: CompiledMetadata,
    breadcrumb: Breadcrumb,
    k: str
) -> None:
    del compiled_metadata[breadcrumb][k]

def write(
    compiled_metadata: CompiledMetadata,
    breadcrumb: Breadcrumb,
    k: str,
    val: Any
) -> CompiledMetadata:
    if val is None:
        raise Exception()
    if breadcrumb in compiled_metadata:
        compiled_metadata[breadcrumb].update({k: val})
    else:
        compiled_metadata[breadcrumb] = {k: val}
    return compiled_metadata

def get(
    compiled_metadata: CompiledMetadata,
    breadcrumb: Breadcrumb,
    k: str
) -> Any:
    return compiled_metadata.get(breadcrumb, {}).get(k)

def get_standard_metadata(
    schema: Optional[dict] = None,
    schema_name: Optional[str] = None,
    key_properties: Optional[List[str]] = None,
    valid_replication_keys: Optional[List[str]] = None,
    replication_method: Optional[str] = None
) -> List[dict]:
    mdata: CompiledMetadata = {}

    if key_properties is not None:
        mdata = write(mdata, (), 'table-key-properties', key_properties)
    if replication_method:
        mdata = write(mdata, (), 'forced-replication-method', replication_method)
    if valid_replication_keys is not None:
        mdata = write(mdata, (), 'valid-replication-keys', valid_replication_keys)
    if schema:
        mdata = write(mdata, (), 'inclusion', 'available')

        if schema_name:
            mdata = write(mdata, (), 'schema-name', schema_name)
        for field_name in schema['properties'].keys():
            if key_properties and field_name in key_properties:
                mdata = write(mdata, ('properties', field_name), 'inclusion', 'automatic')
            else:
                mdata = write(mdata, ('properties', field_name), 'inclusion', 'available')

    return to_list(mdata)
