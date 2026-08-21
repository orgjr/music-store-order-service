from drf_spectacular.utils import extend_schema_view

from .create import create_schema
from .destroy import destroy_schema
from .list import list_schema
from .partial_update import partial_update_schema
from .retrieve import retrieve_schema
from .update import update_schema

order_schema = extend_schema_view(
    list=list_schema,
    create=create_schema,
    retrieve=retrieve_schema,
    update=update_schema,
    partial_update=partial_update_schema,
    destroy=destroy_schema,
)
