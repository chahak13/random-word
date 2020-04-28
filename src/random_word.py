import random
from flask import Flask, url_for, request, jsonify


def create_app():
    app = Flask(__name__)

    with open("./words.txt", "r") as f:
        word_list = f.read().splitlines()

    word_set = set(word_list)
    del word_list
    word_dict = dict(zip(range(len(word_set)), word_set))
    del word_set

    @app.route("/word", methods=["GET"])
    def generate_word():
        """Generate random words.

        This function generates a list of random words of length
        provided by the user (default=1). The function uses the value
        for 'number' passed as an argument in the url and returns a
        JSON response with the words as an array stored in the value of
        the 'data' key of the response.

        Usage:
            /word : Returns a sinlge word. The response will be of the
            type
                {
                    "data": [
                        "expeller"
                    ],
                    "status": 200
                }

            /word?number=2 : Returns an array of words equal to number
            passed. Response will look like
            {
                "data": [
                    "expeller",
                    "sample"
                ],
                "status": 200
            }

        """
        indices = random.sample(
            range(len(word_dict)), int(request.args.get("number", 1))
        )
        response_json = jsonify(
            {
                "data": [word_dict[index] for index in indices],
                "status": 200,
            }
        )
        return response_json

    with app.test_request_context():
        print(url_for("generate_word", number=3))

    return app


if __name__ == "__main__":
    create_app().run("0.0.0.0", port=9000, debug=True)
