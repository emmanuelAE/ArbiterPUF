from time import sleep

import compress_pickle
from threading import Thread, Lock
import socket


class Server:
    def __init__(self, host, port):
        self.port = port
        self.host = host
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((host, port))
        self._socket.listen(10)
        self._lock = Lock()
        self._number_of_response = 1001

        # self._connection_list = []
        self._client_list = []

    def _vote(self, response_list):
        return 1 if sum(response_list) > int(len(response_list) / 2) else 0

    def _close_connection(self):
        while True:
            close_answer = input("Write 'CLOSE' if you want close the connection\nAlways close before exit\n")
            if "OSE" in close_answer or "ose" in close_answer:
                break

    def authentication(self, client, known_client="No", data=None):
        good_response_percent = 0
        try:
            if known_client == "No":
                for bit in data["response_vector"]:
                    if bit == [_tuple[2] for _tuple in self._client_list if _tuple[0] == data["id"]][0]:
                        good_response_percent += 1
                good_response_percent = (good_response_percent / len(data["response_vector"])) * 100

                if good_response_percent > 80:
                    self.send_msg(client=client, data={"request_type": "authentication_result",
                                                       "message": "Authentication succeeded\n          The best "
                                                                  "developers "
                                                                  "ever "
                                                                  "are\n         -> ABO Emmanuel\n         -> "
                                                                  "KAMIDJIGHA Mounya"})
                else:
                    self.send_msg(client=client, data={"request_type": "authentication_result",
                                                       "message": "Authentication failed\n          Closing "
                                                                  "the connection, you are "
                                                                  "an "
                                                                  "imposter !!!!!!!!!!!!!!!!!!!!!!!!!!!"})
        except Exception as e:
            print(e)
            challenge = [_tuple[1] for _tuple in self._client_list if _tuple[0] == data["id"]][0]
            self.send_msg(client=client, data={"request_type": "ask_for_response_vector", "challenge": challenge,
                                               "number_of_response": self._number_of_response,
                                               "message": "You are in my database, skipping enrollment, starting the "
                                                          "authentication ..."})
        return True

    def send_msg(self, client, manuel_input="No", data=None):
        if manuel_input == "Yes":
            while True:
                user_input = input()
                if user_input == "CLOSE":
                    self._socket.close()
                data = {"request_type": "server_admin_input", "message": user_input}
                client.send(compress_pickle.dumps(data, compression="gzip"))
        else:
            client.send(compress_pickle.dumps(data, compression="gzip"))

    def receive_msg(self, client, lock):
        while True:
            # lock.acquire()
            data = client.recv(5000)
            data = compress_pickle.loads(data, compression="gzip")
            if data["request_type"] == "id_request":
                if data["id"] in [_tuple[0] for _tuple in self._client_list]:
                    _ = self.authentication(client, data=data)
                else:
                    self.send_msg(client=client, data={"request_type": "enrolment_request",
                                                       "message": "Send your ArbiterPUF instance for enrollment",
                                                       "number_of_response": self._number_of_response})
            # enrollment
            elif data["request_type"] == "enrolment_request":
                self._client_list.append((data["id"], data["challenge"], self._vote(data["response_vector"])))
                self.send_msg(client=client,
                              data={"request_type": "authentication",
                                    "challenge": [_tuple[1] for _tuple in self._client_list if _tuple[0] == data["id"]][
                                        0],
                                    "number_of_response": self._number_of_response / 10,
                                    "message": "Enrollment succeeded reconnect please"})

                # client.close()
            elif data["request_type"] == "authentication":
                _ = self.authentication(client, data=data)

            elif data["request_type"] == "ask_for_response_vector":
                self.authentication(client)

            else:
                self.send_msg(client=client, data={"request_type": "id_request",
                                                   "message": "Are you new here? What's your id"})
            # lock.release()
            sleep(4)

    def wait_connection(self):
        while True:
            client, ip = self._socket.accept()
            print(client)
            print("the client", ip, "is connected")
            Thread(target=self.receive_msg, args=(client, self._lock)).start()

            # Thread(target=self.print_hello, args=(i,)).start()
            # receive_thread.start()
            # i+=1

    def run(self):
        close_thread = Thread(target=self._close_connection)
        wait_thread = Thread(target=self.wait_connection)

        close_thread.start()
        wait_thread.start()

        close_thread.join()
        # wait_thread.join()

        # client.close()
        self._socket.close()
        exit(0)


#
my_server = Server("localhost", 8080)
my_server.run()
