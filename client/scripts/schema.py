import uuid

from marshmallow import Schema, fields, post_load, validate


class AutoSchema(Schema):

    class Meta:
        ordered = True

    @post_load
    @classmethod
    def build(cls, data, **kwargs):
        return cls(**data)


class JournalEntryGroupSchema(AutoSchema):
    id = fields.UUID(missing=uuid.uuid4)
    date = fields.Date(required=True)
    description = fields.String()
    currency = fields.String(required=True)


class JournalEntrySchema(AutoSchema):
    id = fields.UUID(missing=uuid.uuid4)
    description = fields.String()
    ref_num = fields.Integer()
    quantity = fields.Decimal(required=True, default=1, as_string=True)
    unit_cost = fields.Decimal(required=True, default=1, as_string=True)
    is_debit = fields.Boolean(required=True)
    entry_group = fields.Nested(JournalEntryGroupSchema, required=True)


class AccountingPeriodSchema(AutoSchema):
    name = fields.String(required=True)
    end_date = fields.Date()
    entries = fields.Nested(JournalEntrySchema, many=True)


class AccountSchema(AutoSchema):
    code = fields.Str(required=True)
    name = fields.Str(required=True)
    description = fields.Str()
    account_type = fields.Str(required=True, validate=validate.OneOf(['A', 'L', 'I', 'E']))
    parent_account = fields.Nested('self', many=False, default=None, only=['code'])
    created_at = fields.DateTime()
    is_deleted = fields.Boolean()

    periods = fields.Nested(AccountingPeriodSchema, many=True)


class LegalEntitySchema(AutoSchema):
    code = fields.String(required=True)
    name = fields.String(required=True)
    email = fields.Email()
    description = fields.String()
    currency = fields.String(required=True)
    is_individual = fields.Boolean(required=True)
    accounts = fields.Nested(AccountSchema, many=True)
    created_at = fields.DateTime()
    is_deleted = fields.Boolean()
