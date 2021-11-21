import logging
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import matplotlib.pyplot as plt
import random
import requests
from bs4 import BeautifulSoup as bs
import re
import string
import Graph
import numpy as np
from fractions import Fraction as frac

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def start(update, context):
    logger.info('El usuario ha iniciado el bot')
    name = update.message.chat["first_name"]
    update.message.reply_text(f"""¡Bienvido {name} &#x1F44B! Un gusto tenerte por aca &#x1F601

Si desea obtener mas informacion sobre las funciones de este BOT&#x1F916 digite /ayuda &#x1F575
  """, parse_mode="HTML")
    logger.info("Saludo enviado")


def ayuda(update, context):
    logger.info("El usuario solicito ayuda")
    options = [
        [InlineKeyboardButton("Saludo", callback_data="m1")],
        [InlineKeyboardButton("Grafo", callback_data="m2")],
        [InlineKeyboardButton("Secuencia", callback_data="m3")],
        [InlineKeyboardButton("Recibir imagen", callback_data="m4")],
        [InlineKeyboardButton("Recibir documentos", callback_data="m5")],
    ]
    reply_markup = InlineKeyboardMarkup(options)
    update.message.reply_text("Hola,&#x1F44B bienvenido al menu de ayuda.", parse_mode="HTML")
    update.message.reply_text("Seleccione el comando del que desea información &#x1F44C", parse_mode="HTML",
                              reply_markup=reply_markup)


def resolverRR(cf, cb):
    r = np.roots(cf)
    k = len(cb)
    mr = np.zeros((k, k))
    for i in range(0, k):
        l = 0
        for j in r:
            mr[i, l] = j ** (i)
            l += 1

    b = np.linalg.lstsq(mr, cb, rcond=None)[0]
    sol = ""
    for i in range(0, len(b)):
        if i != 0:
            sol = sol + "+" + str(frac(b[i]).limit_denominator()) + "*" + str(frac(r[i]).limit_denominator()) + "^n"
        else:
            sol = sol + str(frac(b[i]).limit_denominator()) + "*" + str(frac(r[i]).limit_denominator()) + "^n"

    print(sol)

    return r"f_n = 2^{n-1}"


def secuencia(update, context):
    logger.info("El usuario enviará una secuencia de numeros...")
    text = update.message.text
    text = text.replace("/secuencia", "").strip()
    try:
        sec = eval(text)
        r = np.roots(sec)
        dic = {}
        for raiz in r:
            if raiz not in dic.keys():
                dic[raiz] = 1
            else:
                dic[str(raiz)] += 1

        j = 1
        f = ""
        for ra in r:
            for i in range(0, dic[ra]):
                if j > 1:
                    f = f + "+c_" + str(i + j) + "*n^" + str(i) + "*" + str(frac(ra).limit_denominator()) + "^n"
                else:
                    f = f + "c_" + str(i + j) + "*n^" + str(i) + "*" + str(frac(ra).limit_denominator()) + "^n"
            j += 1

        print(f)
    except Exception as e:
        logger.info("Error")
        print(e)


def rr(update, context):
    logger.info("El usuario enviará una relacion de recurrencia...")
    text = update.message.text
    text = text.replace("/rr", "").strip()
    try:
        sec = eval(text)  # Convertimos los parámetros de entrada en una tupla.

        cof = sec[0]
        cb = sec[1]

        resultado = resolverRR(cof, cb)

        """
        resultado = resolverRR(sec,(0,1),1)
        fn = f"${resultado}$"
        fig = plt.figure(figsize=[((len(fn) / 2) * 0.15), 1], dpi=200)
        fig.text(0.5, 0.5, x, horizontalalignment='center',verticalalignment='center', fontsize='xx-large', wrap=True)
        fig.savefig("src/images/solucion_rr.png")
        plt.clf()
        plt.close()
        update.message.reply_text(resultado)
        img = open("src/images/solucion_rr.png", "rb")
        chat_id = update.message.chat.id
        update.message.bot.sendPhoto(chat_id=chat_id, photo=img)"""
    except Exception as e:
        print(e)
        logger.info("Ha ocurrido un error enviando la secuencia...")
        update.message.reply_text(
            "Lo sentimos, los parámetros de la secuencia deben ser números.\nRevise la documención del Bot: /help.")


def markov(update, context):
    name = update.message.chat.first_name
    logger.info(f"El usuario {name} quiere generar una cadena de markov")
    markov_info = update.message.text
    markov_info = markov_info.replace("/markov", "").strip()
    valores = markov_info.split(",")
    if len(valores) > 2 or len(valores) < 2:
        update.message.reply_text("El numero de parametros no es el indicado")
    else:
        url = valores[0]
        n = valores[1]
        if "wikipedia.org" in url and url.startswith("https://"):
            page = requests.get(url)
            soup = bs(page.content, "html.parser")
            parrafos = soup.find_all("p")
            texto = []

            for parrafo in parrafos:
                texto.append(parrafo.getText())

            text = "".join(str(texto))
            text = clean_text(text)

            update.message.reply_text("La cadena generada es:")
            update.message.reply_text(generar_cadena(text, n))
            logger.info("Cadena enviada")

        else:
            update.message.reply_text("El formato del enlace no es el indicado")


def generar_cadena(text, n):
    letras = list(text)
    dic = {}
    for letra in letras:
        if letra not in dic.keys():
            dic[letra] = 1
        else:
            dic[letra] += 1

    freqa = 0
    for llave in dic.keys():
        freq = dic[llave] / len(letras)
        freqa += freq
        dic[llave] = [freq, freqa]

    s = ""
    for n in range(0, int(n)):
        r = random.random()
        for llave in dic.keys():
            (a, b) = dic[llave]
            ant = b
            if ant == b:
                if r <= ant:
                    s = s + llave
                    break
            else:
                if r > ant and r <= b:
                    s = s + llave
                    break

    return s


def grafo(update, context):
    name = update.message.chat.first_name
    logger.info(f"El usuario {name} quiere generar un grafo")
    grafo_info = update.message.text
    grafo_info = grafo_info.replace("/grafo", "")
    try:
        valores = eval(grafo_info)
        if len(valores) > 3 or len(valores) < 3:
            update.message.reply_text("Los parametros superan a los esperados")
        else:
            # []
            vertices = valores[0]
            aristas = valores[1]
            grado = valores[2]
            update.message.reply_text(
                f"Sus parametros son:\n\n1\. *Numero de vertices:* {vertices}\n2\. *Numero de aristas:* {aristas}\n3\. *Grado:* {grado} ",
                parse_mode="MarkdownV2")
            max = vertices * (vertices - 1) / 2
            if (aristas > max):
                update.message.reply_text("El numero de aristas excede al maximo posible")
                logger.info("Ocurrio un error con el numero de aristas")
            else:
                Graph.graficar(vertices, aristas, grado)
                img = open("src/images/grafo.png", "rb")
                chat_id = update.message.chat.id
                update.message.bot.sendPhoto(chat_id=chat_id, photo=img)
    except Exception as e:
        logger.info("Ha ocurrido un error generando un grafo")
        update.message.reply_text("Lo sentimos ha ocurrido un error. Intente de nuevo y revise los paramentros")
        print(e)


def send_doc(query, path):
    logger.info("El usuario ha solicitado un documento")
    chat_id = query.message.chat.id
    doc = open(path, "rb")
    query.message.reply_text("Cargando documento, por favor espere")
    query.bot.sendDocument(chat_id=chat_id, document=doc, timeout=300)


def send_image(query):
    logger.info("El usuario ha solicitado una imagen")
    chat_id = query.message.chat.id
    img = open("src/images/uninorte.jpg", "rb")
    query.message.reply_text("Cargando imagen, por favor espere")
    query.bot.sendPhoto(chat_id=chat_id, photo=img, timeout=120)


def saludo(query):
    name = query.message.chat.first_name
    logger.info(f"El usuario {name} solicito un saludo")
    query.message.reply_text(f"Hola, {name} &#x1F44B . Un gusto tenerte por aca &#x1F601 .", parse_mode="HTML")


def help_grafo(query):
    name = query.message.chat.first_name
    logger.info(f"El usuario {name} solicito ayuda sobre el comando grafo")
    info = f"""
  Bienvenido {name} a continuacion se ve a explicar como generar un grafo y los atributos que se necesitan\.
    
  \- E: Numero de aristas\.
  \- V: Numero de vertices\.
  \-K: Grado maximo del grafo\.
    
  Para correr este comando debes escribir:
  /grafo E,V,K
    
  *Ejemplos*
  1\. /grafo \[1,2,3\]
  2\. /grafo \(1,2,3\)
  3\. /grafo 1,2,3   
    
  """
    query.message.reply_text(info, parse_mode="MarkdownV2")


def help_sec(query):
    name = query.message.chat.first_name
    logger.info(f"El usuario {name} solicito ayuda sobre el comando secuencia")
    info = f"""
  Bienvenido {name} a continuacion se ve a explicar como resolver una relacion de recurrencia y los atributos que se necesitan\.

  \- RR: Coeficientes de la relacion de recurrencia normalizada\.

  Para correr este comando debes escribir:
  /secuencia RR

  *Ejemplos*
  1\. /secuencia \[1,2,3,4,5\]
  2\. /secuencia \(1,2,3\)
  3\. /secuencia 1,2   

  """
    query.message.reply_text(info, parse_mode="MarkdownV2")


def clean_text(text: str):
    text = re.sub(r"\\n", "", text)
    texto = re.sub(r"[%s]" % re.escape(string.punctuation), "", text)
    texto = re.sub(r"([0-9]u[0-9]{3,}b)", "", texto)
    texto = texto.replace(" ", "")
    texto = texto.lower()

    return texto


def menu_ayuda(update, context):
    query = update.callback_query
    print(query)
    query.answer()
    callback = query.data
    if callback == "m1":
        saludo(query)
    elif callback == "m2":
        help_grafo(query)
    elif callback == "m3":
        help_sec(query)
    elif callback == "m4":
        send_image(query)
    elif callback == "m5":
        send_doc(query, "src/docs/doc.pdf")
