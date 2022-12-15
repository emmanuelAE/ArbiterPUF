import random
import socket
from threading import Thread
from time import sleep
import compress_pickle
from model.ArbiterPUF import ArbiterPUF


class client:
    def __init__(self, puf, id):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.puf = puf
        self.id = id

    # def noisemaker(self, bit):
    #     _probability = random.random()
    #     if _probability <= 1:
    #         return 1 - bit
    #     return bit

    def create_random_challenge(self, nb_of_bit):
        challenge = []
        for i in range(nb_of_bit):
            challenge.append(random.randint(0, 1))
        return challenge

    def send_msg(self, manuel_input="No", data=None):
        if manuel_input == "Yes":
            while True:
                msg = input()
                msg = msg.encode('utf-8')
                self._socket.send(msg)
        else:
            self._socket.send(compress_pickle.dumps(data, compression="gzip"))

    def receive_msg(self):
        while True:
            data = self._socket.recv(5000)
            data = compress_pickle.loads(data, compression="gzip")
            if data["request_type"] == "id_request":
                print("server : ", data["message"])
                print("client :  Sending my id")
                self.send_msg(data={"request_type": "id_request", "id": self.id})

            elif data["request_type"] == "enrolment_request":
                print("server : ", data["message"])
                print("client :  Sending my CRPs for enrollment")

                challenge = self.create_random_challenge(64)
                response = self.puf.challenge(challenge)
                # print("response : ", response)
                response_vector = []
                for i in range(data["number_of_response"]):
                    # response_vector.append(self.noisemaker(response))
                    response_vector.append(response)

                self.send_msg(data={"request_type": "enrolment_request", "id": self.id, "challenge": challenge,
                                    "response_vector": response_vector})
            # Authentication
            elif data["request_type"] == "authentication":
                print("server : ", data["message"])
                print("client :  Authenticating ...")
                response_vector = []
                for i in range(int(data["number_of_response"]) + 1):
                    # response_vector.append(self.noisemaker(self.puf.challenge(data["challenge"])))
                    response_vector.append(self.puf.challenge(data["challenge"]))

                self.send_msg(
                    data={"request_type": "authentication", "id": self.id, "response_vector": response_vector})

            elif data["request_type"] == "ask_for_response_vector":
                print("server : ", data["message"])
                response_vector = []
                for i in range(int(data["number_of_response"]) + 1):
                    # response_vector.append(self.noisemaker(self.puf.challenge(data["challenge"])))
                    response_vector.append(self.puf.challenge(data["challenge"]))

                self.send_msg(data={"request_type": "authentication", "id": self.id,
                                    "response_vector": response_vector})

            elif data["request_type"] == "authentication_result":
                print("server : ", data["message"])
                # self.send_msg(data={"request_type": "authentication_result", "id": self.id, "message": "close"})
            else:
                print("WHAT !!!!!!!!!!!!!!")
            # sleep(3)

    def run(self):
        host = "localhost"
        port = 8081

        self._socket.connect((host, port))
        Thread(target=self.receive_msg).start()  # , args=[socket])

        # envoi.start()
        print("client :  Asking for the best developers ever")

        self.send_msg(data={"request_type": "init_comm", "message": "coucou"})


puf_1 = ArbiterPUF(64)
my_client = client(puf=puf_1, id=7)
my_client.run()

sleep(30)
print("\n\n")
print("I'm the same client but 100 years later so my ArbiterPUF is a little old ;)\n")

puf_1.aging()
my_client2 = client(puf=puf_1, id=7)
my_client2.run()
