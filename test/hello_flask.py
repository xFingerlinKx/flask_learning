from flask import Flask

app = Flask(__name__)


def search4vowels(phrase: str) -> set:
    """ Returns the set of vowels found in phrase """
    return set('aeiou').intersection(set(phrase))


def search4letters(phrase: str, letters: str='aeiou') -> set:
    """ Returns the set of letters found in phrase """
    return set(letters).intersection(set(phrase))


@app.route('/')
def hello() -> str:
    greeting_str = 'Hello world from Flask!'
    return greeting_str


@app.route('/search4')
def do_search() -> str:
    return str(search4letters('life, the universe, and everything!'))


app.run(debug=True)
