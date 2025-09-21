Steps to run this file on local host:

Prerequisites : Install all recommended packages listed in requirements.txt file.

How to start the project :

OPTION 1 : Use run.bat file to open with just a double click(for Windows OS)

OPTION 2 : Use start_project.py file to start the server(Prefered option)

OPTION 3 : Run this command on command line "python manage.py runserver"

This command will run a local server with settings listed in manage.py file and supports hot reload.
This command will not redirect you to the web browser thus one needs to open the web browser manually.

Run this command if you dont want hot reload feature: python manage.py runserver --noreload

Screeenshots:

Home Page:

![Error in loading image. Plese visit screenshots folder](<Screenshots/Home page.png>)

Searching a movie:

![Error in loading image. Plese visit screenshots folder](<Screenshots/Searching a movie.png>)

Result Page:

![Error in loading image. Plese visit screenshots folder](<Screenshots/Result Page.png>)

Navigation Menu:

![Error in loading image. Plese visit screenshots folder](<Screenshots/Navigation menu.png>)

Result Not Found:

![Error in loading image. Plese visit screenshots folder](<Screenshots/Unfound message.png>)

Footer:

![Error in loading image. Plese visit screenshots folder](<Screenshots/Footer links.png>)

Recommendation Algorithm:

This project uses a content-based recommendation algorithm to suggest movies similar to a user-inputted movie. The algorithm employs a "soup-based" approach, combining movie metadata into a single text representation for similarity computation.

Working:
Soup Creation: Combines movie metadata (e.g., genres, plot, cast, director) into a single text string ("soup") per movie.
Text Preprocessing: Cleans the soup by lowercasing, removing stop words, and optionally stemming words for consistency.
Feature Extraction: Converts soups into numerical vectors using TF-IDF to weigh terms by importance.
Similarity Computation: Calculates cosine similarity between the input movie’s vector and others to measure likeness.
Recommendation Output: Ranks movies by similarity score and returns the top matches.

Advantages of this algorithm:
- Cold start friendly.
- Easy to interpret and implement.

Disadvantages of this algorithm:
- Model's effectiveness depends on metadata.
- Ignores user prefrences and watch history.
- Scalability issues.
