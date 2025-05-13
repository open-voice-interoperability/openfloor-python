from dataclasses import dataclass, field, make_dataclass
from typing import Dict, List, Optional, Union, Any, Iterator, Tuple, ClassVar, Type, get_type_hints, Set
from abc import ABC, abstractmethod
import json

class JsonSerializable(ABC):
    """Abstract base class for JSON serializable objects"""
    
    @abstractmethod
    def __iter__(self) -> Iterator[Any]:
        """Convert instance to JSON-compatible format"""
        raise NotImplementedError("Subclasses must implement this method")
    
    def _serialize_value(self, value: Any) -> Any:
        """Helper method to recursively serialize values"""
        if isinstance(value, JsonSerializableList):
            return [self._serialize_value(item) for item in value]
        elif isinstance(value, (JsonSerializableDict, JsonSerializableDataclass)):
            return {k: self._serialize_value(v) for k, v in value}
        elif isinstance(value, dict):
            return {k: self._serialize_value(v) for k, v in value.items()}
        elif hasattr(value, '__iter__') and not isinstance(value, (str, bytes)):
            return [self._serialize_value(item) for item in value]
        return value

    @classmethod
    def _json_default(cls, obj: Any) -> Any:
        """Default JSON serialization handler for JsonSerializable objects"""
        if isinstance(obj, JsonSerializable):
            return obj.__json__()
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

    def to_json(self, **kwargs) -> str:
        """Convert instance to JSON string"""
        return json.dumps(self, default=self._json_default, **kwargs)

    def __repr__(self) -> str:
        """Return JSON string representation of the object"""
        return self.to_json()

    def to_file(self, filepath: str, **kwargs) -> None:
        """Save instance to a JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self, f, default=self._json_default, **kwargs)

    @classmethod
    def from_json(cls, json_str: str) -> 'JsonSerializable':
        """Create an instance from a JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)

    @classmethod
    def from_file(cls, filepath: str, **kwargs) -> 'JsonSerializable':
        """Create an instance from a JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f, **kwargs)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JsonSerializableDict':
        """Create an instance from a dictionary or instance"""
        if isinstance(data, cls):
            return data
        if isinstance(data, dict):
            return cls(**data)
        raise TypeError(f"Cannot create {cls.__name__} from {type(data)}")

    def __json__(self):
        """Default JSON serialization method"""
        return list(self)

class JsonSerializableDict(JsonSerializable):
    """Base class for JSON serializable objects that serialize to dictionaries"""
    
    def __init__(self, *args, **kwargs):
        """Initialize with optional key-value pairs"""
        self._data = {}
        if args and isinstance(args[0], dict):
            # Initialize with dictionary from first argument
            for key, value in args[0].items():
                self.__setitem__(key, value)
        # Initialize with keyword arguments
        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def __getitem__(self, key: str) -> Any:
        """Get a value by key"""
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """Set a value by key"""
        self._data[key] = value

    def __delitem__(self, key: str) -> None:
        """Delete a value by key"""
        del self._data[key]

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert instance to JSON-compatible dictionary"""
        for key, value in self._data.items():
            # Convert nested objects to basic types
            if isinstance(value, JsonSerializableList):
                yield key, [self._serialize_value(item) for item in value]
            elif isinstance(value, (JsonSerializableDict, JsonSerializableDataclass)):
                yield key, {k: self._serialize_value(v) for k, v in value}
            elif isinstance(value, list):
                yield key, [self._serialize_value(item) for item in value]
            elif isinstance(value, dict):
                yield key, {k: self._serialize_value(v) for k, v in value.items()}
            else:
                yield key, value

    def __len__(self) -> int:
        """Get the number of items"""
        return len(self._data)

    def __contains__(self, key: str) -> bool:
        """Check if a key exists"""
        return key in self._data

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value by key with a default value"""
        try:
            return self[key]
        except KeyError:
            return default

    def update(self, other: Dict[str, Any]) -> None:
        """Update with values from another dictionary"""
        for key, value in other.items():
            self[key] = value

    def clear(self) -> None:
        """Clear all items"""
        self._data.clear()

    def copy(self) -> 'JsonSerializableDict':
        """Create a copy of the dictionary"""
        return self.__class__(**self._data.copy())

    def __json__(self):
        """JSON serialization for dictionary-like objects"""
        return {k: self._serialize_value(v) for k, v in self}

class JsonSerializableList(JsonSerializable):
    """Base class for JSON serializable objects that serialize to lists"""
    
    def __init__(self, *args, **kwargs):
        """Initialize with optional items"""
        self._items = []
        if args and isinstance(args[0], list):
            self._items = list(args[0])
        elif args:
            self._items = list(args)

    def __iter__(self) -> Iterator[Any]:
        """Convert instance to JSON-compatible list"""
        for item in self._items:
            if isinstance(item, JsonSerializableDict) or isinstance(item, JsonSerializableDataclass):
                yield dict(item)
            elif isinstance(item, JsonSerializableList):
                yield [i for i in item.__iter__()]
            else:
                yield self._serialize_value(item)

    def append(self, item: Any) -> None:
        """Add an item to the list"""
        self._items.append(item)

    def extend(self, items: List[Any]) -> None:
        """Add multiple items to the list"""
        self._items.extend(items)

    def clear(self) -> None:
        """Clear all items from the list"""
        self._items.clear()

    def __len__(self) -> int:
        """Get the number of items in the list"""
        return len(self._items)

    def __getitem__(self, index: int) -> Any:
        """Get an item by index"""
        return self._items[index]

    def __contains__(self, item: Any) -> bool:
        """Check if an item is in the list"""
        return item in self._items

    def __json__(self):
        """JSON serialization for list-like objects"""
        return [self._serialize_value(item) for item in self]

    def to_json(self, **kwargs) -> str:
        """Convert instance to JSON string"""
        return json.dumps(list(self), **kwargs)

    def to_file(self, filepath: str, **kwargs) -> None:
        """Save instance to a JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(list(self), f, **kwargs)

class JsonSerializableDataclass(JsonSerializable):
    """Base class for JSON serializable objects that are dataclasses"""

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Convert instance to JSON-compatible dictionary by iterating over dataclass fields"""
        for field_name, field_value in self.__dataclass_fields__.items():
            if not field_name.startswith('_'):
                value = getattr(self, field_name)
                yield field_name, self._serialize_value(value)

    def __json__(self):
        """JSON serialization for dataclass objects"""
        return {k: self._serialize_value(v) for k, v in self}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JsonSerializableDataclass':
        """Create an instance from a dictionary"""
        if isinstance(data, cls):
            return data
        if isinstance(data, dict):
            return cls(**data)
        raise TypeError(f"Cannot create {cls.__name__} from {type(data)}")

    def copy(self) -> 'JsonSerializableDataclass':
        """Create a copy of the dataclass"""
        return self.__class__(**{k: getattr(self, k) for k in self.__dataclass_fields__ if not k.startswith('_')})


def split_kwargs(cls: Type, kwargs: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Split kwargs into defined and undefined fields for a dataclass class.
    
    Args:
        cls: The class to check fields against
        kwargs: Dictionary of keyword arguments to split
        
    Returns:
        Tuple of (defined_fields, undefined_fields) where each is a dictionary
        of the respective fields from kwargs. Defined fields that are not in kwargs
        will be included in defined_fields with a value of None.
    """
    # Get the defined fields for the class
    defined_fields: Set[str] = set()
    if hasattr(cls, '__dataclass_fields__'):
        defined_fields = set(cls.__dataclass_fields__.keys())
    
    # Initialize defined_kwargs with all defined fields set to None
    defined_kwargs = {field: None for field in defined_fields}
    
    # Update defined_kwargs with values from kwargs
    defined_kwargs.update({k: v for k, v in kwargs.items() if k in defined_fields})
    
    # Get undefined fields
    undefined_kwargs = {k: v for k, v in kwargs.items() if k not in defined_fields}
    
    return defined_kwargs, undefined_kwargs