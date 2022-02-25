#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Boubacar Sow
# Created Date: Sun February 20 15:10:00  2022
# Copyright: Copyright 2022, Small Lexer, simple tokenizer
# =============================================================================
"""The Module Has Been Built do lexical analyse of c# very basic and simple programm"""
# =============================================================================


import lexer

if __name__ == '__main__':
    text = open("fichier_c_sharp.txt", 'r')
    if not text:
        print("Erreur")
        exit(0)
    result, table, error = lexer.run(text.read())
    print("---------Table des tokens-----------")
    print(result, '\n')
    if error:
        print("--------Erreur(s) de syntaxe---------")
        for err in error:
            print(err.as_string())

    print("\n--------TABLE DES SYMBOLES-------")
    for tab in table:
        print(tab)
    text.close()
