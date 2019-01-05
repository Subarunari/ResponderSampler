import responder
from marshmallow import Schema, fields
import flask_sampler

openapi_params = {
    "title": "Sample API",
    "openapi": "3.0.0",
    "version": "1.0",
    "docs_route": "/docs"
}
api = responder.API(**openapi_params)

@api.route("/")
def index(req, resp):
    resp.text = "hello responder"


@api.schema("Echo")
class EchoSchema(Schema):
    message = fields.Str()

@api.route("/echo/{word}")
class Echo():
    """
    test docs
    ---
    get:
        description: echo back word.
        parameters:
            - name: word
              in: path
              schema:
                  type: string
        responses:
            200:
                description: return word
                schema:
                    $ref = "#/components/schemas/Echo"
    """
    def on_get(self, req, resp, *, word):
        resp.content = f"get {word}"

    def on_post(self, req, resp, *, word):
        resp.text = f"post {word}"

    def on_request(self, req, resp, *, word):
        resp.text = "call on request"

@api.route("/ws", websocket=True)
async def websocket(ws):
    await ws.accept()
    while True:
        name = await ws.receive_text()
        await ws.send_text(f"hello websocket")
    await ws.close()

@api.route("/template")
def get_template(req, resp):
    resp.content = api.template("index.html", word="Not Specified word parameter")

@api.route("/template/{word}")
def get_template(req, resp, *, word):
    resp.content = api.template("index.html", word=word)

api.mount("/flask", flask_sampler.app)

if __name__ == '__main__':
    api.run()