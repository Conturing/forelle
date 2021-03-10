from abc import ABC, abstractmethod

from pygame_widgets.widget import WidgetBase


class DynamicWidget(WidgetBase, ABC):

    @abstractmethod
    def partial_draw(self):
        """Redraw as little as necessary"""

