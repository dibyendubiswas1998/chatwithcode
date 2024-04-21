from src.chatwithcode.utils.common_utils import log
from src.chatwithcode.pipeline.chat_with_code import ChatWithCode
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)
log_file = "logs/logs.log"

@app.route("/")
def Home():
    """
        Renders the "index.html" template for the root URL ("/") in a Flask application.

        Returns:
            str: The rendered "index.html" template.
    """
    try:
        return render_template('index.html')
    except Exception as ex:
        log(file_object=log_file, log_message=f"error will be {ex}")
        raise ex
    finally:
        return render_template('index.html')




@app.route("/get_url", methods=['POST', 'GET'])
def embedding_process():
    """
        Process a GitHub repository URL and return a success message.

        Args:
            request (flask.Request): The Flask request object that contains the POST data.

        Returns:
            str: The rendered index.html template with the success message.

        Raises:
            Exception: If an error occurs during processing.
    """
    try:
        sms = None
        pro = ChatWithCode()
        if request.method == 'POST':
            git_url = request.form["url"]
            res = pro.process(url=git_url)
            if res:
                sms=res
        return render_template("index.html", sms=sms)

    except Exception as ex:
        log(file_object=log_file, log_message=f"error will be {ex}")
        raise ex
    finally:
        return render_template("index.html", sms=sms)


@app.route('/ask', methods=['POST'])
def generate_response():
    """
        Generate a response to a question received via a POST request.

        Args:
            None

        Returns:
            dict: A JSON object containing the generated answer.

        Raises:
            Exception: If an error occurs during the generation of the response.
    """
    try:
        data = request.get_json()  # Get the JSON data from the request
        question = data.get("question")  # Extract the question from the JSON data

        # get the response:
        pro = ChatWithCode()
        answer = pro.predict(question=question)
        return jsonify({"answer": answer})  # Return the answer as JSON

    except Exception as ex:
        log(file_object=log_file, log_message=f"error will be {ex}")
        raise ex





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)