from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
app = Flask(__name__)
api = Api(app)

bot_post = reqparse.RequestParser()
bot_post.add_argument("name", type=str, help="Name is required...", required=True)
bot_post.add_argument("age", type=int, help="Age is required...", required=True)
bot_post.add_argument("position", type=str, help="Position is required...", required=True)

bot_put = reqparse.RequestParser()
bot_put.add_argument("name", type=str, help="Name is invalid...")
bot_put.add_argument("age", type=int, help="Age is invalid...")
bot_put.add_argument("position", type=str, help="Position is invalid...", store_missing=False)

bot = {}
def abort_if_not_exists(bot_id):
    if bot_id not in bot:
        abort(404, message="Could not find employee...")

def abort_if_exists(bot_id):
    if bot_id in bot:
        abort(409, message="Employee already exists...")

class Bots(Resource) :
    def get(self, bot_id):
        abort_if_not_exists(bot_id)
        return bot[bot_id]

    def post(self, bot_id):
        abort_if_exists(bot_id)
        args = bot_post.parse_args()
        bot[bot_id] = args
        return bot[bot_id], 201

    def put(self, employee_id):   #Update bots with ID
        abort_if_not_exists(bot_id)
        args = bot_put.parse_args()
        if "name" in args:
            bot[bot_id]["name"] = args["name"]
            if "age" in args:
                bot[bot_id]["age"] = args["age"]
            if "position" in args:
                bot[bot_id]["position"] = args["position"]
                return bot[bot_id]

    def delete(self, bot_id):
        abort_if_not_exists(bot_id)
        del bot[bot_id]
        return '', 204

api.add_resource(Bots, "/bot/<int:bot_id>")
if __name__ == "__main__":
    app.run(debug=True)
