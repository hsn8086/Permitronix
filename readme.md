# Permitronix

Permitronix is a Python permission management module that allows you to manage permission tables for users and objects.

## Installation

Permitronix can be installed via pip:

```bash
pip install permitronix
```

## Usage

### Permitronix

The `Permitronix` class allows you to manage permission tables for objects. Here is an example of how to
use `Permitronix`:

```python
from permitronix import Permitronix
from permitronix.permission_node import PermissionNode
from permitronix.permission_table import PermissionTable

# Create a permitronix instance
ptx = Permitronix({})

# Set a permission for an object
obj = "example"

with ptx.enter(obj) as v:
    pt: PermissionTable = v.value
    pt.set_permission(PermissionNode('regular_expressions_for_some_permissions_.*', 'scope_id:1145'))

# Get the permission table for an object
pt = ptx.get_permission_table(obj)

# Remove a permission table for an object
ptx.rem_permission_obj(obj)

# Check if a permission table exists for an object
exists = ptx.exists(obj)
```

### Permission Table

The `PermissionTable` class allows you to define permission tables for users and objects. Here is an example of how to
create a permission table:

```python
from permitronix import Permitronix
from permitronix.permission_node import PermissionNode
from permitronix.permission_table import PermissionTable

# Create a permitronix instance
ptx = Permitronix({})

# Create a permission table
pt = PermissionTable(ptx, 'data')
pt.set_permission(PermissionNode('regular_expressions_for_some_permissions_.*', 'scope_id:1145'))


```

### Permission Node

A `PermissionNode` is a node in the permission tree. Each node has a name and a permission level. Here is an example of
how to create a permission node:

```python
from permitronix.permission_level import PermissionLevel
from permitronix.permission_node import PermissionNode

# Create a permission node
pn = PermissionNode("admin", PermissionLevel("op:12"))
```

## Contributing

We welcome contributions from anyone who is interested in improving this project. If you find any issues, bugs, or have
suggestions for improvement, please feel free to open an issue or submit a pull request.

We will review your changes and provide feedback if necessary. Thank you for your contributions!

## License

This source code is licensed under the `MIT license` and may be used for any purpose consistent with local law, provided
that the copyright notice is retained.