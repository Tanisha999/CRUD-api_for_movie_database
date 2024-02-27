from extensions import ma


class MoviesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'release_date', 'director_id','cast')

movie_schema = MoviesSchema()
movies_schema = MoviesSchema(many=True)