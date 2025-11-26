import sys
import json
import paho.mqtt.client as mqtt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsPixmapItem, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QBrush, QColor
from PyQt5.QtCore import Qt, QPointF, pyqtSignal

class Sensor:
    def __init__(self, posX, posY, id):
        self.posX = posX
        self.posY = posY
        self.id = id
        self.state = "OFF"

    def get_posX(self):
        return self.posX

    def get_posY(self):
        return self.posY

    def get_id(self):
        return self.id

    def get_type(self):
        return "Sensor"

    def get_status(self):
        return self.state

    def set_posXY(self, x, y):
        self.posX = x
        self.posY = y

    def set_status(self, state):
        self.state = state


class MovingObject(QGraphicsPixmapItem):
    def __init__(self, obj, p_Ui_MainWindow):
        super().__init__()
        self.obj = obj  # This can be either a Sensor or an Asset
        self.pUi_MainWindow = p_Ui_MainWindow

        # Load the image and set it as the pixmap
        self.setPixmap(QPixmap("media/sensor_off.png"))

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


class Ui_MainWindow(QMainWindow):
    update_signal = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()

    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle('PyQt5 Drawing')
        MainWindow.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self.central_widget)
        self.layout.addWidget(self.view)

        self.textField = QLineEdit(self.central_widget)
        self.layout.addWidget(self.textField)

        # Draw a circle
        ellipse = QGraphicsEllipseItem(50, 50, 100, 100)
        ellipse.setBrush(QBrush(QColor("blue")))
        self.scene.addItem(ellipse)

        # Draw a rectangle
        rectangle = QGraphicsRectItem(200, 50, 150, 100)
        rectangle.setBrush(QBrush(QColor("red")))
        self.scene.addItem(rectangle)

        # Adding a moving object
        self.sensors = {}
        sensor = Sensor(300, 300, 1)
        self.moving_object = MovingObject(sensor, self)
        self.sensors[sensor.get_id()] = self.moving_object
        self.scene.addItem(self.moving_object)

        self.update_signal.connect(self.update_asset_state)
        self.setupMqttClient()

    def setupMqttClient(self):
        self.client = mqtt.Client("GUI-Subscribed")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("127.0.0.1", 1883, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("lab1006/control/asset")

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)
        id_asset = data.get("id")
        new_value = data.get("state_value")
        self.update_signal.emit(id_asset, new_value)

    def update_asset_state(self, id_asset, new_value):
        moving_object = self.sensors.get(id_asset)
        if moving_object:
            if new_value == "ON":
                moving_object.change_image("media/sensor_on.png")
                moving_object.obj.set_status("ON")
            else:
                moving_object.change_image("media/sensor_off.png")
                moving_object.obj.set_status("OFF")
            print(f"Updated asset::> {id_asset} to state {new_value}")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
