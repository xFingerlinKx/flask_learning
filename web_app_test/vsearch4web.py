from flask import Flask
from flask import render_template
from flask import request

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


@app.route('/search4', methods=['GET', 'POST'])
def do_search():
    """
    Return the result of searching.
    :return: HTML
    """
    # 'request.form' --> ImmutableMultiDict([('phrase', 'qweqwe'), ('letters', 'a')])
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase, letters))

    return render_template(
        template_name_or_list='results.html',
        the_title=title,
        the_phrase=phrase,
        the_letters=letters,
        the_results=results,
    )


@app.route('/entry')
def entry_page():
    """
    Return the starting page.
    :return: HTML
    """
    return render_template(
        template_name_or_list='entry.html',
        the_title='Welcome to search4letters on the web!',
    )


if __name__ == '__main__':
    app.run(debug=True)
