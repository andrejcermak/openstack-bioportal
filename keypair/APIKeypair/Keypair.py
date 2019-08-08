from flask_restful import Resource
from VirtualMachineHandler import VirtualMachineHandler


class Keypair(Resource):

    def create(self, token, keyname, public_key):
        vh = VirtualMachineHandler(token)
        if vh.conn is None:
            return {"message": vh.STATUS}, 403
        try:
            keypair = vh.conn.compute.find_keypair(keyname)
            if not keypair:
                keypair = vh.conn.compute.create_keypair(
                    name=keyname, public_key=public_key
                )
                return keypair, 201
            elif keypair.public_key != public_key:
                vh.conn.compute.delete_keypair(keypair)
                keypair = vh.conn.compute.create_keypair(
                    name=keyname, public_key=public_key
                )
                return keypair, 200
            return keypair, 200
        except Exception as e:
            return {"message": "Import Keypair {0} error:{1}".format(keyname, e), "result": {}}, 400

    def update(self, token):
        return {}, 501

    def delete(self, token):
        return {}, 501

    def get(self, token, keypair_id):
        vh = VirtualMachineHandler(token)
        if vh.conn is None:
            return {"message": vh.STATUS}, 403
        keypair = vh.conn.compute.find_keypair(keypair_id)
        if keypair is None:
            return {}, 404
        return keypair, 200

    def list(self, token):
        vh = VirtualMachineHandler(token)
        if vh.conn is None:
            return {"message": vh.STATUS}, 403
        tmp = vh.conn.compute.keypairs()
        return [r for r in tmp], 200
