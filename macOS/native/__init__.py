"""NativeMode — registra dialectos.

Cada dialecto: native/<lang>/<dialect>.py → lista `RULES`.
Para agregar uno nuevo, importarlo aquí y registrarlo abajo.
"""

from .engine import NativeMode
from . import dialects

from .en import en_gb, en_us

NativeMode.register("en-US", en_us.RULES)
NativeMode.register("en-GB", en_gb.RULES)

from .es import es_ar, es_co, es_ve

NativeMode.register("es-VE", es_ve.RULES)
NativeMode.register("es-CO", es_co.RULES)
NativeMode.register("es-AR", es_ar.RULES)

__all__ = ["NativeMode", "dialects"]
