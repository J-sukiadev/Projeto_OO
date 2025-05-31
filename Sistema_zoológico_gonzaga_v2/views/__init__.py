# views/__init__.py
from .menu_principal import MenuPrincipal
from .animais_view import AnimaisView
from .habitats_view import HabitatsView
from .visitantes_view import VisitantesView
from .relatorios_view import RelatoriosView

__all__ = [
    'MenuPrincipal',
    'AnimaisView',
    'HabitatsView', 
    'VisitantesView',
    'RelatoriosView'
]