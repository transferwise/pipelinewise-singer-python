from typing import Dict, List, Optional, Any, cast

StateDict = Dict[str, Any]

def ensure_bookmark_path(state: StateDict, path: List[str]) -> StateDict:
    submap = state
    for path_component in path:
        if submap.get(path_component) is None:
            submap[path_component] = {}

        submap = submap[path_component]
    return state

def write_bookmark(
    state: StateDict, tap_stream_id: str, key: str, val: Any
) -> StateDict:
    state = ensure_bookmark_path(state, ['bookmarks', tap_stream_id])
    state['bookmarks'][tap_stream_id][key] = val
    return state

def clear_bookmark(state: StateDict, tap_stream_id: str, key: str) -> StateDict:
    state = ensure_bookmark_path(state, ['bookmarks', tap_stream_id])
    state['bookmarks'][tap_stream_id].pop(key, None)
    return state

def reset_stream(state: StateDict, tap_stream_id: str) -> StateDict:
    state = ensure_bookmark_path(state, ['bookmarks', tap_stream_id])
    state['bookmarks'][tap_stream_id] = {}
    return state

def get_bookmark(
    state: StateDict, tap_stream_id: str, key: str, default: Optional[Any] = None
) -> Optional[Any]:
    return state.get('bookmarks', {}).get(tap_stream_id, {}).get(key, default)

def set_offset(
    state: StateDict, tap_stream_id: str, offset_key: Any, offset_value: Any
) -> StateDict:
    state = ensure_bookmark_path(state, ['bookmarks', tap_stream_id, "offset", offset_key])
    state['bookmarks'][tap_stream_id]["offset"][offset_key] = offset_value
    return state

def clear_offset(state: StateDict, tap_stream_id: str) -> StateDict:
    state = ensure_bookmark_path(state, ['bookmarks', tap_stream_id, "offset"])
    state['bookmarks'][tap_stream_id]["offset"] = {}
    return state

def get_offset(
    state: StateDict, tap_stream_id: str, default: Optional[Any] = None
):
    return state.get('bookmarks', {}).get(tap_stream_id, {}).get("offset", default)

def set_currently_syncing(state: StateDict, tap_stream_id: str):
    state['currently_syncing'] = tap_stream_id
    return state

def get_currently_syncing(state: StateDict, default: str = None) -> Optional[str]:
    return cast(str, state.get('currently_syncing', default))
