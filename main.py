#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import glob
import json
import urllib3
import codecs

import ImgOperator as io
from ImgOperator.Tool import get_4_point_contour
from MtgCardLib import *


def affiche_menu():
    """

    :return:
    """
    print("1) Télécharger un set de carte")
    print("2) Lancer le reconnaisance avec webCam")
    print("3) Lancer le reconnaisance avec une image")
    print("4) Maitre a jours la liste de carte")
    print("5) Quiter")


def choix():
    """
    Fonction qui demmande a l'utisateur d'entrer un numéro
    :return:
    """
    while True:
        c = input(">>>")
        # Traitement basique sur la chaine
        c = c.lower()
        c = c.strip()
        # pour retirer les character spéciaux
        c = ''.join(e for e in c if e.isalnum())
        try:
            c = int(c)
            return c
        except ValueError:
            print("Votre choix n'est pas valide")


def choix_str():
    """
    Fonction qui demmande a l'utisateur d'entrer une string
    :return:
    """

    c = input(">>>")
    return c.strip()


def get_local_set():
    """
    Affiche et propose a l'utilisateur de choisire un set de carte qui est sur sont ordinateur
    :return:
    """
    i = 1
    # on suprimme les .json
    list_set = [name.split('.')[0] for name in glob.glob("*.json")]
    try:
        list_set.remove("cardJson")
    except ValueError:
        pass
    if len(list_set) == 0:
        print("Il n'y a pas de set télécharger")
        return None

    for file in list_set:
        print("{}) {}".format(i, file))
        i += 1

    print("Quelle set voulez vous ?")
    while True:
        c = choix()
        try:
            return list_set[c - 1]
        except IndexError:
            print("Choix non valide")


def get_online_set():
    """
    Demmande a l'utilisateur qu'elle set de carte souhaite en ligne
    :return:
    """
    print("obtention de tout les set en ligne...")
    i = 1
    # on l'ouvre en utf8
    f = codecs.open("cardJson.json", 'r', 'utf-8')
    data = json.load(f)
    # on suprimme les .json
    list_set = [name.split('.')[0] for name in glob.glob("*.json")]
    online_list_set = list()
    # on affiche tout les set de disponible
    for k in data:
        # on ajoute que les set non telecharger
        if data[k]["name"].lower() not in list_set:
            online_list_set.append(data[k]["name"].lower())
            print("{}) {}".format(i, data[k]["name"].lower()))
            i += 1

    print("Le quelle voulez vous ?")
    while True:
        c = choix()
        try:
            return online_list_set[c - 1]
        except IndexError:
            print("get_online_set: Choix non valide")


def doawnload_set(cam_src):
    """
    Télécharge un set demander par l'utilisateur
    :param cam_src:
    :return:
    """
    print("***Téléchargement d'un set***")
    name = get_online_set()
    CardGet(name)


def update_json(cam_src):
    """
    Mais a jours le fichier json de tout les cartes
    :param cam_src:
    :return:
    """
    print("***Mise a jours de la liste des cartes***")
    http = urllib3.PoolManager()
    data = json.loads(http.request('GET', "http://mtgjson.com/json/AllSets.json").data)
    # on l'écrit en utf8 dans notre fichier
    out_json = codecs.open("cardJson.json", "w", "utf-8")
    json.dump(data, out_json)
    out_json.close()
    print("fin de la mise a jours")


def reco_cam(cam_src):
    """
    Lance une reconnaisance avec la webCame
    :param cam_src:
    :return:
    """

    print("***Reconnaisance avec une web cam***")
    set_name = get_local_set()
    if set_name is None:
        return
    c = CardGet(set_name)
    cap = cv2.VideoCapture(cam_src)
    print("Pour quiter taper q")
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        screenCnt = get_4_point_contour(frame)
        try:
            if screenCnt is not None:
                operator3 = io.ImgOprerator(frame)
                operator3.add_oporation(io.ImgTranslation(screenCnt))
                wrap = operator3.img
                cv2.imshow("wrap", wrap)
                card_info = c.recognize_card(wrap)["name"]
                font = cv2.FONT_HERSHEY_PLAIN
                cv2.putText(frame, card_info, (int(screenCnt[1][0] / 2) + 50, int(screenCnt[2][1] / 2)), font, 1,
                            (255, 255, 255), 1, cv2.LINE_4)
                cv2.imshow('img', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        except Exception as e:
            print(e)


def reco_img(cam_src):
    """
    Lance une reconnaissance avec une image
    :param cam_src:
    :return:
    """

    print("***Reconnaisance avec une image***")
    print("Entrer le chemin vers l'image a reconnaitre:")
    chemin_img = choix_str()
    img = cv2.imread(chemin_img)
    while img is None:
        print("reco_img: Le chemin donnée n'est pas valide")
        chemin_img = choix_str()
        img = cv2.imread(chemin_img)

    set_name = get_local_set()
    if set_name is None:
        return
    c = CardGet(set_name)
    screen_cont = get_4_point_contour(img)

    if screen_cont is not None:
        trans = io.ImgTranslation(screen_cont)
        wrap = trans.apply(img)
        cv2.imshow("Transform result", wrap)
        card_info = c.recognize_card(wrap)["name"]
        print(card_info)
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(img, card_info, (int(screen_cont[1][0] / 2) + 50, int(screen_cont[2][1] / 2)), font, 1,
                    (255, 255, 255), 1, cv2.LINE_4)
        print("Pour quiter taper q")
        cv2.imshow("Card found", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("reco_img: Impossible de trouver ma carte dans l'image")


def quiter(cam_src):
    """

    :param cam_src:
    :return:
    """
    exit(0)


def menu(cam_src):
    """
    Programme principale
    :param cam_src: Source de la caméra
    :return:
    """
    choix_possible = {1: doawnload_set, 2: reco_cam, 3: reco_img, 4: update_json, 5: quiter}
    while True:
        affiche_menu()
        try:
            # on demmande a l'utilisateur un choix est on l'éxécute
            choix_possible[choix()](cam_src)
        except KeyError as e:
            print(e)
            print("Manu: Votre choix n'est pas valide")


if __name__ == "__main__":
    menu(1)
