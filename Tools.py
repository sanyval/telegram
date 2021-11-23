import matplotlib.pyplot as plt
import networkx as nx
import random

def graficar(aristas,vertices, grado):
  plt.rcParams.update(plt.rcParamsDefault)
  plt.clf()
  g = nx.Graph()
  a = []
  edges = []

  for i in range(0, vertices):
    g.add_node(i)
    a.append(0)

  for i in range(0, aristas):
    while (True):
      nodo1 = random.randint(0, vertices - 1)
      nodo2 = random.randint(0, vertices - 1)
      if nodo1 != nodo2 and a[nodo1] < grado and a[nodo2] < grado and (nodo1, nodo2) not in edges and (nodo2, nodo1) not in edges:
        a[nodo1] += 1
        a[nodo2] += 1
        edges.append((nodo1, nodo2))
        break
  g.add_edges_from(edges)
  nx.draw(g, node_color='blue', with_labels=True, font_color='white', font_weight='bold')
  plt.savefig("src/images/grafo.png")

def transcribir(formula):
  symbols=["/","*","^","-","+"]
  letras=list(formula)
  ant=""
  parentesis=False
  frac=False
  num=""
  sol=""
  for letra in letras:
    if letra not in symbols:
      if not frac:
        num=num+letra
        sol=sol+letra
        ant=letra
      else:
        num=num+letra
        ant=letra
    else:
      if parentesis:
        sol=sol+")"
        parentesis=False
      elif frac:
        sol=sol+num+"}"
        frac=False
      if letra=="*":
        ant=letra
        sol=sol+r" \cdot "
      elif letra=="-":
        if ant in symbols:
          sol=sol+"("
          parentesis=True
        sol=sol+"-"
      elif letra=="^":
        sol=sol+"^"
      elif letra=="/":
        sol=sol[:len(sol)-len(num)]
        sol=sol+r" \frac{"+num+"}{"
        frac=True
      elif letra=="+":
        sol=sol+"+"

      num=""
      ant=letra
  
  return sol