from flask import Blueprint,jsonify,request
from extensions import db
from models.models import Movies,CastMember,Director
from datetime import datetime
from schema import mov_schema,dir_schema

movie=Blueprint('movie',__name__)

# Creating a movie
@movie.route('/create_movie', methods=['POST'])
def create_movie():
    try:
        data = request.json
        name = data.get('name')
        release_date = data.get('release_date')
        director_id = data.get('director_id')
        cast = data.get('cast') 

        # Check if the movie already exists
        movie_exists = Movies.query.filter_by(name=name).first()
        if movie_exists:
            return jsonify({"message": "Movie already exists."})

        # Convert release_date to a datetime object (assuming it's in 'YYYY-MM-DD' format)
        release_date = datetime.strptime(release_date, '%Y-%m-%d')

        new_movie = Movies(name=name, release_date=release_date, director_id=director_id, cast=cast) 
        
        for cast_member_name in cast.split(','):
            cast_member = CastMember.query.filter_by(name=cast_member_name.strip()).first()
            if cast_member:
                new_movie.cast_members.append(cast_member)


        db.session.add(new_movie)
        db.session.commit()

        movie_data = {'id': new_movie.id, 'name': new_movie.name, 'release_date': new_movie.release_date, 'director_id': new_movie.director_id, 'cast': new_movie.cast} 

        response_data = {"movie": movie_data, "message": "Movie added successfully"}

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)})

#getting movie by id
@movie.route('/get_movie/<int:id>',methods=['GET'])
def get_movie(id):
     try:
          movie=Movies.query.get(id)
          if movie:
               return mov_schema.movie_schema.jsonify(movie)
          else:
                return jsonify({"success": False, "message": "Movie not found"})
        
     except Exception as e:
        return jsonify({"error": str(e)})
     
#getting movie by name
@movie.route('/get_movie/<string:name>', methods=['GET'])
def get_movie_by_name(name):
    try:
        movie = Movies.query.filter_by(name=name).first()

        if movie:
            return mov_schema.movie_schema.jsonify(movie)
        else:
            return jsonify({"success": False, "message": "Movie not found"})

    except Exception as e:
        return jsonify({"error": str(e)})
    
#getting movies by cast member
@movie.route('/get_movies_by_cast/<string:cast_member_name>', methods=['GET'])
def get_movies_by_cast(cast_member_name):
    try:
        # Query the database for the cast member by name
        cast_member = CastMember.query.filter(CastMember.name.ilike(cast_member_name)).first()


        if cast_member:
            # Get the list of movies associated with the cast member
            movies = [{'id': movie.id, 'name': movie.name, 'release_date': str(movie.release_date), 'director_id': movie.director_id, 'cast': movie.cast} for movie in cast_member.movies]
            return jsonify({"cast_member": cast_member_name, "movies": movies})
        else:
            return jsonify({"message": "Cast member not found"})

    except Exception as e:
        return jsonify({"error": str(e)})
    
#getting all movies
@movie.route('/get_all_movies',methods=['GET'])
def get_all_movies():
    all_movies=Movies.query.all()
    results=mov_schema.movies_schema.dump(all_movies)
    return jsonify(results)

#getting movies with same director
@movie.route('/get_details/<int:director_id>', methods=['GET'])
def get_details(director_id):
    director = Director.query.get(director_id)

    try:

        if director is None:
            return jsonify({"error": "Director not found"})

        director_data = dir_schema.director_schema.dump(director)
        movies = director.movies  

        if not movies:
            result = {
                "director": director_data,
                "movies": "No movies yet"
            }
        else:
            movies_data = mov_schema.movies_schema.dump(movies)
            result = {
                "director": director_data,
                "movies": movies_data
            }

        return jsonify(result)
    except Exception as e:
          return jsonify({"error": str(e)})
    
# updating movie by id 
@movie.route('/update_movie/<int:id>',methods=['PUT'])
def update_movie(id):
     try:
          movie=Movies.query.get(id)
          if movie:
            name=request.json['name']
            cast=request.json['cast']
            release_date=request.json['release_date']

            movie.name=name
            movie.cast=cast
            movie.release_date=release_date

            db.session.commit()

            return mov_schema.movie_schema.jsonify(movie)
          
          else:
               return jsonify({"message" : "movie not found"})
          

     except Exception as e:
          return jsonify({"error": str(e), "message": "An error occurred."}) 
     
#deleting a movie by id
@movie.route('/delete_movie/<int:id>', methods=['DELETE'])
def delete_movie(id):
    try:
        movie = Movies.query.get(id)
        if movie:
            db.session.delete(movie)
            db.session.commit()

            return jsonify({"message": "Movie deleted successfully"})
        else:
            return jsonify({"message": "Movie not found"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e), "message": "An error occurred."})
    
# updating movie by id 
@movie.route('/updating_movie/<int:id>',methods=['PUT'])
def updating_movie(id):
     try:
          movie=Movies.query.get(id)
          if movie:
            name=request.json['name']
            cast=request.json['cast']
            release_date=request.json['release_date']

            movie.name=name
            movie.cast=cast
            movie.release_date=release_date

            db.session.commit()

            return mov_schema.movie_schema.jsonify(movie)
          
          else:
               return jsonify({"message" : "movie not found"})
          

     except Exception as e:
            return jsonify({"error": str(e)})  

 # Endpoint to retrieve movies around a specific date
@movie.route('/get_movies_around_date', methods=['GET'])
def get_movies_around_date():
        try:
            start_date_str = request.args.get('start_date')
            end_date_str = request.args.get('end_date')

            # If both start_date and end_date are provided, retrieve movies between two dates
            if start_date_str and end_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

                movies = Movies.query.filter(Movies.release_date.between(start_date, end_date)).all()
            # If only start_date is provided, retrieve movies released after that date
            elif start_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')

                movies = Movies.query.filter(Movies.release_date >= start_date).all()
            # If only end_date is provided, retrieve movies released before that date
            elif end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

                movies = Movies.query.filter(Movies.release_date <= end_date).all()
            else:
            
                return jsonify({"error": "Invalid date parameters"})

            # Convert movies to JSON format
            movies_data = [{'id': movie.id, 'name': movie.name, 'release_date': str(movie.release_date), 'director_id': movie.director_id, 'cast': movie.cast} for movie in movies]

            return jsonify({"movies": movies_data})

        except Exception as e:
          return jsonify({"error": str(e)})