# coding: utf-8
from flask import Flask
import random,json
from flask_restful import Api, Resource, reqparse
players_api=Flask(__name__)
api=Api(players_api)

players=json.load(open('players_test.json','rt'))

class Players(Resource):
    def get_id(self,params):
        clubAlias=''.join([word[0].upper() for word in params["club"].split()])
        return params["name"].lower()+'_'+clubAlias

    def return_player_ind(self,id):
        for ind,player in enumerate(players):
            if player["id"]==id:
                return ind
        
    def get(self,id=""):
        if id=="":
            return players,200
        ind=self.return_player_ind(id)
        if ind:
            return players[ind],200
        else:
            return f"Player {id} not found", 404

    # for new entries
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("score")
        parser.add_argument("gender")
        parser.add_argument("club")
        
        params=parser.parse_args()

        if any(paramVal is None for paramVal in params.values()):
            return f"all entries need to be filled"

        id=self.get_id(params)
        
        ind=self.return_player_ind(id)
        if ind:
            return f"Player with id {id} (name: {params['name']}, club: {params['club']}) already exists",400
        
        player={
            "id":id,
        "name":params["name"],
                "score": float(params["score"]),
                "gender": params["gender"],
                "club": params["club"]
                }
        players.append(player)
        json.dump(players,open('players_test.json','wt'),indent=2)
        return player,201

    # for updates of scores
    def put(self):
        parser=reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("score")        
        
        params=parser.parse_args()

        if any(paramVal is None for paramVal in [params["id"],params["score"]]):
            return f"id and score need to be filled"

        print(params["id"])
        print(params["score"])
        ind=self.return_player_ind(params["id"])
        if not ind:
            return f"no player with that id exists"
        playerToUpdate=players[ind]
        playerToUpdate["score"]=float(params["score"])
        players[ind]=playerToUpdate
        json.dump(players,open('players_test.json','wt'),indent=2)

        return playerToUpdate, 201
    
    def delete(self,id):
        global players
        #players=[player for player in players if player["id"]!=id]
        ind=self.return_player_ind(id)
        if not ind:
            return f"{id} does not exist"
        
        players=players[:ind]+players[ind+1:]
        json.dump(players,open('players_test.json','wt'),indent=2)

        return f"Player with id {id} is deleted",200
        
api.add_resource(Players,"/players","/players/","/players/<id>")

if __name__=='__main__':
    players_api.run(debug=True)
