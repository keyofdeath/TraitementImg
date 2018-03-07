#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ImgOperator import *

if __name__ == "__main__":
    # operator3.add_oporation(ImgTranslation([[353, 56, 1], [550, 132, 1], [200, 308, 1], [417, 421, 1]],
    #                                        [[0, 0, 1], [200, 0, 1], [0, 250, 1], [200, 250, 1]]))

    # Coordoner x, y de la carte après extraction
    out_position = [[0, 0], [220, 0], [0, 310], [220, 310]]
    # Coordoner x, y de la carte dans la cameras
    img_poition = [[353, 56], [550, 132], [200, 308], [417, 421]]

    l, err = dlt(2, out_position, img_poition)

    print("Teste d'une dlt d'un point image en point objet: ")
    print(l)
    print("Taux erreu de la calibration")
    print(err)
    out_position_recronstruction = np.zeros((len(out_position), 2))
    for i in range(len(img_poition)):
        out_position_recronstruction[i, :] = dlt_reconstruction(2, 1, l, img_poition[i])

    print("Reconstruction des point objet")
    print(out_position_recronstruction)

    print("*******************************")

    print("Test d'une dlt d'un point objet vers un point image")

    midle_point_img = [381, 218]
    midle_point_out_position = [110, 155]

    l, err = dlt(2, img_poition, out_position)
    print(l)
    print("on donne un point objet est on regarde si cela corespon au point image")
    out_position_recronstruction = dlt_reconstruction(2, 1, l, midle_point_out_position)
    print("Point trouver")
    print(out_position_recronstruction)
    print("Point attendu")
    print(midle_point_img)
