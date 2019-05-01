from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)


class Chatbot():

	def __init__(self):
		self.file = None
		self.dataframe = pd.DataFrame()
		self.conversation = ""

	def add_file(self, file, delimiter=';'):
		self.file = file
		self.dataframe = pd.read_csv(file, delimiter=delimiter, header=None)
		print(self.dataframe)
		self.dataframe.columns = ["User", "Chatbot"]

	def user_says(self, statement):
		self.conversation += "<p><b>User</b>: "+statement+"</p>"
		found_answer = False
		for index, row in self.dataframe.iterrows():
			print(row, statement.upper())
			if row["User"].upper() == statement.upper():
				response = row["Chatbot"]
				found_answer = True
		if found_answer:
			self.conversation += "<p><b>Chatbot</b>: "+response+"</p>"
		else:
			self.conversation += "<p><b>Chatbot</b>: Je ne connais pas la réponse.</p>"
		return self.conversation



chatbot = Chatbot()

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/read_file", methods=["GET", "POST"])
def read_file():
	print("GOT IT")
	file = request.files['file']
	print("GOT IT")
	chatbot.add_file(file, delimiter=';')
	return redirect(url_for("process"))


@app.route("/process", methods=["GET", "POST"])
def process():
	if request.method == "POST":
		return render_template("conversation.html", html_dialogue=chatbot.user_says(request.form["user_input"]))

	else:
		return render_template("conversation.html", html_dialogue=chatbot.conversation)





if __name__ == '__main__':
	app.run(thread=True)