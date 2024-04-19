from abc import ABC
from dataclasses import dataclass
from enum import Enum

from numpy import insert, where

class TipoAlimento(Enum):
    OVOS = 1
    SOJA = 2
    PEIXE = 3
    CARNE = 4

"""
data Alimento = OVOS
              | SOJA
              | PEIXE
              | Carne
              | Junta Alimento Alimento
              | Cozinha Alimento

tem_modo OVOS Vegetariano = True
tem_modo (Cozinha al) m = tem_modo al m

"""


class Alimento(ABC):
    pass

@dataclass
class AlimentoSimples(Alimento):
    nome:TipoAlimento

@dataclass
class SomaAlimento(Alimento):
    left: Alimento
    right: Alimento

@dataclass
class Cozinha(Alimento):
    alimento:Alimento

class Modo(Enum):
    VEGAN = 1
    VEGETARIANO = 2
    NORMAL = 3

    def __gt__(self, o):
        return self._value_ > o._value_

    def __ge__(self, o):
        return self._value_ >= o._value_

@dataclass
class Programa:
    al:Alimento
    m:Modo

    def __str__(self):
        return f"serve {self.al} {self.m}"


class TypeCheckingException(Exception):
    pass

modos_tipos_simples = {
    TipoAlimento.OVOS: Modo.VEGETARIANO,
    TipoAlimento.SOJA: Modo.VEGAN,
    TipoAlimento.CARNE: Modo.NORMAL,
    TipoAlimento.PEIXE: Modo.NORMAL,
}

def infere_modo(al:Alimento) -> Modo:
    if isinstance(al, AlimentoSimples):
        return modos_tipos_simples[al.nome]
    elif isinstance(al, Cozinha):
        return infere_modo(al.alimento)
    elif isinstance(al, SomaAlimento):
        m1 = infere_modo(al.left)
        m2 = infere_modo(al.right)
        return max(m1, m2)
    else:
        print(al)
        raise NotImplementedError()


def verifica_modo(al:Alimento, m:Modo) -> bool:
    """ T-subtyping """
    m1 = infere_modo(al)
    return m1 <= m

def valida(p:Programa):
    if not verifica_modo(p.al, p.m):
        raise TypeCheckingException(f"{p} não é válido")

al1 = SomaAlimento(
    AlimentoSimples(TipoAlimento.OVOS), 
    Cozinha(AlimentoSimples(TipoAlimento.SOJA))
)
p1 = Programa(al=al1, m=Modo.VEGETARIANO)
print(p1)

valida(p1)
