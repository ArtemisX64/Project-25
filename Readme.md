# (WLEGS)[Vee-Legs] Wikipedia Linked Entity Generation System
This is an attempt to generate entities from *Wikipedia.org* articles. Also, it has a parser that can save the derived entities in a .csv    

## Instructions
- Run python src/parser.py 
- Run python src/trainer.py
- python test.py

## Usage
```
python src/parser.py -- To create a train data using wikipedia
python src/trainer.py -- To train model
python src/backend.py -- To run the backend with server
``` 
**PASS `wiki` to train using wiki and run server using wiki**
*eg:*
`python src/parser.py "Donald Trump"`
`python src/backend.py wiki`
`python src/trainer.py wiki`


## Dependencies
`pip install spacy pandas wikipedia-api flask python-dotenv tqdm matplotlib`
