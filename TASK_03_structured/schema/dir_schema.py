from extensions import ma

class DirectorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'age', 'gender')


director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)