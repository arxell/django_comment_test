from contracts import new_contract


@new_contract
def QuerySet(x):
    from django.db.models.query import QuerySet
    return isinstance(x, QuerySet)


@new_contract
def Comment(x):
    from .models import Comment
    return isinstance(x, Comment)


@new_contract
def Export(x):
    from .models import Export
    return isinstance(x, Comment)


@new_contract
def AddSchemIn(x):
    from .defs import AddSchemIn
    return isinstance(x, AddSchemIn)


@new_contract
def AddSchemOut(x):
    from .defs import AddSchemOut
    return isinstance(x, AddSchemOut)


@new_contract
def EditSchemIn(x):
    from .defs import EditSchemIn
    return isinstance(x, EditSchemIn)


@new_contract
def EditSchemOut(x):
    from .defs import EditSchemOut
    return isinstance(x, EditSchemOut)


@new_contract
def DeleteSchemIn(x):
    from .defs import DeleteSchemIn
    return isinstance(x, DeleteSchemIn)


@new_contract
def DeleteSchemOut(x):
    from .defs import DeleteSchemOut
    return isinstance(x, DeleteSchemOut)


@new_contract
def TreeSchemOut(x):
    from .defs import TreeSchemOut
    return isinstance(x, TreeSchemOut)


@new_contract
def TreeSchemIn(x):
    from .defs import TreeSchemIn
    return isinstance(x, TreeSchemIn)


@new_contract
def UserHistorySchemaIn(x):
    from .defs import UserHistorySchemaIn
    return isinstance(x, UserHistorySchemaIn)


@new_contract
def UserHistorySchemaOut(x):
    from .defs import UserHistorySchemaOut
    return isinstance(x, UserHistorySchemaOut)


@new_contract
def ExportSchemaIn(x):
    from .defs import ExportSchemaIn
    return isinstance(x, ExportSchemaIn)


@new_contract
def ExportSchemaOut(x):
    from .defs import ExportSchemaOut
    return isinstance(x, ExportSchemaOut)


@new_contract
def ExportHistorySchemaIn(x):
    from .defs import ExportHistorySchemaIn
    return isinstance(x, ExportHistorySchemaIn)


@new_contract
def ExportHistorySchemaOut(x):
    from .defs import ExportHistorySchemaOut
    return isinstance(x, ExportHistorySchemaOut)

