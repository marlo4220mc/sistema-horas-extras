"""Clase base de las personas que participan en el sistema."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Persona(ABC):
    """Datos comunes de identificacion de una persona.

    Es una clase abstracta: no se instancia directamente, se hereda.
    """

    def __init__(
        self,
        nombres: str,
        apellidos: str,
        tipo_documento: str,
        numero_documento: str,
        correo: str,
    ) -> None:
        self.nombres = nombres
        self.apellidos = apellidos
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento
        self.correo = correo

    @abstractmethod
    def obtener_rol(self) -> str:
        """Cada subclase indica el rol que cumple dentro de la empresa."""

    @property
    def nombres(self) -> str:
        return self._nombres

    @nombres.setter
    def nombres(self, valor: str) -> None:
        self._nombres = self._validar_texto(valor, "nombres")

    @property
    def apellidos(self) -> str:
        return self._apellidos

    @apellidos.setter
    def apellidos(self, valor: str) -> None:
        self._apellidos = self._validar_texto(valor, "apellidos")

    @property
    def tipo_documento(self) -> str:
        return self._tipo_documento

    @tipo_documento.setter
    def tipo_documento(self, valor: str) -> None:
        self._tipo_documento = self._validar_texto(valor, "tipo de documento")

    @property
    def numero_documento(self) -> str:
        return self._numero_documento

    @numero_documento.setter
    def numero_documento(self, valor: str) -> None:
        texto = self._validar_texto(valor, "numero de documento")
        if len(texto) < 6:
            raise ValueError("El numero de documento debe tener al menos 6 caracteres.")
        self._numero_documento = texto

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        texto = self._validar_texto(valor, "correo")
        if "@" not in texto or "." not in texto:
            raise ValueError("El correo no tiene un formato valido.")
        self._correo = texto

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombres} {self.apellidos}"

    @staticmethod
    def _validar_texto(valor: str, campo: str) -> str:
        """Metodo de apoyo para no repetir las validaciones de texto."""
        if valor is None or not str(valor).strip():
            raise ValueError(f"El campo {campo} no puede estar vacio.")
        return str(valor).strip()

    def __str__(self) -> str:
        return f"{self.nombre_completo} ({self.tipo_documento} {self.numero_documento})"
