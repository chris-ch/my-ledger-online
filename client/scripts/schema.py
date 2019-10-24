from marshmallow import Schema, fields, post_load, validate


class AccountSchema(Schema):
    class Meta:
        fields = ('account_type', 'parent_account','code', 'name', 'description', 'is_deleted', 'created_at')
        ordered = True

    code = fields.Str(required=True)
    name = fields.Str(required=True)
    description = fields.Str()
    account_type = fields.Str(required=True, validate=validate.OneOf(['A', 'L', 'I', 'E']))
    parent_account = fields.Nested('self', many=False, default=None, only=['code'])
    created_at = fields.DateTime()
    is_deleted = fields.Boolean()

    @post_load
    @classmethod
    def build(cls, data, **kwargs):
        return cls(**data)


class LegalEntitySchema(Schema):
    class Meta:
        fields = ('code', 'name', 'email', 'description', 'currency', 'created_at', 'is_individual', 'is_deleted', 'accounts', 'created_at')
        ordered = True

    code = fields.String(required=True)
    name = fields.String(required=True)
    email = fields.Email()
    description = fields.String()
    currency = fields.String(required=True)
    is_individual = fields.Boolean(required=True)
    accounts = fields.Nested(AccountSchema, many=True)
    created_at = fields.DateTime()
    is_deleted = fields.Boolean()

    @post_load
    @classmethod
    def build(cls, data, **kwargs):
        return cls(**data)


class AccountingPeriodSchema(Schema):
    class Meta:
        fields = ('legal_entity', 'name', 'end_date')
        ordered = True

    name = fields.String(required=True)
    end_date = fields.Date()
    legal_entity_code = fields.Nested(LegalEntitySchema, only=['code'], required=True)

    @post_load
    @classmethod
    def build(cls, data, **kwargs):
        return cls(**data)


class JournalEntrySchema(Schema):
    description = fields.String()
    ref_num = fields.Integer()
    quantity = fields.Decimal(required=True, default=1, as_string=True)
    unit_cost = fields.Decimal(required=True, default=1, as_string=True)
    is_debit = fields.Boolean(required=True)

    account = fields.Nested(AccountSchema, only=['code'], required=True)

    @post_load
    @classmethod
    def build(cls, data, **kwargs):
        return cls(**data)


class JournalEntryGroupSchema(Schema):
    date = fields.Date(required=True)
    description = fields.String()

    currency = fields.String(required=True)
    accounting_period = fields.Nested(AccountingPeriodSchema, only=['name'], many=False, required=True)
    entries = fields.Nested(JournalEntrySchema, many=True)

    @post_load
    @classmethod
    def build(cls, data, **kwargs):
        return cls(**data)
