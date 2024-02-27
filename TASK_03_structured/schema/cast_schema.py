from extensions import ma


class CastMemberSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')





cast_schema = CastMemberSchema()