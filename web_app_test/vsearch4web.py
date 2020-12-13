from flask import Flask
from flask import render_template
from flask import request
from flask import escape
# from flask import redirect

app = Flask(__name__)


# @app.route('/')
# def redirect_to_entry():
#     """
#     Redirecting to '/entry' location.
#     :return: code=302
#     """
#     return redirect(location='/entry')
def search4vowels(phrase: str) -> set:
    """ Returns the set of vowels found in phrase """
    return set('aeiou').intersection(set(phrase))


def search4letters(phrase: str, letters: str='aeiou') -> set:
    """ Returns the set of letters found in phrase """
    return set(letters).intersection(set(phrase))


def log_request(request, res: str) -> None:
    """
    Write request and the results in 'vsearch.log'.

    :param request: request obj
    :param res: result of request
    :return: None
    """
    with open('vsearch.log', 'a') as log:
        print(request.form, request.remote_addr, request.user_agent, res, file=log, sep='|')


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

    log_request(request=request, res=results)

    return render_template(
        template_name_or_list='results.html',
        the_title=title,
        the_phrase=phrase,
        the_letters=letters,
        the_results=results,
    )


@app.route('/')
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


@app.route('/viewlog')
def view_log_file() -> str:
    """
    Return the contents of the log file in HTML table.

    :return: {HTML} contents of the log file.
    """
    contents = []

    with open('vsearch.log') as log:
        for line in log.readlines():
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))

    titles = ('Form Data', 'Remote addr', 'User agent', 'Results')

    return render_template(
        template_name_or_list='log.html',
        the_title='The log file results',
        the_row_titles=titles,
        the_data=contents,
    )


if __name__ == '__main__':
    app.run(debug=True)
