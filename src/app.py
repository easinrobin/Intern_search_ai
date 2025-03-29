from flask import Flask, request, render_template_string
from search import search_products

app = Flask(__name__)

HTML = """
<form method="POST">
    <input name="query" placeholder="Enter your search intent (e.g., Amazon brand blue tent under $500)">
    <input type="submit" value="Search">
</form>
{% if results %}
    <h3>Results:</h3>
    <ul>
    {% for r in results %}
        <li>{{ r['Title'] }} - {{ r['Brand'] }} - ${{ r['Price'] }} ({{ r['Main_Category'] }}, Rating: {{ r['Average_Rating'] }})</li>
    {% endfor %}
    </ul>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def home():
    results = None
    if request.method == "POST":
        query = request.form["query"]
        results = search_products(query)
    return render_template_string(HTML, results=results)

if __name__ == "__main__":
    app.run(debug=True)