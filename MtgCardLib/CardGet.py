#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
import json
import urllib.request
import cv2
import numpy as np
import imagehash
from PIL import Image
import pickle


def hash(image):
    """
    Hash l'image donnée dois entre en forma opencv
    :param image:
    :param hashSize:
    :return:
    """
    try:
        # on transform l'image BGR en RGB pour que image hash puisse traiter cette image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return imagehash.phash(Image.fromarray(image))
    except Exception as e:
        print("Error! MtgHasing, hash,: ", e)


def download_and_hash(multiverseid):
    resp = urllib.request.urlopen(
        'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid={}&type=card'.format(multiverseid))
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return hash(image)


class CardGet(object):

    def __init__(self, set_name):

        # Traitement basique sur la chaine
        set_name = set_name.lower()
        set_name = set_name.strip()

        if os.path.exists("{}.json".format(set_name)):
            print("Set found in path")
            f = codecs.open("{}.json".format(set_name), 'r', 'utf-8')
            self.card_set = json.load(f)
        else:
            print("Set n'a pas été trouver dans vos fichier..")
            self.__get_json_set(set_name)
            self.__set_set_img_hash()
            # on l'écrit en utf8 dans notre fichier
            out_json = codecs.open("{}.json".format(set_name), "w", "utf-8")
            json.dump(self.card_set, out_json)
            out_json.close()

    def __set_set_img_hash(self):

        print("Get the image hash")
        nb_card = len(self.card_set["cards"])
        card_cc = 1
        for card in self.card_set["cards"]:
            print("Get img of the card {} / {}".format(card_cc, nb_card))
            try:
                if card.get("multiverseid"):
                    multiverseid = int(card.get("multiverseid"))
                    hash = download_and_hash(multiverseid)
                    card["hash"] = codecs.encode(pickle.dumps(hash), "base64").decode()
            except Exception as e:
                print("Error! __set_set_img_hash, multiverseid to int ", e)
            card_cc += 1

    def __get_json_set(self, set_name):

        # on l'ouvre en utf8
        f = codecs.open("cardJson.json", 'r', 'utf-8')
        data = json.load(f)
        # on controle que le set donner existe si oui on recupaire le clef du set demander
        set_key = list(filter(lambda k: data[k]["name"].lower() == set_name, data))
        if len(set_key) == 0:
            print("Set")
            raise ValueError("Le set donner n'existe pas ou n'a pas été trouver")
        dic_set = data[set_key[0]]

        self.card_set = dic_set

    def recognize_card(self, img):

        code_hash = hash(img)
        # on tri notre liste de carte en fonction de la distance de hamming
        # pickle.loads(codecs.decode(c["hash"].encode(), "base64") permert de transformer une string en un objet
        # image hash
        return sorted(self.card_set["cards"], key=lambda c: abs(pickle.loads(codecs.decode(c["hash"].encode(),
                                                                                           "base64")) - code_hash))[0]


if __name__ == "__main__":
    pass
