from PyQt5.QtWidgets import QGraphicsPixmapItem, QApplication
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPixmap

from sensor import Sensor
from user import User

class MovingObject(QGraphicsPixmapItem):
    def __init__(self, obj, p_Ui_MainWindow):
        super().__init__()
        self.obj = obj  # This can be either a Sensor or an Asset
        self.pUi_MainWindow = p_Ui_MainWindow

        # Load the image and set it as the pixmap
        if isinstance(obj, User):
            self.setPixmap(QPixmap(obj.get_path())) # Placeholder for user
        else:
            self.setPixmap(QPixmap(obj.get_path_state2()))  # Placeholder for sensor and asset image

        self.setPos(obj.get_posX(), obj.get_posY())
        self.setAcceptHoverEvents(True)
        self.id_obj = obj.get_id()  # Generic method to get ID

    def hoverEnterEvent(self, event):
        QApplication.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        QApplication.instance().restoreOverrideCursor()

    def mousePressEvent(self, event):
        print("Click here")

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()
        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()

        # Get the scene rectangle
        scene_rect = self.scene().sceneRect()

        # Clamp the position within the scene boundaries
        updated_cursor_x = max(scene_rect.left(), min(updated_cursor_x, scene_rect.right() - self.pixmap().width()))
        updated_cursor_y = max(scene_rect.top(), min(updated_cursor_y, scene_rect.bottom() - self.pixmap().height()))

        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

        self.obj.set_posXY(updated_cursor_x, updated_cursor_y)

    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}, id: {2}'.format(self.pos().x(), self.pos().y(), self.id_obj))
        self.pUi_MainWindow.textField.setText('id: {0}, type: {1}, x: {2}, y: {3}, status: {4}'.format(
            self.id_obj,
            self.obj.get_type(),
            self.pos().x(),
            self.pos().y(),
            self.obj.get_status()))

    def change_image(self, image_path):
        self.setPixmap(QPixmap(image_path))
