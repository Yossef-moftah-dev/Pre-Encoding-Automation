#############################################################
#### JSON serialization utilities for safe data conversion.
#############################################################


import json
from typing import Any, Dict
from dataclasses import asdict, is_dataclass


class SafeJSONEncoder(json.JSONEncoder):
    # Custom JSON encoder that handles non-serializable objects.
    
    def default(self, obj: Any) -> Any:
        # Convert non-serializable objects to serializable format.
        # Args:
        #     obj: Object to encode
        # Returns:
        #     Serializable representation of object

        # Handle dataclasses
        if is_dataclass(obj):
            return asdict(obj)
        
        # Handle custom objects with to_dict method
        if hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
            return obj.to_dict()
        
        # Handle objects with __dict__
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        
        # Fall back to default encoder
        return super().default(obj)


def make_serializable(obj: Any) -> Any:
    # Convert an object to a JSON-serializable format.
    # Args:
    #     obj: Object to convert
    # Returns:
    #     JSON-serializable version of object

    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj
    
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    
    if isinstance(obj, (list, tuple)):
        return [make_serializable(item) for item in obj]
    
    if is_dataclass(obj):
        return make_serializable(asdict(obj))
    
    if hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
        return make_serializable(obj.to_dict())
    
    if hasattr(obj, '__dict__'):
        return make_serializable(obj.__dict__)
    
    return str(obj)


def to_json(obj: Any, indent: int = 2) -> str:
    # Convert object to JSON string safely.
    # Args:
    #     obj: Object to convert
    #     indent: Indentation level
    # Returns:
    #     JSON string

    safe_obj = make_serializable(obj)
    return json.dumps(safe_obj, indent=indent, cls=SafeJSONEncoder)


def from_json(json_str: str) -> Any:
    # Parse JSON string safely.
    # Args:
    #     json_str: JSON string to parse
    # Returns:
    #     Parsed object

    return json.loads(json_str)
